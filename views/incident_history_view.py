import customtkinter as ctk
from tkinter import ttk


class IncidentHistoryView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.filter_type_combo = None
        self.filter_entry = None
        self.incident_frame = None
        self.message_label = None
        self.loading_label = None
        self.create_incident_response_history_page()

    def set_controller(self, controller):
        """Sets the controller reference."""
        self.controller = controller
        self.update_incidents()  # Load initial data from the controller

    def create_incident_response_history_page(self):
        """Creates the incident response history UI with a modern look."""
        for widget in self.winfo_children():
            widget.destroy()

        # Title and Loading Frame
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", pady=(20, 10), padx=20)

        title_label = ctk.CTkLabel(
            title_frame,
            text="Incident Response History",
            font=("Arial", 22, "bold")
        )
        title_label.pack(side="left")

        self.loading_label = ctk.CTkLabel(
            title_frame,
            text="🔄 Syncing...",
            font=("Arial", 12),
            text_color="gray"
        )
        self.loading_label.pack(side="right")
        self.loading_label.pack_forget()

        # Filter Controls
        filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        filter_frame.pack(pady=10, padx=20, fill="x")

        self.filter_type_combo = ctk.CTkComboBox(
            filter_frame,
            values=["All", "Date", "Incident", "Action"],
            state="readonly",
            width=150
        )
        self.filter_type_combo.set("All")
        self.filter_type_combo.pack(side="left", padx=10)

        self.filter_entry = ctk.CTkEntry(
            filter_frame,
            placeholder_text="Search...",
            width=250
        )
        self.filter_entry.pack(side="left", padx=10, expand=True, fill="x")

        apply_button = ctk.CTkButton(
            filter_frame,
            text="Apply Filter",
            command=self.apply_filter,
            width=100
        )
        apply_button.pack(side="left", padx=5)

        clear_button = ctk.CTkButton(
            filter_frame,
            text="Clear Filter",
            command=self.clear_filter,
            width=100
        )
        clear_button.pack(side="left", padx=5)

        refresh_button = ctk.CTkButton(
            filter_frame,
            text="🔄 Refresh",
            command=self.refresh_incidents,
            width=100
        )
        refresh_button.pack(side="left", padx=5)

        # Incident List
        self.incident_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            height=400
        )
        self.incident_frame.pack(fill="both", expand=True, pady=10, padx=20)

        # Message Label
        self.message_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 12),
            text_color="green"
        )
        self.message_label.pack(pady=5)

        # Button Actions
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20)

        export_button = ctk.CTkButton(
            button_frame,
            text="Export as CSV",
            command=self.export_incident_history
        )
        export_button.pack(side="left", padx=10)

        printer_button = ctk.CTkButton(
            button_frame,
            text="🖨️ Print",
            command=self.print_incident_history
        )
        printer_button.pack(side="left", padx=10)

        # Initial update
        self.update_incidents()

    def show_loading(self, show=True):
        """Shows or hides the loading indicator"""
        if show:
            self.loading_label.pack(side="right")
        else:
            self.loading_label.pack_forget()

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

    def get_filter_type(self):
        """Returns the selected filter type from the dropdown."""
        return self.filter_type_combo.get()

    def get_filter_value(self):
        """Returns the filter value from the search entry."""
        return self.filter_entry.get().strip()

    def update_incidents(self, filter_type="All", filter_value=""):
        """Refreshes the displayed incident history with optional filters."""
        for widget in self.incident_frame.winfo_children():
            widget.destroy()

        incidents = self.controller.get_incidents(filter_type, filter_value) if self.controller else []
        print(f"Updating view with {len(incidents)} incidents")  # Debug print

        if not incidents:
            no_data_label = ctk.CTkLabel(
                self.incident_frame,
                text="No incidents recorded.",
                font=("Arial", 14, "italic")
            )
            no_data_label.pack(pady=5, padx=10)
            return

        for incident in incidents:
            frame = ctk.CTkFrame(
                self.incident_frame,
                corner_radius=10,
                border_width=1,
                border_color="#ddd"
            )
            frame.pack(fill="x", pady=5, padx=10)

            # Date with icon
            date_label = ctk.CTkLabel(
                frame,
                text=f"📅 {incident['Date']}",
                font=("Arial", 12, "bold")
            )
            date_label.pack(anchor="w", padx=10, pady=(5, 0))

            # Incident with icon
            incident_label = ctk.CTkLabel(
                frame,
                text=f"🚨 {incident['Incident']}",
                font=("Arial", 14)
            )
            incident_label.pack(anchor="w", padx=10, pady=(0, 0))

            # Action with icon
            action_label = ctk.CTkLabel(
                frame,
                text=f"⚡ Action: {incident['Action']}",
                font=("Arial", 12),
                text_color="gray"
            )
            action_label.pack(anchor="w", padx=10, pady=(0, 5))

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

    def export_incident_history(self):
        if self.controller:
            self.controller.export_incident_history()

    def print_incident_history(self):
        if self.controller:
            self.controller.print_incident_history()

    def show_message(self, message, color="green"):
        """Displays a message to the user."""
        self.message_label.configure(text=message, text_color=color)
        # Auto-hide message after 5 seconds
        self.after(5000, lambda: self.message_label.configure(text=""))
