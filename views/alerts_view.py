# views/alerts_view.py
import customtkinter as ctk
from tkinter import ttk
import threading
import time
import logging

from PIL._tkinter_finder import tk

logger = logging.getLogger(__name__)


class AlertsView(ctk.CTkFrame):
    VERSION = "2.0"  # Version tracking to confirm code changes

    def __init__(self, parent):
        super().__init__(parent)
        logger.info(f"AlertsView {self.VERSION} initialized")
        self.view_id = id(self)
        print(f"Creating AlertsView with ID: {self.view_id}")
        self.should_stop = False  # Add this flag
        self.controller = None
        self.tree = None
        self.details_text = None
        self.is_destroyed = False  # Flag to track destruction
        self.current_theme = ctk.get_appearance_mode().lower()  # Get current theme

        # Define theme colors
        self.colors = {
            "dark": {
                "treeview_bg": "#2b2b2b",
                "treeview_fg": "#32CD32",  # Lime green
                "header_bg": "#1e1e1e",
                "header_fg": "#32CD32",
                "selected_bg": "#3a3a3a",
                "selected_fg": "#32CD32",
                "details_bg": "#1e1e1e",
                "details_fg": "#32CD32",
                "details_border": "#404040",
                "critical": "#FF3333",  # Bright red
                "high": "#FF8C00",  # Dark orange
                "medium": "#32CD32",  # Lime green
                "low": "#98FB98"  # Pale green
            },
            "light": {
                "treeview_bg": "#FFFFFF",
                "treeview_fg": "#006400",  # Dark green
                "header_bg": "#F0F0F0",
                "header_fg": "#000000",
                "selected_bg": "#d0e8d0",
                "selected_fg": "#006400",
                "details_bg": "#FFFFFF",
                "details_fg": "#000000",
                "details_border": "#D0D0D0",
                "critical": "#D32F2F",  # Dark red
                "high": "#F57C00",  # Orange
                "medium": "#388E3C",  # Green
                "low": "#689F38"  # Light green
            }
        }

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_loading_state()
        self.update_thread = threading.Thread(target=self.update_alerts_periodically, daemon=True)
        self.update_thread.start()

    def set_controller(self, controller):
        self.controller = controller
        # Always check theme and rebuild UI when controller is set
        self.current_theme = ctk.get_appearance_mode().lower()
        logger.info(f"AlertsView theme: {self.current_theme}")
        self.show_alerts_page()
        self.after(100, self.controller.update_alerts)

    def create_loading_state(self):
        loading_label = ctk.CTkLabel(
            self,
            text="Loading alerts...",
            font=("Arial", 12)
        )
        loading_label.pack(pady=50)

    def show_alerts_page(self):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Update theme
        self.current_theme = ctk.get_appearance_mode().lower()

        # Create header
        self.create_header()

        # Create main content
        self.create_main_content()

    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        header_frame.grid_columnconfigure(1, weight=1)

        # Title with alert count
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            title_frame,
            text="Security Alerts",
            font=("Arial", 24, "bold")
        ).pack(side="left", padx=(0, 10))

        self.alert_count = ctk.CTkLabel(
            title_frame,
            text="0",
            font=("Arial", 14),
            fg_color="#e74c3c",
            text_color="white",
            corner_radius=8,
            width=30,
            height=30
        )
        self.alert_count.pack(side="left")

        # Action buttons
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=1, sticky="e")

        ctk.CTkButton(
            actions_frame,
            text="Acknowledge",
            command=self.acknowledge_alert,
            font=("Arial", 12),
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=120
        ).pack(side="right", padx=(10, 0))

        ctk.CTkButton(
            actions_frame,
            text="Refresh",
            command=self.refresh_alerts,
            font=("Arial", 12),
            width=100
        ).pack(side="right")

    def create_main_content(self):
        content_frame = ctk.CTkFrame(self)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # Get current theme colors
        theme_colors = self.colors[self.current_theme]

        # Create custom style for treeview based on current theme
        style = ttk.Style()

        # Define Treeview style
        style.configure(
            "Custom.Treeview",
            background=theme_colors["treeview_bg"],
            foreground=theme_colors["treeview_fg"],
            fieldbackground=theme_colors["treeview_bg"],
            borderwidth=0,
            font=("Arial", 10)
        )

        # Configure Treeview Headings
        style.configure(
            "Custom.Treeview.Heading",
            background=theme_colors["header_bg"],
            foreground=theme_colors["header_fg"],
            borderwidth=1,
            relief="flat",
            font=("Arial", 11, "bold")
        )

        # Heading hover effect
        style.map(
            "Custom.Treeview.Heading",
            background=[('active', theme_colors["selected_bg"])],
            foreground=[('active', theme_colors["header_fg"])]
        )

        # Row selection colors
        style.map(
            "Custom.Treeview",
            background=[('selected', theme_colors["selected_bg"])],
            foreground=[('selected', theme_colors["selected_fg"])]
        )

        # Initialize Treeview
        self.tree = ttk.Treeview(
            content_frame,
            columns=("Timestamp", "Level", "Description", "Location"),
            show="headings",
            height=15,
            style="Custom.Treeview"
        )

        # Configure scrollbar
        scrollbar = ctk.CTkScrollbar(content_frame, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Configure columns with better spacing and alignment
        columns = {
            "Timestamp": {"width": 180, "anchor": "w"},
            "Level": {"width": 100, "anchor": "center"},
            "Description": {"width": 400, "anchor": "w"},
            "Location": {"width": 200, "anchor": "w"}
        }

        for col, settings in columns.items():
            self.tree.heading(col, text=col, anchor=settings["anchor"])
            self.tree.column(col, width=settings["width"], anchor=settings["anchor"])

        self.tree.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        # Configure tag colors for different alert levels
        self.tree.tag_configure('critical', foreground=theme_colors["critical"])
        self.tree.tag_configure('high', foreground=theme_colors["high"])
        self.tree.tag_configure('medium', foreground=theme_colors["medium"])
        self.tree.tag_configure('low', foreground=theme_colors["low"])

        # Details section
        # Use a different color for the details frame based on the theme
        details_frame = ctk.CTkFrame(
            content_frame,
            fg_color=theme_colors["details_bg"],
            border_width=1,
            border_color=theme_colors["details_border"]
        )
        details_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        ctk.CTkLabel(
            details_frame,
            text="Alert Details",
            font=("Arial", 16, "bold"),
            text_color=theme_colors["details_fg"]
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.details_text = ctk.CTkTextbox(
            details_frame,
            height=100,
            font=("Arial", 12),
            fg_color=theme_colors["details_bg"],
            text_color=theme_colors["details_fg"],
            border_width=1,
            border_color=theme_colors["details_border"]
        )
        self.details_text.pack(fill="x", padx=15, pady=(0, 15))
        self.details_text.insert("1.0", "Select an alert to view details")
        self.details_text.configure(state="disabled")

        # Bind events
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def update_alerts(self, alerts):
        """Safe update method that checks widget validity"""
        # Check if view is destroyed
        if self.is_destroyed:
            print(f"AlertsView {self.view_id}: Can't update, view is destroyed")
            return

        # Check if tree widget exists and is valid
        if not self.tree:
            print(f"AlertsView {self.view_id}: Tree widget not created yet")
            return

        try:
            # Try to check if widget still exists in Tk
            self.tree.winfo_exists()
        except (tk.TclError, RuntimeError, Exception) as e:
            print(f"AlertsView {self.view_id}: Tree widget no longer valid: {e}")
            return

        try:
            # Clear existing items
            existing_items = self.tree.get_children()
            if existing_items:
                self.tree.delete(*existing_items)

            # Insert new alerts
            for alert in alerts:
                level = alert["actions"].lower()
                tag = level if level in ['critical', 'high', 'medium', 'low'] else ''

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        alert["timestamp"],
                        alert["actions"],
                        alert["type"],
                        alert["file"]
                    ),
                    tags=(tag,)
                )

            # Update alert count safely
            try:
                if hasattr(self, 'alert_count'):
                    self.alert_count.configure(text=str(len(alerts)))
            except Exception as count_err:
                print(f"Error updating alert count: {count_err}")

        except Exception as e:
            print(f"Error updating alerts display: {e}")
            import traceback
            traceback.print_exc()

    def refresh_alerts(self):
        """Manually refresh alerts"""
        if self.controller:
            self.controller.update_alerts()

    def acknowledge_alert(self):
        """Acknowledge selected alert"""
        if self.controller:
            self.controller.acknowledge_alert()

    def on_select(self, event):
        """Handle alert selection"""
        selected_item = self.tree.focus()
        if not selected_item:
            return

        values = self.tree.item(selected_item)['values']
        if not values:
            return

        self.details_text.configure(state="normal")
        self.details_text.delete("1.0", "end")
        details = (
            f"Timestamp: {values[0]}\n"
            f"Alert Level: {values[1]}\n"
            f"Description: {values[2]}\n"
            f"Location: {values[3]}\n"
        )
        self.details_text.insert("1.0", details)
        self.details_text.configure(state="disabled")

    def update_alerts_periodically(self):
        """Update alerts periodically with better error handling"""
        while True:
            try:
                # Check if view is destroyed or no longer mapped
                if self.is_destroyed:
                    print(f"AlertsView {self.view_id}: Stopping periodic updates (destroyed)")
                    break

                # Only update if controller exists and view is visible
                if self.controller and self.winfo_ismapped():
                    self.controller.update_alerts()
                else:
                    # Skip update but continue the loop
                    pass

                # Sleep for the update interval
                time.sleep(30)
            except Exception as e:
                print(f"Error in periodic update: {e}")
                # Shorter sleep on error
                time.sleep(5)

    def destroy(self):
        """Override destroy to properly clean up"""
        print(f"Destroying AlertsView {self.view_id}")
        self.is_destroyed = True  # Set flag first

        try:
            # Clean up any resources before destruction
            if hasattr(self, 'tree') and self.tree:
                try:
                    self.tree.destroy()
                except:
                    pass
                self.tree = None
        except Exception as e:
            print(f"Error during AlertsView cleanup: {e}")

        # Call parent destroy
        super().destroy()
