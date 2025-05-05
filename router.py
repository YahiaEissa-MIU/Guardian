from typing import Dict, Optional, Type
import logging
import os
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
def setup_debug_logging():
    log_dir = os.path.join(os.environ['APPDATA'], 'Guardian', 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Configure file handler for debug logging
    debug_logger = logging.getLogger('guardian_debug')
    debug_logger.setLevel(logging.DEBUG)

    log_file = os.path.join(log_dir, 'sync_debug.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(message)s'))
    debug_logger.addHandler(file_handler)

    return debug_logger


# Initialize loggers
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
debug_logger = setup_debug_logging()


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
            needs_refresh=True,  # Add this
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
            debug_logger.info(f"=== Router Show: {name} ===")
            debug_logger.info(f"Controller exists: {name in self.controllers}")
            debug_logger.info(f"View exists: {name in self.views}")

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
            debug_logger.info(f"Needs refresh: {config.needs_refresh if config else None}")

            if config and config.needs_refresh:
                controller = self.controllers.get(name)
                if controller:
                    # Make sure view is set before updating
                    if not controller.view:
                        controller.set_view(self.views[name])

                    # Call appropriate update method based on controller type
                    if isinstance(controller, DashboardController):
                        debug_logger.info("Calling dashboard update")
                        controller.update_dashboard()
                    elif isinstance(controller, AlertsController):
                        debug_logger.info("Calling alerts update")
                        controller.update_alerts()

            logger.info(f"Showed view: {name}")

        except Exception as e:
            error_msg = f"Error showing view {name}: {e}"
            logger.error(error_msg)
            debug_logger.error(error_msg)
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
