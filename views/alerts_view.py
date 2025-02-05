from tkinter import ttk
import customtkinter as ctk


class AlertsView(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = None
        self.tree = None
        self.details_text = None

        if controller:
            self.set_controller(controller)
        else:
            self.create_loading_state()

    def create_loading_state(self):
        """Temporary UI until controller is set"""
        for widget in self.winfo_children():
            widget.destroy()

        loading_label = ctk.CTkLabel(self, text="Loading alerts...")
        loading_label.pack(pady=50)

    def set_controller(self, controller):
        """Finalize initialization when controller is available"""
        self.controller = controller
        self.show_alerts_page()

    def show_alerts_page(self):
        """Create full UI after controller is set"""
        for widget in self.winfo_children():
            widget.destroy()

        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Ransomware Alerts",
            font=("Arial", 22, "bold"),

        )
        title_label.pack(pady=10)

        # Treeview setup
        alerts_frame = ctk.CTkFrame(self, corner_radius=10)
        alerts_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(alerts_frame, columns=("Timestamp", "Type", "File", "Actions"),
                                 show="headings", height=12)

        # Configure columns
        self.tree.heading("Timestamp", text="Timestamp")
        self.tree.heading("Type", text="Threat Type")
        self.tree.heading("File", text="Affected File")
        self.tree.heading("Actions", text="Actions Taken")

        self.tree.column("Timestamp", anchor="center", width=150)
        self.tree.column("Type", anchor="center", width=150)
        self.tree.column("File", anchor="center", width=300)  # Centered "Affected File" column
        self.tree.column("Actions", anchor="center", width=150)

        for alert in self.controller.get_alerts():
            self.tree.insert("", "end", values=(
                alert["timestamp"],
                alert["type"],
                alert["file"],
                alert["actions"]
            ))
        self.tree.pack(fill="both", expand=True)

        # Details Section
        details_frame = ctk.CTkFrame(self)
        details_frame.pack(fill="x", padx=20, pady=10)

        details_label = ctk.CTkLabel(details_frame, text="Alert Details:", font=("Arial", 14, "bold"))
        details_label.grid(row=0, column=0, sticky="w", padx=10)

        self.details_text = ctk.CTkLabel(details_frame, text="", font=("Arial", 12), justify="left")
        self.details_text.grid(row=1, column=0, sticky="w", padx=10)

        # Bind event for selecting an alert
        self.tree.bind("<ButtonRelease-1>", self.display_details)

        # Acknowledge Button
        acknowledge_button = ctk.CTkButton(
            self,
            text="Acknowledge Alert",
            command=self.controller.acknowledge_alert,

        )
        acknowledge_button.pack(pady=10)

    def display_details(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            alert_details = self.tree.item(selected_item, "values")
            self.details_text.configure(
                text=f"Type: {alert_details[1]}\n"
                     f"Affected File: {alert_details[2]}\n"
                     f"Actions Taken: {alert_details[3]}"
            )

    def update_alerts(self, alerts):
        """Refresh the treeview with updated alerts"""
        self.tree.delete(*self.tree.get_children())
        for alert in alerts:
            self.tree.insert("", "end", values=(
                alert["timestamp"],
                alert["type"],
                alert["file"],
                alert["actions"]
            ))
