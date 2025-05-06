import customtkinter as ctk
from tkinter import ttk
import logging

from PIL._tkinter_finder import tk

logger = logging.getLogger(__name__)


class IncidentHistoryView(ctk.CTkFrame):
    VERSION = "2.0"  # Version tracking

    def __init__(self, parent):
        super().__init__(parent)
        logger.info(f"IncidentHistoryView {self.VERSION} initialized")
        self.controller = None
        self.filter_type_combo = None
        self.filter_entry = None
        self.incident_frame = None
        self.message_label = None
        self.loading_label = None

        self.is_destroyed = False
        self.view_id = id(self)
        print(f"Creating IncidentHistoryView with ID: {self.view_id}")

        # Get current theme
        self.current_theme = ctk.get_appearance_mode().lower()
        logger.info(f"Initial theme: {self.current_theme}")

        # Define theme colors
        self.colors = {
            "dark": {
                "card_bg": "#2b2b2b",
                "card_border": "#404040",
                "accent": "#32CD32",  # Lime green
                "text": "#FFFFFF",
                "subtext": "#AAAAAA"
            },
            "light": {
                "card_bg": "#FFFFFF",
                "card_border": "#D0D0D0",
                "accent": "#007700",  # Dark green
                "text": "#000000",
                "subtext": "#666666"
            }
        }

        # Configure grid
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_incident_response_history_page()

    def set_controller(self, controller):
        """Sets the controller and initializes the data"""
        self.controller = controller
        # Always check theme when controller is set
        self.current_theme = ctk.get_appearance_mode().lower()
        logger.info(f"IncidentHistoryView theme after set_controller: {self.current_theme}")

        # Recreate the UI with current theme
        self.create_incident_response_history_page()

        self.update_incidents()

    def create_incident_response_history_page(self):
        """Creates the incident response history UI with a modern look."""
        self.grid_rowconfigure(2, weight=1)  # Make incident list expandable
        self.grid_columnconfigure(0, weight=1)

        # Update current theme
        self.current_theme = ctk.get_appearance_mode().lower()

        # Title and Loading Section
        title_frame = self.create_title_section()
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        # Filter Controls Section
        filter_frame = self.create_filter_section()
        filter_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))

        # Incident List Section
        self.create_incident_list_section()

        # Action Buttons Section
        self.create_action_buttons()

    def create_title_section(self):
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid_columnconfigure(1, weight=1)

        title_label = ctk.CTkLabel(
            title_frame,
            text="Incident Response History",
            font=("Arial", 24, "bold")
        )
        title_label.grid(row=0, column=0, sticky="w")

        self.loading_label = ctk.CTkLabel(
            title_frame,
            text="Syncing...",
            font=("Arial", 12),
            text_color="gray"
        )
        self.loading_label.grid(row=0, column=1, sticky="e")
        self.loading_label.grid_remove()

        return title_frame

    def create_filter_section(self):
        filter_frame = ctk.CTkFrame(self)
        filter_frame.grid_columnconfigure(1, weight=1)

        # Filter type dropdown
        self.filter_type_combo = ctk.CTkComboBox(
            filter_frame,
            values=["All", "Date", "Incident", "Action"],
            state="readonly",
            width=150,
            font=("Arial", 12)
        )
        self.filter_type_combo.set("All")
        self.filter_type_combo.grid(row=0, column=0, padx=(10, 5), pady=10)

        # Search entry
        self.filter_entry = ctk.CTkEntry(
            filter_frame,
            placeholder_text="Search incidents...",
            font=("Arial", 12),
            height=32
        )
        self.filter_entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        # Buttons frame
        buttons_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        buttons_frame.grid(row=0, column=2, padx=(5, 10), pady=10)

        # Filter buttons
        ctk.CTkButton(
            buttons_frame,
            text="Apply",
            command=self.apply_filter,
            width=80,
            font=("Arial", 12)
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            buttons_frame,
            text="Clear",
            command=self.clear_filter,
            width=80,
            font=("Arial", 12)
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            buttons_frame,
            text="↻",
            command=self.refresh_incidents,
            width=40,
            font=("Arial", 12)
        ).pack(side="left", padx=2)

        return filter_frame

    def create_incident_list_section(self):
        # Incident list container with theme-aware styling
        self.incident_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            height=400
        )
        self.incident_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

    def create_incident_card(self, incident):
        # Get current theme colors
        theme_colors = self.colors[self.current_theme]

        card = ctk.CTkFrame(
            self.incident_frame,
            fg_color=theme_colors["card_bg"],
            corner_radius=6,
            border_width=1,
            border_color=theme_colors["card_border"]
        )
        card.pack(fill="x", pady=5, padx=5)

        # Date header
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkLabel(
            header_frame,
            text=incident['Date'],
            font=("Arial", 12, "bold"),
            text_color=theme_colors["accent"]
        ).pack(side="left")

        # Incident details
        details_frame = ctk.CTkFrame(card, fg_color="transparent")
        details_frame.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(
            details_frame,
            text=incident['Incident'],
            font=("Arial", 12),
            wraplength=500,
            justify="left",
            text_color=theme_colors["text"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            details_frame,
            text=f"Action: {incident['Action']}",
            font=("Arial", 11),
            text_color=theme_colors["subtext"],
            wraplength=500,
            justify="left"
        ).pack(anchor="w", pady=(5, 0))

    def create_action_buttons(self):
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=3, column=0, pady=20)

        ctk.CTkButton(
            button_frame,
            text="Export CSV",
            command=self.export_incident_history,
            font=("Arial", 12),
            width=120
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Print",
            command=self.print_incident_history,
            font=("Arial", 12),
            width=120
        ).pack(side="left", padx=5)

    def show_loading(self, show=True):
        """Shows or hides the loading indicator"""
        if show:
            self.loading_label.grid()
        else:
            self.loading_label.grid_remove()

    def apply_filter(self):
        """Applies the selected filter to the incident list."""
        filter_type = self.filter_type_combo.get()
        filter_value = self.filter_entry.get().strip()
        self.update_incidents(filter_type, filter_value)

    def clear_filter(self):
        """Clears the filter and refreshes the data."""
        self.filter_type_combo.set("All")
        self.filter_entry.delete(0, "end")
        self.update_incidents()

    def refresh_incidents(self):
        """Refreshes the incident list."""
        self.show_loading(True)
        if self.controller:
            success = self.controller.refresh_incidents()
            if success:
                self.show_message("Incidents refreshed successfully")
            else:
                self.show_message("Failed to refresh incidents", "red")
        self.show_loading(False)

    def update_incidents(self, incidents=None):
        """Update the incident display with proper widget validity checking"""
        if self.is_destroyed:
            print(f"IncidentHistoryView {self.view_id}: Can't update, view is destroyed")
            return

        try:
            # Check if incident_frame exists and is valid
            if not hasattr(self, 'incident_frame') or not self.winfo_exists():
                print(f"IncidentHistoryView {self.view_id}: Widget no longer valid")
                return

            # Try to verify the widget still exists in Tk
            try:
                self.incident_frame.winfo_exists()
            except (tk.TclError, RuntimeError, Exception) as e:
                print(f"IncidentHistoryView {self.view_id}: Incident frame no longer valid: {e}")
                return

            # Now proceed with the update
            # Clear existing items
            for widget in self.incident_frame.winfo_children():
                widget.destroy()

            # Get current incidents from controller
            if self.controller:
                incidents_to_display = self.controller.get_incidents()
                if incidents_to_display:
                    print(f"Displaying {len(incidents_to_display)} incidents")
                    for incident in incidents_to_display:
                        self.create_incident_card(incident)
                else:
                    print("No incidents to display")
                    # Show a message in the incident frame when no incidents are available
                    empty_label = ctk.CTkLabel(
                        self.incident_frame,
                        text="No incident history available",
                        font=("Arial", 14),
                        text_color="gray"
                    )
                    empty_label.pack(pady=30)
            else:
                print("Controller not available")

        except Exception as e:
            print(f"Error updating incidents display: {e}")
            import traceback
            traceback.print_exc()

    def export_incident_history(self):
        """Exports incident history to CSV"""
        if self.controller:
            self.controller.export_incident_history()

    def print_incident_history(self):
        """Prints incident history"""
        if self.controller:
            self.controller.print_incident_history()

    def show_message(self, message, color="green"):
        """Shows a temporary message to the user"""
        if not hasattr(self, 'message_label') or self.message_label is None:
            self.message_label = ctk.CTkLabel(
                self,
                text="",
                font=("Arial", 12),
                text_color=color
            )
            self.message_label.grid(row=4, column=0, pady=(0, 10))

        self.message_label.configure(text=message, text_color=color)
        self.after(5000, lambda: self.message_label.configure(text=""))

        # Override destroy method

    def destroy(self):
        """Override destroy to properly clean up"""
        print(f"Destroying IncidentHistoryView {self.view_id}")
        self.is_destroyed = True  # Set flag first

        # Tell controller this view is being destroyed
        if hasattr(self, 'controller') and self.controller:
            self.controller.view_destroyed(self)

        try:
            # Clean up any resources before destruction
            if hasattr(self, 'incident_frame'):
                try:
                    self.incident_frame.destroy()
                except:
                    pass
                self.incident_frame = None
        except Exception as e:
            print(f"Error during IncidentHistoryView cleanup: {e}")

        # Call parent destroy
        super().destroy()
