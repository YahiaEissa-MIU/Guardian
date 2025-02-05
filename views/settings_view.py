import customtkinter as ctk


class SettingsView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.router = parent
        self.controller = controller  # Use the controller passed from the router
        self.create_settings_page()

    def create_settings_page(self):
        for widget in self.winfo_children():
            widget.destroy()

        scrollable_frame = ctk.CTkScrollableFrame(self, width=600, height=500, corner_radius=10)
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        title_label = ctk.CTkLabel(scrollable_frame, text="Settings", font=("Arial", 20, "bold"))
        title_label.pack(pady=20)

        general_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
        general_frame.pack(pady=10, padx=20, fill="x")

        general_label = ctk.CTkLabel(general_frame, text="General Settings", font=("Arial", 16, "bold"))
        general_label.pack(anchor="w", pady=10, padx=10)

        auto_response_toggle = ctk.CTkSwitch(
            general_frame, text="Automatically detect and respond to ransomware threats.",
            variable=self.controller.auto_response_var,
            command=self.controller.toggle_auto_response
        )
        auto_response_toggle.pack(anchor="w", padx=20, pady=5)

        notify_toggle = ctk.CTkSwitch(
            general_frame, text="Notify me when threats are detected or resolved.",
            variable=self.controller.notify_var,
            command=self.controller.toggle_notifications
        )
        notify_toggle.pack(anchor="w", padx=20, pady=5)

        security_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
        security_frame.pack(pady=10, padx=20, fill="x")

        security_label = ctk.CTkLabel(security_frame, text="Security Settings", font=("Arial", 16, "bold"))
        security_label.pack(anchor="w", pady=10, padx=10)

        real_time_toggle = ctk.CTkSwitch(
            security_frame, text="Continuously monitor for ransomware activities.",
            variable=self.controller.real_time_var,
            command=self.controller.toggle_real_time
        )
        real_time_toggle.pack(anchor="w", padx=20, pady=5)

        backup_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
        backup_frame.pack(pady=10, padx=20, fill="x")

        backup_label = ctk.CTkLabel(backup_frame, text="Backup & Recovery Settings", font=("Arial", 16, "bold"))
        backup_label.pack(anchor="w", pady=10, padx=10)

        recovery_dropdown = ctk.CTkOptionMenu(
            backup_frame, values=["Most Recent Backup", "Custom Recovery Point"],
            variable=self.controller.recovery_var
        )
        recovery_dropdown.pack(anchor="w", padx=20, pady=5)

        auto_backup_toggle = ctk.CTkSwitch(
            backup_frame, text="Enable automatic backup of critical files.",
            variable=self.controller.auto_backup_var,
            command=self.controller.toggle_auto_backup
        )
        auto_backup_toggle.pack(anchor="w", padx=20, pady=5)

        frequency_dropdown = ctk.CTkOptionMenu(
            backup_frame, values=["Hourly", "Daily", "Weekly"],
            variable=self.controller.frequency_var
        )
        frequency_dropdown.pack(anchor="w", padx=20, pady=5)

        advanced_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
        advanced_frame.pack(pady=10, padx=20, fill="x")

        advanced_label = ctk.CTkLabel(advanced_frame, text="Advanced Options", font=("Arial", 16, "bold"))
        advanced_label.pack(anchor="w", pady=10, padx=10)

        exclude_entry = ctk.CTkEntry(advanced_frame, placeholder_text="Enter file/folder paths")
        exclude_entry.pack(anchor="w", padx=20, pady=5)

        reset_button = ctk.CTkButton(advanced_frame, text="Reset to Default", command=self.controller.reset_to_default)
        reset_button.pack(anchor="w", padx=20, pady=10)

        resources_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
        resources_frame.pack(pady=10, padx=20, fill="x")

        resources_label = ctk.CTkLabel(resources_frame, text="Educational Resources", font=("Arial", 16, "bold"))
        resources_label.pack(anchor="w", pady=10, padx=10)

        guide_button = ctk.CTkButton(resources_frame, text="Learn About Ransomware", command=self.controller.open_guide)
        guide_button.pack(anchor="w", padx=20, pady=5)
