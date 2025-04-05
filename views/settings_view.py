import customtkinter as ctk
from typing import List


class SettingsView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        print("Initializing SettingsView...")
        self.router = parent
        self.controller = controller
        self.controller.set_view(self)
        # Define common styles
        self.SECTION_FONT = ("Helvetica", 18, "bold")
        self.SUBTITLE_FONT = ("Helvetica", 14)
        self.BUTTON_FONT = ("Helvetica", 12)
        self.SECTION_PADDING = (20, 15)
        self.WIDGET_PADDING = (0, 8)

        self.create_settings_page()
        print("SettingsView initialized")

    def get_agent_ip(self):
        """Get the IP address from the agent IP entry field"""
        if hasattr(self, 'agent_ip_entry'):
            return self.agent_ip_entry.get().strip()
        return ""

    def create_settings_page(self):
        print("Creating settings page...")
        for widget in self.winfo_children():
            widget.destroy()

        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))

        title_label = ctk.CTkLabel(
            header_frame,
            text="Settings",
            font=("Helvetica", 24, "bold")
        )
        title_label.pack(side="left")

        # Main scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(
            main_container,
            width=680,
            height=580,
            corner_radius=15
        )
        scrollable_frame.pack(fill="both", expand=True)

        # Create general settings sections
        self.create_notification_settings(scrollable_frame)
        self.create_backup_settings(scrollable_frame)
        self.create_suspicious_paths_settings(scrollable_frame)

        # Separator before Advanced settings
        separator = ctk.CTkFrame(scrollable_frame, height=2, fg_color="gray70")
        separator.pack(fill="x", pady=20, padx=2)

        # Advanced Settings Header
        advanced_header = ctk.CTkLabel(
            scrollable_frame,
            text="Advanced Settings",
            font=("Helvetica", 20, "bold")
        )
        advanced_header.pack(anchor="w", pady=(0, 20), padx=2)

        # Create advanced settings sections
        self.create_api_connection_settings(scrollable_frame)
        self.create_agent_settings(scrollable_frame)
        self.create_shuffle_settings(scrollable_frame)

    def create_notification_settings(self, parent):
        section_frame = self.create_section_frame(parent, "Notification Settings")

        # Description label
        description = ctk.CTkLabel(
            section_frame,
            text="Configure desktop notifications for security alerts",
            font=self.SUBTITLE_FONT
        )
        description.pack(anchor="w", pady=(0, 15))

        # Notification switch
        notification_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        notification_frame.pack(fill="x", pady=(0, 10))

        switch = ctk.CTkSwitch(
            notification_frame,
            text="Enable desktop notifications",
            variable=self.controller.notify_var,
            command=self.controller.toggle_notifications,
            font=self.SUBTITLE_FONT,
            height=32
        )
        switch.pack(side="left")

        # Test notification button
        test_notify_button = ctk.CTkButton(
            section_frame,
            text="Test Notification",
            command=self.controller.test_notification,
            font=self.BUTTON_FONT,
            height=32,
            width=120
        )
        test_notify_button.pack(anchor="w", pady=(10, 0))

    def create_backup_settings(self, parent):
        section_frame = self.create_section_frame(parent, "Backup Settings")

        # Description label
        description = ctk.CTkLabel(
            section_frame,
            text="Configure automatic backup settings",
            font=self.SUBTITLE_FONT
        )
        description.pack(anchor="w", pady=(0, 15))

        # Auto backup switch
        backup_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        backup_frame.pack(fill="x", pady=(0, 10))

        switch = ctk.CTkSwitch(
            backup_frame,
            text="Enable automatic backup",
            variable=self.controller.auto_backup_var,
            command=self.controller.toggle_auto_backup,
            font=self.SUBTITLE_FONT,
            height=32
        )
        switch.pack(side="left")

        # Backup frequency selection
        frequency_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        frequency_frame.pack(fill="x", pady=(10, 0))

        frequency_label = ctk.CTkLabel(
            frequency_frame,
            text="Backup Frequency:",
            font=self.SUBTITLE_FONT
        )
        frequency_label.pack(side="left", padx=(0, 10))

        frequency_menu = ctk.CTkOptionMenu(
            frequency_frame,
            values=["Daily", "Weekly", "Monthly"],
            variable=self.controller.frequency_var,
            font=self.BUTTON_FONT,
            height=32
        )
        frequency_menu.pack(side="left")

    def create_suspicious_paths_settings(self, parent):
        section_frame = self.create_section_frame(parent, "Suspicious Paths")

        # Description label
        description = ctk.CTkLabel(
            section_frame,
            text="Monitor these paths for suspicious activities",
            font=self.SUBTITLE_FONT
        )
        description.pack(anchor="w", pady=(0, 10))

        # Paths display
        self.paths_text = ctk.CTkTextbox(
            section_frame,
            height=120,
            corner_radius=6
        )
        self.paths_text.pack(fill="x", pady=(0, 10))
        self.update_paths_list()

        # Input frame
        input_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        input_frame.pack(fill="x")

        self.path_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter new suspicious path",
            height=32
        )
        self.path_entry.pack(side="left", fill="x", expand=True)

        ctk.CTkButton(
            input_frame,
            text="Add Path",
            command=self.add_path,
            font=self.BUTTON_FONT,
            width=100,
            height=32
        ).pack(side="left", padx=(10, 0))

    def create_api_connection_settings(self, parent):
        section_frame = self.create_section_frame(parent, "API Connection Settings")

        # Description label
        description = ctk.CTkLabel(
            section_frame,
            text="Configure Wazuh API connection settings",
            font=self.SUBTITLE_FONT
        )
        description.pack(anchor="w", pady=(0, 15))

        # Create input fields with labels
        fields = [
            ("Server URL:", self.controller.wazuh_url, "Enter Wazuh server URL", ""),
            ("Username:", self.controller.wazuh_username, "Enter username", ""),
            ("Password:", self.controller.wazuh_password, "Enter password", "*")
        ]

        for label_text, variable, placeholder, show in fields:
            field_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=(0, 10))

            label = ctk.CTkLabel(
                field_frame,
                text=label_text,
                font=self.SUBTITLE_FONT,
                width=100
            )
            label.pack(side="left")

            entry = ctk.CTkEntry(
                field_frame,
                textvariable=variable,
                placeholder_text=placeholder,
                show=show,
                height=32,
                width=400
            )
            entry.pack(side="left", fill="x", expand=True, padx=(10, 0))

        # Buttons frame
        button_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 0))

        # Left side buttons
        left_buttons_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        left_buttons_frame.pack(side="left")

        ctk.CTkButton(
            left_buttons_frame,
            text="Test Connection",
            command=self.controller.test_connection,
            font=self.BUTTON_FONT,
            height=32,
            width=150
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            left_buttons_frame,
            text="Save Settings",
            command=self.controller.save_settings,
            font=self.BUTTON_FONT,
            height=32,
            width=150
        ).pack(side="left")

        # Reset button on the right
        ctk.CTkButton(
            button_frame,
            text="Reset Wazuh Settings",
            command=self.controller.reset_wazuh_to_default,
            font=self.BUTTON_FONT,
            height=32,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "gray90")
        ).pack(side="right")

    def create_agent_settings(self, parent):
        section_frame = self.create_section_frame(parent, "Agent Settings")

        # Description label
        description = ctk.CTkLabel(
            section_frame,
            text="Configure Wazuh agent connection settings (requires administrator privileges)",
            font=self.SUBTITLE_FONT,
            text_color="red"
        )
        description.pack(anchor="w", pady=(0, 15))

        # Agent IP Configuration
        field_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        field_frame.pack(fill="x", pady=(0, 10))

        label = ctk.CTkLabel(
            field_frame,
            text="Manager IP:",
            font=self.SUBTITLE_FONT,
            width=100
        )
        label.pack(side="left")

        self.agent_ip_entry = ctk.CTkEntry(
            field_frame,
            placeholder_text="Enter Wazuh manager IP",
            height=32,
            width=400
        )
        self.agent_ip_entry.pack(side="left", fill="x", expand=True, padx=(10, 0))

        # Button frame
        button_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 0))

        ctk.CTkButton(
            button_frame,
            text="Update Agent Configuration",
            command=self.controller.update_agent_config,
            font=self.BUTTON_FONT,
            height=32,
            width=200
        ).pack(side="left")

    def create_shuffle_settings(self, parent):
        section_frame = self.create_section_frame(parent, "Shuffle SOAR Settings")

        # Description label
        description = ctk.CTkLabel(
            section_frame,
            text="Configure Shuffle SOAR connection settings",
            font=self.SUBTITLE_FONT
        )
        description.pack(anchor="w", pady=(0, 15))

        # Create input fields with labels
        fields = [
            ("Server URL:", self.controller.shuffle_url, "Enter Shuffle server URL (e.g., http://192.168.1.5:3001)", ""),
            ("API Key:", self.controller.shuffle_api_key, "Enter Shuffle API key", ""),
            ("Workflow Name:", self.controller.shuffle_workflow, "Enter workflow name (e.g., test)", "")
        ]

        for label_text, variable, placeholder, show in fields:
            field_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=(0, 10))

            label = ctk.CTkLabel(
                field_frame,
                text=label_text,
                font=self.SUBTITLE_FONT,
                width=100
            )
            label.pack(side="left")

            entry = ctk.CTkEntry(
                field_frame,
                textvariable=variable,
                placeholder_text=placeholder,
                show=show,
                height=32,
                width=400
            )
            entry.pack(side="left", fill="x", expand=True, padx=(10, 0))

        # Buttons frame
        button_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 0))

        # Left side buttons
        left_buttons_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        left_buttons_frame.pack(side="left")

        ctk.CTkButton(
            left_buttons_frame,
            text="Test Shuffle Connection",
            command=self.controller.test_shuffle_connection,
            font=self.BUTTON_FONT,
            height=32,
            width=150
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            left_buttons_frame,
            text="Save Shuffle Settings",
            command=self.controller.save_shuffle_settings,
            font=self.BUTTON_FONT,
            height=32,
            width=150
        ).pack(side="left")

        # Reset button on the right
        ctk.CTkButton(
            button_frame,
            text="Reset Shuffle Settings",
            command=self.controller.reset_shuffle_to_default,
            font=self.BUTTON_FONT,
            height=32,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "gray90")
        ).pack(side="right")

    def create_section_frame(self, parent, title):
        frame = ctk.CTkFrame(parent, corner_radius=10)
        frame.pack(fill="x", pady=(0, 20), padx=2)

        ctk.CTkLabel(
            frame,
            text=title,
            font=self.SECTION_FONT
        ).pack(anchor="w", pady=(15, 20), padx=15)

        content_frame = ctk.CTkFrame(frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=(0, 15))

        return content_frame

    def update_paths_list(self):
        try:
            print("Updating suspicious paths list...")
            self.paths_text.configure(state="normal")
            self.paths_text.delete("1.0", "end")
            paths = self.controller.get_suspicious_paths()
            self.paths_text.insert("1.0", "\n".join(paths))
            self.paths_text.configure(state="disabled")
            print(f"Updated paths list with {len(paths)} paths")
        except Exception as e:
            print(f"Error updating paths list: {e}")

    def add_path(self):
        try:
            print("Adding new suspicious path...")
            path = self.path_entry.get()
            if path.strip():
                if self.controller.add_suspicious_path(path):
                    print(f"Successfully added path: {path}")
                    self.path_entry.delete(0, "end")
                    self.update_paths_list()
                else:
                    self.show_error("Failed to add path", "The path could not be added. Please try again.")
            else:
                self.show_error("Invalid Path", "Please enter a valid path.")
        except Exception as e:
            self.show_error("Error", f"An error occurred: {str(e)}")

    def show_error(self, title, message):
        ctk.messagebox.showerror(title, message)

    def show_info(self, title, message):
        ctk.messagebox.showinfo(title, message)