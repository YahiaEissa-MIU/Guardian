# views/alerts_view.py

import customtkinter as ctk
from tkinter import ttk
import threading
import time


class AlertsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = None
        self.tree = None
        self.details_text = None

        # Start with loading state
        self.create_loading_state()

        # Start update thread
        self.update_thread = threading.Thread(target=self.update_alerts_periodically, daemon=True)
        self.update_thread.start()

    def create_loading_state(self):
        """Show loading state"""
        loading_label = ctk.CTkLabel(self, text="Loading alerts...")
        loading_label.pack(pady=50)

    def set_controller(self, controller):
        """Set controller and initialize view"""
        self.controller = controller
        self.show_alerts_page()
        # Force immediate update after UI is ready
        self.after(100, self.controller.update_alerts)  # Use after to ensure UI is ready

    def show_alerts_page(self):
        """Initialize the alerts page"""
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Header Frame
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        title_label = ctk.CTkLabel(
            header_frame,
            text="Security Alerts",
            font=("Arial", 24, "bold")
        )
        title_label.pack(side="left")

        # Buttons Frame
        buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        buttons_frame.pack(side="right")

        acknowledge_button = ctk.CTkButton(
            buttons_frame,
            text="Acknowledge Alert",
            command=self.acknowledge_alert,
            width=120
        )
        acknowledge_button.pack(side="right", padx=(10, 0))

        refresh_button = ctk.CTkButton(
            buttons_frame,
            text="Refresh",
            command=self.refresh_alerts,
            width=100
        )
        refresh_button.pack(side="right")

        # Main Content Frame
        content_frame = ctk.CTkFrame(self)
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Treeview Frame
        tree_frame = ctk.CTkFrame(content_frame)
        tree_frame.pack(fill="both", expand=True, pady=(0, 10))

        # Initialize Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Timestamp", "Level", "Description", "Location"),
            show="headings",
            height=15
        )

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Configure columns
        self.tree.heading("Timestamp", text="Timestamp", anchor="center")
        self.tree.heading("Level", text="Level", anchor="center")
        self.tree.heading("Description", text="Description", anchor="w")
        self.tree.heading("Location", text="Location", anchor="w")

        self.tree.column("Timestamp", width=150, anchor="center")
        self.tree.column("Level", width=80, anchor="center")
        self.tree.column("Description", width=400, anchor="w")
        self.tree.column("Location", width=200, anchor="w")

        # Pack Treeview and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Details Frame
        details_frame = ctk.CTkFrame(content_frame)
        details_frame.pack(fill="x", pady=(10, 0))

        details_label = ctk.CTkLabel(
            details_frame,
            text="Alert Details",
            font=("Arial", 16, "bold")
        )
        details_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.details_text = ctk.CTkTextbox(
            details_frame,
            height=100,
            wrap="word"
        )
        self.details_text.pack(fill="x", padx=10, pady=(0, 10))
        self.details_text.insert("1.0", "Select an alert to view details")
        self.details_text.configure(state="disabled")

        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def update_alerts(self, alerts):
        """Update the alerts display"""
        if not self.tree:
            return

        try:
            # Clear existing items
            self.tree.delete(*self.tree.get_children())

            # Add new alerts
            for alert in alerts:
                self.tree.insert("", "end", values=(
                    alert["timestamp"],
                    alert["actions"],
                    alert["type"],
                    alert["file"]
                ))
        except Exception as e:
            print(f"Error updating alerts display: {e}")

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
        """Update alerts periodically"""
        while True:
            try:
                if self.controller:
                    self.controller.update_alerts()
                time.sleep(30)
            except Exception as e:
                print(f"Error in periodic update: {e}")
                time.sleep(5)