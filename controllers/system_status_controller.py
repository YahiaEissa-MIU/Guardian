import threading
import time


class SystemStatusController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.running = True  # Flag to stop the update loop

    def update_view(self):
        """Continuously fetch metrics and update the view."""
        while self.running:
            metrics = self.model.fetch_metrics()
            self.view.update_metrics(metrics)
            time.sleep(5)  # Refresh every 5 seconds

    def start_updates(self):
        """Start the update loop in a separate thread."""
        update_thread = threading.Thread(target=self.update_view, daemon=True)
        update_thread.start()

    def stop_updates(self):
        """Stop the update loop."""
        self.running = False
