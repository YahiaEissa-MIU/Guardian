import customtkinter as ctk


class AboutSystemView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.router = parent
        self.create_about_system_page()

    def create_about_system_page(self):
        # Clear the main content frame
        for widget in self.winfo_children():
            widget.destroy()

        # Create a scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(self, width=1000, height=600, corner_radius=10)
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        title_label = ctk.CTkLabel(scrollable_frame, text="About System", font=("Arial", 20, "bold"))
        title_label.pack(pady=20)

        # Purpose Frame
        purpose_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
        purpose_frame.pack(fill="x", padx=20, pady=10)

        purpose_label = ctk.CTkLabel(purpose_frame, text="Purpose", font=("Arial", 16, "bold"))
        purpose_label.pack(pady=10, padx=10, anchor="w")

        purpose_content = [
            {"title": "Automated Detection and Response:",
             "text": "Automates identification, containment, and recovery from ransomware attacks, minimizing manual intervention and reducing recovery time."},
            {"title": "Enhancing Personal Cybersecurity:",
             "text": "Equips users with strong cybersecurity tools, typically accessible to large organizations, enhancing defense against advanced threats."},
            {"title": "User-Friendly Interface:",
             "text": "Designed for users without technical expertise, the application delivers clear, actionable alerts and instructions."},
            {"title": "Continuous Threat Intelligence:",
             "text": "Incorporates real-time threat intelligence feeds for up-to-date detection of ransomware variants."},
            {"title": "Cost-Effective Solution:",
             "text": "Provides an affordable cybersecurity solution targeted at individuals and small businesses."},
        ]

        for item in purpose_content:
            ctk.CTkLabel(purpose_frame, text=item["title"], font=("Arial", 12, "bold")).pack(anchor="w", padx=10,
                                                                                             pady=(5, 0))
            ctk.CTkLabel(purpose_frame, text=item["text"], font=("Arial", 12), wraplength=900, justify="left").pack(
                anchor="w", padx=10, pady=(0, 10))

        # Overview Frame
        overview_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
        overview_frame.pack(fill="x", padx=20, pady=10)

        overview_label = ctk.CTkLabel(overview_frame, text="Overview of Guardian's Objectives",
                                      font=("Arial", 16, "bold"))
        overview_label.pack(pady=10, padx=10, anchor="w")

        overview_content = [
            {"title": "Objective 1",
             "text": "The application is a desktop interface designed for end-users."},
            {"title": "Objective 2",
             "text": "Integration: It integrates with Splunk Security Information and Event Management (SIEM) system and utilizes a customized Security Orchestration, Automation, and Response (SOAR) solution."},
            {"title": "Objective 3",
             "text": "Functionality: The application will provide real-time alerts, enable isolation of infected files, and facilitate automated recovery processes."},
        ]

        for item in overview_content:
            ctk.CTkLabel(overview_frame, text=item["title"], font=("Arial", 12, "bold")).pack(anchor="w", padx=10,
                                                                                              pady=(5, 0))
            ctk.CTkLabel(overview_frame, text=item["text"], font=("Arial", 12), wraplength=900, justify="left").pack(
                anchor="w", padx=10, pady=(0, 10))

        # Developers & Contributors Section
        developers_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
        developers_frame.pack(fill="x", padx=20, pady=10)

        developers_label = ctk.CTkLabel(developers_frame, text="Developers", font=("Arial", 16, "bold"))
        developers_label.pack(pady=10, padx=10, anchor="w")

        developers_content = [
            {"title": "Lead Developer", "text": "Yahia Eissa"},
            {"title": "Contributor", "text": "Nada Abdelrahman"},
            {"title": "Contributor", "text": "Donya Hany"},
            {"title": "Contributor", "text": "Abdelrahman Walid"},
            {"title": "Contributor", "text": "Ali Ahmed"},
        ]

        for item in developers_content:
            ctk.CTkLabel(developers_frame, text=item["title"], font=("Arial", 12, "bold")).pack(anchor="w", padx=10,
                                                                                                pady=(5, 0))
            ctk.CTkLabel(developers_frame, text=item["text"], font=("Arial", 12), wraplength=900, justify="left").pack(
                anchor="w", padx=10, pady=(0, 10))

        # Version Information Section
        version_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
        version_frame.pack(fill="x", padx=20, pady=10)

        version_label = ctk.CTkLabel(version_frame, text="Versions", font=("Arial", 16, "bold"))
        version_label.pack(pady=10, padx=10, anchor="w")

        version_content = [
            {"title": "Version 1.0",
             "text": "Released on November 9, 2024 - This version outlined the specifications for the initial proposal."},
            {"title": "Version 1.1",
             "text": "Released on January 10, 2025 - This version incorporated updates to the project's scope."},
        ]

        for item in version_content:
            ctk.CTkLabel(version_frame, text=item["title"], font=("Arial", 12, "bold")).pack(anchor="w", padx=10,
                                                                                             pady=(5, 0))
            ctk.CTkLabel(version_frame, text=item["text"], font=("Arial", 12), wraplength=900, justify="left").pack(
                anchor="w", padx=10, pady=(0, 10))
