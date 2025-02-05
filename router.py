from controllers.system_status_controller import SystemStatusController
from models.system_status_model import SystemStatusModel
from views.dashboard_view import DashboardView
from views.system_status_view import SystemStatusView
from views.incident_history_view import IncidentHistoryView
from models.incident_history_model import IncidentHistoryModel
from controllers.incident_history_controller import IncidentHistoryController
from views.settings_view import SettingsView
from controllers.settings_controller import SettingsController
from views.alerts_view import AlertsView
from models.alert_model import AlertModel
from controllers.alerts_controller import AlertsController
from views.about_system_view import AboutSystemView
from views.contact_us_view import ContactView
from controllers.contact_controller import ContactController


class Router:
    def __init__(self, root):
        self.system_status_model = SystemStatusModel()
        self.root = root
        self.views = {}
        self.alert_model = AlertModel()  # Create an instance of AlertModel
        self.incident_history_model = IncidentHistoryModel()

    def register(self, name, view_class, controller=None):
        """Register a view by name if not already registered."""
        if name not in self.views:
            if controller:
                self.views[name] = view_class(self.root.main_content_frame, controller)
            else:
                self.views[name] = view_class(self.root.main_content_frame)

            # Use grid() instead of place()
            self.views[name].grid(row=0, column=0, sticky="nsew")

    def show(self, name):
        """Show the requested view and hide others."""
        for view in self.views.values():
            view.grid_forget()  # Hide all views

        if name not in self.views:
            if name == "dashboard":
                self.register(name, DashboardView)
            elif name == "system_status":
                model = self.system_status_model
                view = SystemStatusView(self.root.main_content_frame, None)
                controller = SystemStatusController(model, view)
                view.set_controller(controller)
                self.views[name] = view
            elif name == "incident_history":
                model = self.incident_history_model
                view = IncidentHistoryView(self.root.main_content_frame, None)
                controller = IncidentHistoryController(model, view)
                view.set_controller(controller)
                self.views[name] = view
            elif name == "settings":
                controller = SettingsController()
                view = SettingsView(self.root.main_content_frame, controller)
                self.views[name] = view
            elif name == "alerts":
                model = self.alert_model
                view = AlertsView(self.root.main_content_frame, None)
                controller = AlertsController(model, view)
                view.set_controller(controller)
                self.views[name] = view
            elif name == "about_system":
                self.register(name, AboutSystemView)
            elif name == "contact_us":
                view = ContactView(self.root.main_content_frame)
                controller = ContactController(view)
                view.set_controller(controller)
                self.views[name] = view

        # Instead of `place`, use `grid()`
        self.views[name].grid(row=0, column=0, sticky="nsew")
