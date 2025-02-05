class AlertsController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self)  # Connect the view to controller

    def get_alerts(self):
        """Returns alerts from the Model"""
        return self.model.get_alerts()

    def acknowledge_alert(self):
        """Handles acknowledging an alert"""
        selected_item = self.view.tree.focus()
        if selected_item:
            index = self.view.tree.index(selected_item)
            self.model.acknowledge_alert(index)
            self.view.update_alerts(self.model.get_alerts())  # Refresh UI
            self.view.details_text.configure(text="Alert acknowledged and removed.")