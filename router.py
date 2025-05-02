from typing import Dict, Optional, Type
import logging
from dataclasses import dataclass

from controllers import (
    SystemStatusController, DashboardController, IncidentHistoryController,
    SettingsController, AlertsController, ContactController
)
from models import SystemStatusModel, IncidentHistoryModel, WazuhConfig
from utils.alert_manager import AlertManager
from views import (
    DashboardView, SystemStatusView, IncidentHistoryView, SettingsView,
    AlertsView, ContactView, AboutSystemView
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ViewConfiguration:
    """Configuration for a view including its dependencies"""
    view_class: Type
    controller_class: Optional[Type] = None
    model_class: Optional[Type] = None
    needs_refresh: bool = False
    observes_settings: bool = False


class Router:
    """Router for managing application views and their dependencies"""

    # Define view configurations
    VIEW_CONFIGS = {
        "dashboard": ViewConfiguration(
            view_class=DashboardView,
            controller_class=DashboardController,
            needs_refresh=True,
            observes_settings=True
        ),
        "system_status": ViewConfiguration(
            view_class=SystemStatusView,
            controller_class=SystemStatusController,
            model_class=SystemStatusModel
        ),
        "incident_history": ViewConfiguration(
            view_class=IncidentHistoryView,
            controller_class=IncidentHistoryController,
            model_class=IncidentHistoryModel
        ),
        "settings": ViewConfiguration(
            view_class=SettingsView,
            controller_class=SettingsController
        ),
        "alerts": ViewConfiguration(
            view_class=AlertsView,
            controller_class=AlertsController,
            observes_settings=True
        ),
        "about_system": ViewConfiguration(
            view_class=AboutSystemView
        ),
        "contact_us": ViewConfiguration(
            view_class=ContactView,
            controller_class=ContactController
        )
    }

    def __init__(self, root):
        """Initialize router with root window"""
        self.root = root
        self.views: Dict = {}
        self.controllers: Dict = {}
        self.models: Dict = {}

        # Initialize AlertManager
        AlertManager().load_acknowledged_alerts()

        # Initialize core components
        self.initialize_core_components()
        logger.info("Router initialized")

    def initialize_core_components(self):
        """Initialize essential models and controllers"""
        try:
            # Initialize settings controller first
            self.settings_controller = SettingsController()
            self.controllers['settings'] = self.settings_controller

            # Initialize core models
            self.models['system_status'] = SystemStatusModel()
            self.models['incident_history'] = IncidentHistoryModel()

            logger.info("Core components initialized")
        except Exception as e:
            logger.error(f"Error initializing core components: {e}")
            raise

    def create_view(self, name: str) -> None:
        try:
            config = self.VIEW_CONFIGS.get(name)
            if not config:
                logger.error(f"No configuration found for view: {name}")
                return

            # Create model if specified
            model = None
            if config.model_class:
                model = self.models.get(name) or config.model_class()
                self.models[name] = model

            # Create controller
            controller = None
            if config.controller_class:
                if name == "settings":
                    controller = self.settings_controller
                elif model:
                    controller = config.controller_class(model)
                else:
                    controller = config.controller_class()
                self.controllers[name] = controller

            # Create view
            view = config.view_class(self.root.main_content_frame)
            self.views[name] = view

            # Set up view-controller relationship
            if controller:
                view.set_controller(controller)
                controller.set_view(view)

            # Add settings observer if needed
            if config.observes_settings and controller:
                self.settings_controller.add_observer(controller.on_config_change)

            logger.info(f"Created view: {name}")

        except Exception as e:
            logger.error(f"Error creating view {name}: {e}")
            raise

    def show(self, name: str) -> None:
        try:
            # Hide all current views
            for view in self.views.values():
                view.grid_forget()

            # Create view if it doesn't exist
            if name not in self.views:
                self.create_view(name)

            # Show the requested view
            self.views[name].grid(row=0, column=0, sticky="nsew")

            # Refresh view if needed
            config = self.VIEW_CONFIGS.get(name)
            if config and config.needs_refresh:
                controller = self.controllers.get(name)
                if controller and hasattr(controller, 'update_dashboard'):
                    # Make sure view is set before updating
                    if not controller.view:
                        controller.set_view(self.views[name])
                    controller.update_dashboard()

            logger.info(f"Showed view: {name}")

        except Exception as e:
            logger.error(f"Error showing view {name}: {e}")
            raise

    def cleanup(self):
        """Cleanup resources when closing the application"""
        try:
            for controller in self.controllers.values():
                if hasattr(controller, 'cleanup'):
                    controller.cleanup()
            logger.info("Router cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")