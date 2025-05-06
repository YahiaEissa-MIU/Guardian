import customtkinter as ctk
from datetime import datetime


class AboutSystemView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_about_system_page()

    def create_about_system_page(self):
        # Main container
        container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Header Section
        self.create_header_section(container)

        # System Information
        self.create_system_info_section(container)

        # Features Section
        self.create_features_section(container)

        # Technical Details
        self.create_technical_section(container)

        # Version History
        self.create_version_section(container)

    def create_header_section(self, parent):
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))

        # Logo or Icon could be added here
        ctk.CTkLabel(
            header,
            text="Guardian 2.0",
            font=("JetBrains Mono", 28, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Advanced Ransomware Detection & Response System",
            font=("JetBrains Mono", 14)
        ).pack(anchor="w", pady=(5, 0))

    def create_system_info_section(self, parent):
        info_frame = self.create_section_frame(parent, "System Information")

        info_data = {
            "Version": "2.0.0",
            "Build Date": datetime.now().strftime("%B %d, %Y"),
            "Platform": "Windows 10/11",
            "Architecture": "64-bit",
            "UI Framework": "CustomTkinter 5.2.0"
        }

        for key, value in info_data.items():
            self.create_info_row(info_frame, key, value)

    def create_features_section(self, parent):
        features_frame = self.create_section_frame(parent, "Core Features")

        features = [
            {
                "title": "Real-time Protection",
                "desc": "Continuous monitoring and instant response to potential ransomware threats"
            },
            {
                "title": "Automated Response",
                "desc": "Immediate threat containment and system isolation capabilities"
            },
            {
                "title": "Secure Backup Integration",
                "desc": "Automated backup system with versioning and quick restore options"
            }
        ]

        for feature in features:
            self.create_feature_card(features_frame, feature)

    def create_technical_section(self, parent):
        tech_frame = self.create_section_frame(parent, "Technical Specifications")

        specs = {
            "Response Time": "< 100ms average",
            "Memory Usage": "50MB - 150MB",
            "CPU Impact": "< 3% in idle state"
        }

        for key, value in specs.items():
            self.create_info_row(tech_frame, key, value)

    def create_version_section(self, parent):
        version_frame = self.create_section_frame(parent, "Version History")

        versions = [
            {
                "version": "2.0.0",
                "date": "March 2024",
                "changes": [
                    "Complete UI/UX revamp",
                    "Enhanced detection engine",
                    "Improved response automation",
                    "New dashboard analytics"
                ]
            },
            {
                "version": "1.1.0",
                "date": "January 2024",
                "changes": [
                    "Performance optimizations",
                    "Additional threat patterns",
                    "Bug fixes and improvements"
                ]
            }
        ]

        for version in versions:
            self.create_version_card(version_frame, version)

    def create_section_frame(self, parent, title):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            frame,
            text=title,
            font=("JetBrains Mono", 16, "bold")
        ).pack(anchor="w", padx=15, pady=10)

        return frame

    def create_info_row(self, parent, key, value):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=2)

        ctk.CTkLabel(
            row,
            text=key,
            font=("JetBrains Mono", 12, "bold"),
            width=150
        ).pack(side="left")

        ctk.CTkLabel(
            row,
            text=str(value),
            font=("JetBrains Mono", 12)
        ).pack(side="left")

    def create_feature_card(self, parent, feature):
        card = ctk.CTkFrame(parent)
        card.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            card,
            text=feature["title"],
            font=("JetBrains Mono", 12, "bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        ctk.CTkLabel(
            card,
            text=feature["desc"],
            font=("JetBrains Mono", 11),
            wraplength=800,
            justify="left"
        ).pack(anchor="w", padx=10, pady=(0, 10))

    def create_version_card(self, parent, version):
        card = ctk.CTkFrame(parent)
        card.pack(fill="x", padx=15, pady=5)

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            header,
            text=f"Version {version['version']}",
            font=("JetBrains Mono", 12, "bold")
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text=version['date'],
            font=("JetBrains Mono", 11),
            text_color="gray"
        ).pack(side="right")

        for change in version['changes']:
            ctk.CTkLabel(
                card,
                text=f"• {change}",
                font=("JetBrains Mono", 11),
                justify="left"
            ).pack(anchor="w", padx=10, pady=2)