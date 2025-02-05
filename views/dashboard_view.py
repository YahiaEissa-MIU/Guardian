import customtkinter as ctk


class DashboardView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.router = parent

        self.create_widgets()

    def create_widgets(self):
        # Dashboard Title
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(pady=(20, 15), fill="x")

        ctk.CTkLabel(title_frame,
                     text="Security Dashboard",
                     font=("Arial", 28, "bold"),
                     text_color="white").pack()

        # Stats Grid
        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Configure grid layout
        grid_frame.grid_rowconfigure(0, weight=1)
        grid_frame.grid_rowconfigure(1, weight=1)
        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(1, weight=1)

        stats = [
            {"title": "Active Threats", "value": "0", "color": "#e74c3c"},
            {"title": "Last Scan", "value": "2 hours ago", "color": "#3498db"},
            {"title": "System Status", "value": "Secure", "color": "#2ecc71"},
            {"title": "Total Alerts", "value": "5", "color": "#f1c40f"},
        ]

        for i, stat in enumerate(stats):
            row = i // 2
            col = i % 2

            # Card Frame with integer corner radius
            card = ctk.CTkFrame(grid_frame,
                                corner_radius=12,  # Integer value
                                border_width=2,
                                border_color="#ecf0f1",
                                fg_color="#ffffff")
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            card.grid_propagate(False)
            card.pack_propagate(False)

            # Card Content
            content_frame = ctk.CTkFrame(card, fg_color="transparent")
            content_frame.pack(expand=True, fill="both", padx=20, pady=20)

            # Title Section
            title_label = ctk.CTkLabel(content_frame,
                                       text=stat["title"],
                                       font=("Arial", 16, "bold"),
                                       text_color="#7f8c8d")
            title_label.pack(anchor="w", pady=(0, 5))

            # Value Display
            value_label = ctk.CTkLabel(content_frame,
                                       text=stat["value"],
                                       font=("Arial", 32, "bold"),
                                       text_color=stat["color"])
            value_label.pack(anchor="w")

            # Status Indicator with integer corner radius
            if stat["title"] == "System Status":
                indicator_size = 14
                indicator = ctk.CTkFrame(content_frame,
                                         width=indicator_size,
                                         height=indicator_size,
                                         corner_radius=int(indicator_size / 2),  # Convert to integer
                                         fg_color=stat["color"])
                indicator.pack(anchor="w", pady=(10, 0))

        # Set consistent card size
        for child in grid_frame.winfo_children():
            if isinstance(child, ctk.CTkFrame):
                child.configure(width=300, height=180)
