from tkinter import messagebox
import customtkinter as ctk
from typing import List


class SettingsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.router = parent
        self.controller = None
        self.current_theme = ctk.get_appearance_mode().lower()

        # Define theme colors
        self.colors = {
            "dark": {
                "bg": "#2b2b2b",
                "fg": "#ffffff",
                "label": "#9ba3af",
                "section_bg": "gray17",
                "container_bg": "gray16",
                "accent": "#1f538d",
                "entry_bg": "#333333",
                "entry_fg": "#ffffff",
                "border": "#404040"
            },
            "light": {
                "bg": "#f0f0f0",
                "fg": "#333333",
                "label": "#5b6676",
                "section_bg": "gray85",
                "container_bg": "gray90",
                "accent": "#4a8ede",
                "entry_bg": "#ffffff",
                "entry_fg": "#333333",
                "border": "#d0d0d0"
            }
        }

        # Theme-aware font configuration
        self.fonts = {
            "section": ("JetBrains Mono", 18, "bold"),
            "header": ("JetBrains Mono", 24, "bold"),
            "subtitle": ("JetBrains Mono", 14),
            "label": ("JetBrains Mono", 12),
            "button": ("JetBrains Mono", 12)
        }

        print("SettingsView initialized")

    def set_controller(self, controller):
        self.controller = controller
        self.controller.set_view(self)
        # Update the current theme when controller is set
        self.current_theme = ctk.get_appearance_mode().lower()
        self.create_settings_page()

    def create_settings_page(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Main container with theme-aware styling
        main_container = ctk.CTkFrame(
            self,
            fg_color=self.colors[self.current_theme]["container_bg"],
            corner_radius=15
        )
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        self.create_header(main_container)

        # Scrollable content
        content = ctk.CTkScrollableFrame(
            main_container,
            fg_color="transparent",
            corner_radius=0
        )
        content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Create settings sections
        self.create_api_connection_settings(content)
        self.create_agent_settings(content)
        self.create_shuffle_settings(content)

    def create_header(self, parent):
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)

        title = ctk.CTkLabel(
            header,
            text="Guardian Settings",
            font=self.fonts["header"],
            text_color=self.colors[self.current_theme]["fg"]
        )
        title.pack(anchor="w")

        description = ctk.CTkLabel(
            header,
            text="Configure your security preferences and connections",
            font=self.fonts["subtitle"],
            text_color=self.colors[self.current_theme]["label"]
        )
        description.pack(anchor="w", pady=(5, 0))

    def create_section_frame(self, parent, title, description):
        frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors[self.current_theme]["section_bg"],
            corner_radius=10
        )
        frame.pack(fill="x", pady=(0, 15), padx=2)

        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=15)

        title_label = ctk.CTkLabel(
            header,
            text=title,
            font=self.fonts["section"],
            text_color=self.colors[self.current_theme]["fg"]
        )
        title_label.pack(anchor="w")

        if description:
            desc_label = ctk.CTkLabel(
                header,
                text=description,
                font=self.fonts["subtitle"],
                text_color=self.colors[self.current_theme]["label"]
            )
            desc_label.pack(anchor="w", pady=(5, 0))

        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=(0, 15))

        return content

    def create_api_connection_settings(self, parent):
        content = self.create_section_frame(
            parent,
            "API Connection",
            "Configure Wazuh API connection settings"
        )

        fields = [
            ("Server URL:", self.controller.wazuh_url, "Enter Wazuh server URL"),
            ("Username:", self.controller.wazuh_username, "Enter username"),
            ("Password:", self.controller.wazuh_password, "Enter password", "*")
        ]

        for label_text, variable, placeholder, *show in fields:
            field_frame = ctk.CTkFrame(content, fg_color="transparent")
            field_frame.pack(fill="x", pady=(0, 10))

            label = ctk.CTkLabel(
                field_frame,
                text=label_text,
                font=self.fonts["label"],
                width=100,
                text_color=self.colors[self.current_theme]["fg"]
            )
            label.pack(side="left")

            entry = ctk.CTkEntry(
                field_frame,
                textvariable=variable,
                placeholder_text=placeholder,
                show=show[0] if show else "",
                font=self.fonts["label"],
                height=32,
                fg_color=self.colors[self.current_theme]["entry_bg"],
                text_color=self.colors[self.current_theme]["entry_fg"],
                border_color=self.colors[self.current_theme]["border"]
            )
            entry.pack(side="left", fill="x", expand=True, padx=(10, 0))

        # Button frame with center alignment
        button_frame = ctk.CTkFrame(content, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 0))

        # Center alignment container
        center_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        center_frame.pack(expand=True, fill="x")
        # Configure center frame for center alignment
        center_frame.columnconfigure(0, weight=1)
        center_frame.rowconfigure(0, weight=1)

        save_button = ctk.CTkButton(
            center_frame,
            text="Save Settings",
            command=self.controller.save_settings,
            font=self.fonts["button"],
            height=32,
            width=150,  # Fixed width for better centering
            fg_color=self.colors[self.current_theme]["accent"],
            text_color=self.colors[self.current_theme]["fg"]
        )
        save_button.grid(row=0, column=0)  # Using grid for center alignment

    def create_agent_settings(self, parent):
        content = self.create_section_frame(
            parent,
            "Agent Configuration",
            "Configure Wazuh agent connection settings (requires administrator privileges)"
        )

        field_frame = ctk.CTkFrame(content, fg_color="transparent")
        field_frame.pack(fill="x", pady=(0, 10))

        label = ctk.CTkLabel(
            field_frame,
            text="Manager IP:",
            font=self.fonts["label"],
            width=100,
            text_color=self.colors[self.current_theme]["fg"]
        )
        label.pack(side="left")

        self.agent_ip_entry = ctk.CTkEntry(
            field_frame,
            placeholder_text="Enter Wazuh manager IP",
            font=self.fonts["label"],
            height=32,
            fg_color=self.colors[self.current_theme]["entry_bg"],
            text_color=self.colors[self.current_theme]["entry_fg"],
            border_color=self.colors[self.current_theme]["border"]
        )
        self.agent_ip_entry.pack(side="left", fill="x", expand=True, padx=(10, 0))

        # Button frame with center alignment
        button_frame = ctk.CTkFrame(content, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 0))

        # Center alignment container
        center_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        center_frame.pack(expand=True, fill="x")
        # Configure center frame for center alignment
        center_frame.columnconfigure(0, weight=1)
        center_frame.rowconfigure(0, weight=1)

        update_button = ctk.CTkButton(
            center_frame,
            text="Update Agent Configuration",
            command=self.controller.update_agent_config,
            font=self.fonts["button"],
            height=32,
            width=250,  # Fixed width for better centering
            fg_color=self.colors[self.current_theme]["accent"],
            text_color=self.colors[self.current_theme]["fg"]
        )
        update_button.grid(row=0, column=0)  # Using grid for center alignment

    def get_agent_ip(self):
        """Get the agent IP from the entry field"""
        if hasattr(self, 'agent_ip_entry'):
            return self.agent_ip_entry.get().strip()
        else:
            print("Error: agent_ip_entry not found in SettingsView")
            return None

    def create_shuffle_settings(self, parent):
        content = self.create_section_frame(
            parent,
            "Shuffle SOAR Integration",
            "Configure Shuffle SOAR connection settings"
        )

        fields = [
            ("Server URL:", self.controller.shuffle_url, "Enter Shuffle server URL"),
            ("API Key:", self.controller.shuffle_api_key, "Enter Shuffle API key"),
            ("Workflow:", self.controller.shuffle_workflow, "Enter workflow name")
        ]

        for label_text, variable, placeholder in fields:
            field_frame = ctk.CTkFrame(content, fg_color="transparent")
            field_frame.pack(fill="x", pady=(0, 10))

            label = ctk.CTkLabel(
                field_frame,
                text=label_text,
                font=self.fonts["label"],
                width=100,
                text_color=self.colors[self.current_theme]["fg"]
            )
            label.pack(side="left")

            entry = ctk.CTkEntry(
                field_frame,
                textvariable=variable,
                placeholder_text=placeholder,
                font=self.fonts["label"],
                height=32,
                fg_color=self.colors[self.current_theme]["entry_bg"],
                text_color=self.colors[self.current_theme]["entry_fg"],
                border_color=self.colors[self.current_theme]["border"]
            )
            entry.pack(side="left", fill="x", expand=True, padx=(10, 0))

        # Button frame with center alignment
        button_frame = ctk.CTkFrame(content, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 0))

        # Center alignment container
        center_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        center_frame.pack(expand=True, fill="x")
        # Configure center frame for center alignment
        center_frame.columnconfigure(0, weight=1)
        center_frame.rowconfigure(0, weight=1)

        save_button = ctk.CTkButton(
            center_frame,
            text="Save Settings",
            command=self.controller.save_shuffle_settings,
            font=self.fonts["button"],
            height=32,
            width=150,  # Fixed width for better centering
            fg_color=self.colors[self.current_theme]["accent"],
            text_color=self.colors[self.current_theme]["fg"]
        )
        save_button.grid(row=0, column=0)  # Using grid for center alignment

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def show_info(self, title, message):
        messagebox.showinfo(title, message)