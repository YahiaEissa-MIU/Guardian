# views/dashboard_view.py
import customtkinter as ctk
from datetime import datetime
import threading
import time


class DashboardView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.router = parent
        self.controller = None
        self.stat_labels = {}

        self.create_widgets()

        # Start update thread
        self.update_thread = threading.Thread(target=self.update_stats_periodically, daemon=True)
        self.update_thread.start()

    def set_controller(self, controller):
        """Set the controller for this view"""
        self.controller = controller
        # Perform initial update when controller is set
        self.controller.update_dashboard()  # Add this line

    def show_message(self, message, color):
        """Display messages/errors to the user"""
        print(f"{color}: {message}")

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
            {"title": "Active Threats", "color": "#e74c3c"},
            {"title": "Last Scan", "color": "#3498db"},
            {"title": "System Status", "color": "#2ecc71"},
            {"title": "Total Alerts", "color": "#f1c40f"},
        ]

        for i, stat in enumerate(stats):
            row = i // 2
            col = i % 2

            card = ctk.CTkFrame(grid_frame,
                                corner_radius=12,
                                border_width=2,
                                border_color="#ecf0f1",
                                fg_color="#ffffff")
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            card.grid_propagate(False)
            card.pack_propagate(False)

            content_frame = ctk.CTkFrame(card, fg_color="transparent")
            content_frame.pack(expand=True, fill="both", padx=20, pady=20)

            title_label = ctk.CTkLabel(content_frame,
                                       text=stat["title"],
                                       font=("Arial", 16, "bold"),
                                       text_color="#7f8c8d")
            title_label.pack(anchor="w", pady=(0, 5))

            value_label = ctk.CTkLabel(content_frame,
                                       text="Loading...",
                                       font=("Arial", 32, "bold"),
                                       text_color=stat["color"])
            value_label.pack(anchor="w")

            if stat["title"] == "System Status":
                indicator_size = 14
                indicator = ctk.CTkFrame(content_frame,
                                         width=indicator_size,
                                         height=indicator_size,
                                         corner_radius=int(indicator_size / 2),
                                         fg_color=stat["color"])
                indicator.pack(anchor="w", pady=(10, 0))

            # Store the label reference
            self.stat_labels[stat["title"]] = {
                "label": value_label
            }

            # Set consistent card size
            card.configure(width=300, height=180)

    def update_stats(self, dashboard_data):
        """Update all statistics with provided data"""
        try:
            # Update Active Threats
            self.stat_labels["Active Threats"]["label"].configure(
                text=str(dashboard_data["active_threats"]))

            # Update Last Scan - now using the pre-formatted string
            self.stat_labels["Last Scan"]["label"].configure(
                text=dashboard_data["last_scan"])

            # Update System Status
            self.stat_labels["System Status"]["label"].configure(
                text=dashboard_data["system_status"])

            # Update Total Alerts
            self.stat_labels["Total Alerts"]["label"].configure(
                text=str(dashboard_data["total_alerts"]))

        except Exception as e:
            self.show_message(f"Error updating stats: {e}", "red")

    def update_stats_periodically(self):
        """Update stats periodically"""
        while True:
            try:
                if self.controller:
                    self.controller.update_dashboard()
                time.sleep(30)  # Update every 30 seconds
            except Exception as e:
                print(f"Update error: {e}")
                time.sleep(5)  # Short retry delay on error