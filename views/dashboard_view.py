import customtkinter as ctk
from datetime import datetime
import threading
import time


class StatCard(ctk.CTkFrame):
    def __init__(self, parent, title, icon=None, **kwargs):
        # For dark mode, add a subtle gradient-like effect with slightly lighter top
        appearance = ctk.get_appearance_mode()
        if appearance == "dark" and "fg_color" not in kwargs:
            kwargs["fg_color"] = ("#F0F2F5", "#272B30")  # More refined dark color

        # Add a subtle border in dark mode
        if appearance == "dark" and "border_width" not in kwargs:
            kwargs["border_width"] = 1
            kwargs["border_color"] = ("#E1E3E6", "#32363B")  # Slightly lighter than background

        super().__init__(parent, **kwargs)
        self.is_valid = True  # Track validity of widget

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Title with icon
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="ew")

        if icon:
            icon_label = ctk.CTkLabel(title_frame, text=icon, font=("Arial", 20))
            icon_label.pack(side="left", padx=(0, 10))

        title_label = ctk.CTkLabel(
            title_frame,
            text=title,
            font=("Arial", 14, "bold"),
            anchor="w"
        )
        title_label.pack(side="left", fill="x", expand=True)

        # Value with increased prominence
        self.value_label = ctk.CTkLabel(
            self,
            text="--",
            font=("Arial", 26, "bold"),  # Slightly larger for more impact
            anchor="w"
        )
        self.value_label.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")

    def update_value(self, value, color=None):
        """Safely update the card value"""
        try:
            # Check if widget still exists
            if not self.is_valid or not self.winfo_exists():
                return False

            # Check if value_label still exists
            if not hasattr(self, 'value_label') or not self.value_label.winfo_exists():
                return False

            self.value_label.configure(text=str(value))
            if color:
                # Adjust color intensity based on theme
                appearance = ctk.get_appearance_mode()
                self.value_label.configure(text_color=color)
            return True
        except Exception as e:
            print(f"StatCard update error: {e}")
            self.is_valid = False  # Mark as invalid if an error occurs
            return False

    def destroy(self):
        """Override destroy to mark card as invalid"""
        self.is_valid = False
        super().destroy()


class DashboardView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.router = parent
        self.controller = None
        self.stat_cards = {}
        self.is_destroyed = False
        self.view_id = id(self)  # Unique ID for this instance

        print(f"Creating DashboardView with ID: {self.view_id}")

        # Configure grid with specific weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_widgets()

        self.update_thread = threading.Thread(target=self.update_stats_periodically, daemon=True)
        self.update_thread.start()

    def create_widgets(self):
        # Header Section
        self.create_header()

        # Main Content with fixed minimum size
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

        # Configure content grid with equal weights
        self.content_frame.grid_columnconfigure((0, 1), weight=1, uniform="column")
        self.content_frame.grid_rowconfigure((0, 1), weight=1, uniform="row")

        stats_config = [
            {
                "title": "Active Threats",
                "icon": "🛡️",
                "color": "#e74c3c",
                "position": (0, 0)
            },
            {
                "title": "System Status",
                "icon": "⚡",
                "color": "#2ecc71",
                "position": (0, 1)
            },
            {
                "title": "Total Alerts",
                "icon": "🔔",
                "color": "#f1c40f",
                "position": (1, 0)
            },
            {
                "title": "Last Scan",
                "icon": "🔄",
                "color": "#3498db",
                "position": (1, 1)
            }
        ]

        # Create stat cards with minimum size
        for stat in stats_config:
            card_frame = ctk.CTkFrame(
                self.content_frame,
                fg_color="transparent",
            )
            card_frame.grid(
                row=stat["position"][0],
                column=stat["position"][1],
                padx=10,
                pady=10,
                sticky="nsew"
            )

            # Force minimum size for card frame
            card_frame.grid_propagate(False)
            card_frame.configure(width=200, height=150)  # Minimum size

            # Use different fg_color for light/dark modes
            card = StatCard(
                card_frame,
                stat["title"],
                stat["icon"],
                fg_color=("gray90", "gray25"),  # Lighter gray for light mode
                corner_radius=10,
                border_width=1,  # Add border in light mode
                border_color=("gray80", "gray30")  # Border color for light/dark mode
            )
            card.pack(fill="both", expand=True)

            self.stat_cards[stat["title"]] = {
                "card": card,
                "color": stat["color"]
            }

    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        header_frame.grid_columnconfigure(1, weight=1)

        # Title
        ctk.CTkLabel(
            header_frame,
            text="Security Dashboard",
            font=("Arial", 24, "bold")
        ).grid(row=0, column=0, sticky="w")

        # Quick Actions Frame
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=1, sticky="e")

        # Refresh Button
        refresh_btn = ctk.CTkButton(
            actions_frame,
            text="Refresh",
            width=100,
            command=self.safe_refresh
        )
        refresh_btn.pack(side="right", padx=5)

    def safe_refresh(self):
        """Safely call the controller's update method"""
        if not self.is_destroyed and self.controller:
            self.controller.update_dashboard()

    def update_stats(self, dashboard_data):
        """Update all statistics with provided data"""
        if self.is_destroyed:
            print(f"DashboardView {self.view_id}: Can't update, view is destroyed")
            return

        try:
            if not self.winfo_exists():
                print(f"DashboardView {self.view_id}: Widget no longer exists")
                self.is_destroyed = True
                return

            # First check if self.stat_cards still exists
            if not hasattr(self, 'stat_cards'):
                print(f"DashboardView {self.view_id}: stat_cards attribute missing")
                return

            # Now try to update each card safely
            for title, card_info in self.stat_cards.items():
                # Extract the card object
                card = card_info.get("card")
                if not card or not hasattr(card, 'is_valid') or not card.is_valid:
                    continue

                # Get value from dashboard data with reasonable fallback
                key = title.lower().replace(" ", "_")
                value = dashboard_data.get(key, "N/A")

                # Try to update the card
                card.update_value(value, card_info.get("color"))

        except Exception as e:
            print(f"Error updating stats: {e}")
            import traceback
            traceback.print_exc()

    def set_controller(self, controller):
        self.controller = controller
        if self.controller and not self.is_destroyed:
            # Use after() to avoid immediate update issues
            self.after(100, self.controller.update_dashboard)

    def update_stats_periodically(self):
        """Background thread for periodic updates"""
        while True:
            try:
                # Exit thread if view is destroyed
                if self.is_destroyed:
                    print(f"DashboardView {self.view_id}: Exiting update thread (destroyed)")
                    break

                # Only update if controller exists and not destroyed
                if self.controller and not self.is_destroyed:
                    # Queue the update in the main thread to avoid threading issues
                    self.after_idle(self.safe_refresh)

                # Sleep with periodic checks for destruction
                for _ in range(30):  # 30 second sleep in small increments
                    if self.is_destroyed:
                        break
                    time.sleep(1)

            except Exception as e:
                print(f"Update thread error: {e}")
                time.sleep(5)

    def destroy(self):
        """Clean up resources when the view is destroyed"""
        print(f"Destroying DashboardView {self.view_id}")
        self.is_destroyed = True

        # Clean up cards
        if hasattr(self, 'stat_cards'):
            for title, card_info in self.stat_cards.items():
                if 'card' in card_info:
                    card_info['card'].is_valid = False

        # Call the parent's destroy method
        super().destroy()