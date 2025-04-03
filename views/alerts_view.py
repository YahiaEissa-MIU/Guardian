# alerts_view.py
from tkinter import ttk
import customtkinter as ctk
import threading
import time


class AlertsView(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        print("Initializing AlertsView...")  # Debug print
        super().__init__(parent)
        self.controller = None
        self.tree = None
        self.details_text = None
        self.update_thread = None
        self.running = True

        if controller:
            self.set_controller(controller)
        else:
            self.create_loading_state()

    def create_loading_state(self):
        """Temporary UI until controller is set"""
        print("Creating loading state...")  # Debug print
        for widget in self.winfo_children():
            widget.destroy()

        loading_label = ctk.CTkLabel(self, text="Loading alerts...")
        loading_label.pack(pady=50)

    def set_controller(self, controller):
        """Finalize initialization when controller is available"""
        print("Setting controller and initializing view...")  # Debug print
        self.controller = controller
        self.show_alerts_page()
        self.start_periodic_updates()

    def start_periodic_updates(self):
        """Start the periodic updates thread"""
        print("Starting periodic updates thread...")  # Debug print
        if not self.update_thread:
            self.update_thread = threading.Thread(target=self.update_alerts_periodically, daemon=True)
            self.update_thread.start()

    def show_alerts_page(self):
        """Create full UI after controller is set"""
        print("Initializing alerts page...")  # Debug print

        try:
            # Clear existing widgets
            for widget in self.winfo_children():
                widget.destroy()

            # Title and Header Frame
            header_frame = ctk.CTkFrame(self, fg_color="transparent")
            header_frame.pack(fill="x", padx=20, pady=(20, 10))

            title_label = ctk.CTkLabel(
                header_frame,
                text="Security Alerts",
                font=("Arial", 24, "bold")
            )
            title_label.pack(side="left")

            # Buttons frame
            buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
            buttons_frame.pack(side="right")

            acknowledge_button = ctk.CTkButton(
                buttons_frame,
                text="Acknowledge Alert",
                command=self.acknowledge_alert,
                width=120
            )
            acknowledge_button.pack(side="right", padx=(10, 0))

            refresh_button = ctk.CTkButton(
                buttons_frame,
                text="Refresh",
                command=self.refresh_alerts,
                width=100
            )
            refresh_button.pack(side="right")

            # Main content frame
            content_frame = ctk.CTkFrame(self)
            content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

            # Treeview Frame
            tree_frame = ctk.CTkFrame(content_frame)
            tree_frame.pack(fill="both", expand=True, pady=(0, 10))

            # Initialize Treeview
            self.tree = ttk.Treeview(
                tree_frame,
                columns=("Timestamp", "Level", "Description", "Location"),
                show="headings",
                height=15
            )

            # Configure scrollbar
            scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=scrollbar.set)

            # Configure columns
            self.tree.heading("Timestamp", text="Timestamp", anchor="center")
            self.tree.heading("Level", text="Level", anchor="center")
            self.tree.heading("Description", text="Description", anchor="w")
            self.tree.heading("Location", text="Location", anchor="w")

            self.tree.column("Timestamp", width=150, anchor="center")
            self.tree.column("Level", width=80, anchor="center")
            self.tree.column("Description", width=400, anchor="w")
            self.tree.column("Location", width=200, anchor="w")

            # Pack Treeview and scrollbar
            self.tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Details Frame
            details_frame = ctk.CTkFrame(content_frame)
            details_frame.pack(fill="x", pady=(10, 0))

            details_label = ctk.CTkLabel(
                details_frame,
                text="Alert Details",
                font=("Arial", 16, "bold")
            )
            details_label.pack(anchor="w", padx=10, pady=(10, 5))

            self.details_text = ctk.CTkTextbox(
                details_frame,
                height=100,
                wrap="word"
            )
            self.details_text.pack(fill="x", padx=10, pady=(0, 10))
            self.details_text.insert("1.0", "Select an alert to view details")
            self.details_text.configure(state="disabled")

            # Bind selection event
            self.tree.bind("<<TreeviewSelect>>", self.on_select)

            print("UI initialization complete")  # Debug print

            # Initial load of alerts
            self.refresh_alerts()

        except Exception as e:
            print(f"Error initializing UI: {e}")  # Debug print
            self.create_loading_state()

    def acknowledge_alert(self):
        """Handle alert acknowledgment"""
        print("Attempting to acknowledge alert...")  # Debug print
        if self.controller:
            self.controller.acknowledge_alert()
        else:
            print("Controller not available for acknowledgment")  # Debug print

    def update_alerts(self, alerts):
        """Update the treeview with new alerts"""
        print(f"Updating alerts view with {len(alerts)} alerts")  # Debug print
        if self.tree is None:
            print("Tree view not initialized!")  # Debug print
            return

        try:
            self.tree.delete(*self.tree.get_children())
            for alert in alerts:
                print(f"Adding alert: {alert}")  # Debug print
                self.tree.insert("", "end", values=(
                    alert["timestamp"],
                    alert["actions"],
                    alert["type"],
                    alert["file"]
                ))
        except Exception as e:
            print(f"Error updating alerts: {e}")  # Debug print

    def refresh_alerts(self):
        """Manually refresh alerts"""
        print("Manually refreshing alerts...")  # Debug print
        if self.controller:
            alerts = self.controller.get_alerts()
            print(f"Received {len(alerts)} alerts from controller")  # Debug print
            self.update_alerts(alerts)
        else:
            print("Controller not initialized")  # Debug print

    def update_alerts_periodically(self):
        """Update alerts every 30 seconds"""
        print("Starting periodic updates")  # Debug print
        while self.running:
            try:
                if self.controller and self.tree:  # Check if tree exists
                    print("Performing periodic update...")  # Debug print
                    self.refresh_alerts()
                time.sleep(30)
            except Exception as e:
                print(f"Error in periodic update: {e}")  # Debug print
                time.sleep(30)  # Still wait before next attempt

    def on_select(self, event):
        """Handle alert selection"""
        print("Alert selected")  # Debug print
        selected_item = self.tree.focus()
        if not selected_item:
            print("No item selected")  # Debug print
            return

        values = self.tree.item(selected_item)['values']
        if not values:
            print("No values for selected item")  # Debug print
            return

        print(f"Selected alert details: {values}")  # Debug print
        self.details_text.configure(state="normal")
        self.details_text.delete("1.0", "end")
        details = (
            f"Timestamp: {values[0]}\n"
            f"Alert Level: {values[1]}\n"
            f"Description: {values[2]}\n"
            f"Location: {values[3]}\n"
        )
        self.details_text.insert("1.0", details)
        self.details_text.configure(state="disabled")

    def destroy(self):
        """Clean up when the view is destroyed"""
        print("Cleaning up alerts view...")  # Debug print
        self.running = False
        if self.update_thread:
            self.update_thread.join(timeout=1)
        super().destroy()