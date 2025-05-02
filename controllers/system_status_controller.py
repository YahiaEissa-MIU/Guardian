# system_status_controller.py
import threading
import time
import logging


class SystemStatusController:
    def __init__(self, model):
        self.model = model
        self.view = None
        self.running = True
        self._update_thread = None
        logging.info("SystemStatusController initialized with model")

    def set_view(self, view):
        self.view = view
        logging.info("View set for SystemStatusController")
        self.start_updates()

    def update_view(self):
        """Continuously fetch metrics and update the view."""
        while self.running:
            try:
                if self.model and self.view:
                    metrics = self.model.fetch_metrics()
                    # Use after() to update GUI from this thread safely
                    self.view.after(0, self.view.update_metrics, metrics)
                time.sleep(5)  # Refresh every 5 seconds
            except Exception as e:
                logging.error(f"Error in update_view: {str(e)}")
                # If there's an error, wait before trying again
                time.sleep(5)

    def start_updates(self):
        """Start the update loop in a separate thread."""
        if not self.view:
            logging.error("Cannot start updates: View not set")
            return

        try:
            if not self._update_thread or not self._update_thread.is_alive():
                self.running = True
                self._update_thread = threading.Thread(target=self.update_view, daemon=True)
                self._update_thread.start()
                logging.info("Started system status update thread")
        except Exception as e:
            logging.error(f"Error starting updates: {str(e)}")

    def stop_updates(self):
        """Stop the update loop."""
        try:
            self.running = False
            if self._update_thread and self._update_thread.is_alive():
                self._update_thread.join(timeout=1.0)
                logging.info("Stopped system status updates")
        except Exception as e:
            logging.error(f"Error stopping updates: {str(e)}")

    def cleanup(self):
        """Cleanup resources when closing."""
        self.stop_updates()
