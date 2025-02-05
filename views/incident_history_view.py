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
        self.create_incident_response_history_page()

    def set_controller(self, controller):
        """Sets the controller reference."""
        self.controller = controller
        self.update_incidents()  # Load initial data from the controller

    def create_incident_response_history_page(self):
        """Creates the incident response history UI with a modern look."""
        for widget in self.winfo_children():
            widget.destroy()

        # Title
        title_label = ctk.CTkLabel(self, text="Incident Response History", font=("Arial", 22, "bold"))
        title_label.pack(pady=(20, 10))

        # Filter Controls
        filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        filter_frame.pack(pady=10, padx=20, fill="x")

        self.filter_type_combo = ctk.CTkComboBox(
            filter_frame, values=["All", "Date", "Incident", "Action"], state="readonly", width=150
        )
        self.filter_type_combo.set("All")
        self.filter_type_combo.pack(side="left", padx=10)

        self.filter_entry = ctk.CTkEntry(filter_frame, placeholder_text="Search...", width=250)
        self.filter_entry.pack(side="left", padx=10, expand=True, fill="x")

        apply_button = ctk.CTkButton(filter_frame, text="Apply", command=self.apply_filter, width=100)
        apply_button.pack(side="left", padx=5)

        clear_button = ctk.CTkButton(filter_frame, text="Clear", command=self.clear_filter, width=100)
        clear_button.pack(side="left", padx=5)

        # Incident List
        self.incident_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.incident_frame.pack(fill="both", expand=True, pady=10, padx=20)

        self.message_label = ctk.CTkLabel(self, text="", font=("Arial", 12), text_color="green")
        self.message_label.pack(pady=5)

        # Button Actions
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20)

        export_button = ctk.CTkButton(button_frame, text="Export as CSV", command=self.export_incident_history)
        export_button.pack(side="left", padx=10)

        printer_button = ctk.CTkButton(button_frame, text=" 🖨️ Print", command=self.print_incident_history)
        printer_button.pack(side="left", padx=10)

        self.update_incidents()

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

        if not incidents:
            no_data_label = ctk.CTkLabel(self.incident_frame, text="No incidents recorded.", font=("Arial", 14, "italic"))
            no_data_label.pack(pady=5, padx=10)
            return

        for incident in incidents:
            frame = ctk.CTkFrame(self.incident_frame, corner_radius=10, border_width=1, border_color="#ddd")
            frame.pack(fill="x", pady=5, padx=10)

            details = f"{incident['Date']} - {incident['Incident']} - Action: {incident['Action']}"
            label = ctk.CTkLabel(frame, text=details, font=("Arial", 14), anchor="w")
            label.pack(padx=10, pady=5, fill="x")

    def export_incident_history(self):
        if self.controller:
            self.controller.export_incident_history()

    def print_incident_history(self):
        if self.controller:
            self.controller.print_incident_history()

    def show_message(self, message, color="green"):
        """Displays a message to the user."""
        self.message_label.configure(text=message, text_color=color)

