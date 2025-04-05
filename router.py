from controllers.system_status_controller import SystemStatusController
from models.system_status_model import SystemStatusModel
from views.dashboard_view import DashboardView
from controllers.dashboard_controller import DashboardController
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
        self.alert_model = AlertModel()
        self.incident_history_model = IncidentHistoryModel()

        # Initialize the settings controller first as it's needed for configuration
        self.settings_controller = SettingsController()
        # Controllers will be initialized when their views are created
        self.alerts_controller = None
        self.dashboard_controller = None

    def register(self, name, view_class, controller=None):
        """Register a view by name if not already registered."""
        if name not in self.views:
            if controller:
                self.views[name] = view_class(self.root.main_content_frame, controller)
            else:
                self.views[name] = view_class(self.root.main_content_frame)

            self.views[name].grid(row=0, column=0, sticky="nsew")

    def show(self, name):
        """Show the requested view and hide others."""
        for view in self.views.values():
            view.grid_forget()

        if name not in self.views:
            if name == "dashboard":
                view = DashboardView(self.root.main_content_frame)
                self.dashboard_controller = DashboardController(view)
                view.set_controller(self.dashboard_controller)
                self.views[name] = view
                # Add observer for settings changes
                self.settings_controller.add_observer(self.dashboard_controller.on_config_change)

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
                view = SettingsView(self.root.main_content_frame, self.settings_controller)
                self.views[name] = view

            elif name == "alerts":
                view = AlertsView(self.root.main_content_frame)
                self.alerts_controller = AlertsController(view)
                view.set_controller(self.alerts_controller)
                self.views[name] = view
                # Add observer for settings changes
                self.settings_controller.add_observer(self.alerts_controller.on_config_change)

            elif name == "about_system":
                self.register(name, AboutSystemView)

            elif name == "contact_us":
                view = ContactView(self.root.main_content_frame)
                controller = ContactController(view)
                view.set_controller(controller)
                self.views[name] = view

        self.views[name].grid(row=0, column=0, sticky="nsew")

        # Update views that need refreshing when shown
        if name == "dashboard" and self.dashboard_controller:
            self.dashboard_controller.update_dashboard()