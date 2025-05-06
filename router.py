from typing import Dict, Optional, Type
import logging
import os
from dataclasses import dataclass

from controllers import (
    DashboardController, IncidentHistoryController,
    SettingsController, AlertsController
)
from models import IncidentHistoryModel, WazuhConfig
from utils.alert_manager import AlertManager
from utils.config_manager import ConfigManager
from views import (
    DashboardView, IncidentHistoryView, SettingsView,
    AlertsView, AboutSystemView
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
        "incident_history": ViewConfiguration(
            view_class=IncidentHistoryView,
            controller_class=IncidentHistoryController,
            model_class=IncidentHistoryModel,
            observes_settings=True  # Add this flag
        ),
        "settings": ViewConfiguration(
            view_class=SettingsView,
            controller_class=SettingsController
        ),
        "alerts": ViewConfiguration(
            view_class=AlertsView,
            controller_class=AlertsController,
            needs_refresh=True,
            observes_settings=True
        ),
        "about_system": ViewConfiguration(
            view_class=AboutSystemView
        )
    }

    def __init__(self, root):
        """Initialize router with root window"""
        self.root = root
        self.views: Dict = {}
        self.controllers: Dict = {}
        self.models: Dict = {}

        # Initialize ConfigManager early to ensure it's available to all components
        self.config_manager = ConfigManager()
        debug_logger.info("ConfigManager initialized")

        # Load and verify configurations
        self.verify_configurations()

        # Initialize AlertManager
        AlertManager().load_acknowledged_alerts()

        # Initialize core components
        self.initialize_core_components()
        logger.info("Router initialized")

        # Ensure observers are properly registered
        self.register_configuration_observers()

    def verify_configurations(self):
        """Verify all configurations are properly loaded at startup"""
        try:
            # Get current configurations
            wazuh_config = self.config_manager.get_wazuh_config()
            shuffle_config = self.config_manager.get_shuffle_config()

            # Log current configuration state
            debug_logger.info("=== Configuration Verification ===")
            debug_logger.info(f"Wazuh configured: {wazuh_config.is_configured}")
            if wazuh_config.is_configured:
                debug_logger.info(f"Wazuh URL: {wazuh_config.url}")
                debug_logger.info(f"Wazuh username: {wazuh_config.username}")
                debug_logger.info(
                    f"Wazuh password length: {len(wazuh_config.password) if wazuh_config.password else 0}")

            debug_logger.info(f"Shuffle configured: {shuffle_config.is_configured}")
            if shuffle_config.is_configured:
                debug_logger.info(f"Shuffle URL: {shuffle_config.shuffle_url}")

        except Exception as e:
            debug_logger.error(f"Error during configuration verification: {e}")
            import traceback
            debug_logger.error(traceback.format_exc())

    def register_configuration_observers(self):
        """Register all controllers that need to observe configuration changes"""
        try:
            debug_logger.info("Registering configuration observers...")

            # Register DashboardController if it exists
            if 'dashboard' in self.controllers:
                controller = self.controllers['dashboard']
                self.config_manager.add_wazuh_observer(controller.on_config_change)
                debug_logger.info(f"Added Wazuh observer: {controller.on_config_change}")

            # Register AlertsController if it exists
            if 'alerts' in self.controllers:
                controller = self.controllers['alerts']
                self.config_manager.add_wazuh_observer(controller.on_config_change)
                debug_logger.info(f"Added Wazuh observer: {controller.on_config_change}")

                # Register IncidentHistoryController if it exists
            if 'incident_history' in self.controllers:
                controller = self.controllers['incident_history']
                self.config_manager.add_shuffle_observer(controller.on_config_change)
                debug_logger.info(f"Added Shuffle observer: {controller.on_config_change}")

        except Exception as e:
            debug_logger.error(f"Error registering configuration observers: {e}")

    def initialize_core_components(self):
        """Initialize essential models and controllers"""
        try:
            # Initialize settings controller first, providing the ConfigManager
            self.settings_controller = SettingsController()
            self.controllers['settings'] = self.settings_controller

            # Initialize DashboardController early to ensure it's registered for config updates
            self.controllers['dashboard'] = DashboardController()

            # Initialize AlertsController early for the same reason
            self.controllers['alerts'] = AlertsController()

            # Initialize core models
            self.models['incident_history'] = IncidentHistoryModel()

            logger.info("Core components initialized")

            # Ensure controllers have the current configuration
            self.sync_controllers_with_config()

        except Exception as e:
            logger.error(f"Error initializing core components: {e}")
            debug_logger.error(f"Error initializing core components: {e}")
            import traceback
            debug_logger.error(traceback.format_exc())
            raise

    def sync_controllers_with_config(self):
        """Ensure all controllers have the latest configuration"""
        try:
            wazuh_config = self.config_manager.get_wazuh_config()

            # Update settings controller
            if 'settings' in self.controllers:
                controller = self.controllers['settings']
                if hasattr(controller, 'wazuh_config'):
                    controller.wazuh_config = wazuh_config
                if hasattr(controller, 'wazuh_url'):
                    controller.wazuh_url.set(wazuh_config.url)
                    controller.wazuh_username.set(wazuh_config.username)
                    controller.wazuh_password.set(wazuh_config.password)

            # Update dashboard controller
            if 'dashboard' in self.controllers:
                controller = self.controllers['dashboard']
                if hasattr(controller, 'wazuh_config'):
                    controller.wazuh_config = wazuh_config

            # Update alerts controller
            if 'alerts' in self.controllers:
                controller = self.controllers['alerts']
                if hasattr(controller, 'wazuh_config'):
                    controller.wazuh_config = wazuh_config

            debug_logger.info("Controllers synchronized with latest configuration")

        except Exception as e:
            debug_logger.error(f"Error syncing controllers with config: {e}")

    def create_view(self, name: str) -> None:
        try:
            config = self.VIEW_CONFIGS.get(name)
            if not config:
                logger.error(f"No configuration found for view: {name}")
                return

            # If view already exists and is still valid, don't recreate it
            if name in self.views:
                try:
                    # Check if the view is still valid
                    if self.views[name].winfo_exists():
                        debug_logger.info(f"View {name} already exists and is valid")

                        # Even if view exists, make sure controller has the latest config
                        if name in self.controllers:
                            if hasattr(self.controllers[name], 'wazuh_config'):
                                self.controllers[name].wazuh_config = self.config_manager.get_wazuh_config()
                            if hasattr(self.controllers[name], 'model') and hasattr(self.controllers[name].model,
                                                                                    'shuffle_url'):
                                # For IncidentHistoryController
                                self.controllers[name].model = self.config_manager.get_shuffle_config()

                        return
                except Exception as e:
                    # View exists but is invalid, will be recreated
                    debug_logger.info(f"View {name} exists but is invalid, recreating: {e}")
                    try:
                        self.views[name].destroy()
                    except Exception as destroy_err:
                        debug_logger.error(f"Error destroying invalid view: {destroy_err}")
                    del self.views[name]

            # Create model if specified
            model = None
            if config.model_class:
                # Use existing model if already initialized
                if name in self.models:
                    model = self.models[name]
                else:
                    model = config.model_class()
                    self.models[name] = model

            # Create controller
            controller = None
            if config.controller_class:
                # Use existing controller if already initialized
                if name in self.controllers:
                    controller = self.controllers[name]
                    debug_logger.info(f"Using existing controller for {name}")
                elif name == "settings":
                    controller = self.settings_controller
                elif model:
                    controller = config.controller_class(model)
                else:
                    controller = config.controller_class()
                self.controllers[name] = controller

            # Create view
            debug_logger.info(f"Creating new view for {name}")
            view = config.view_class(self.root.main_content_frame)
            self.views[name] = view

            # Set up view-controller relationship
            if controller:
                if hasattr(view, 'set_controller'):
                    view.set_controller(controller)

                if hasattr(controller, 'set_view'):
                    controller.set_view(view)

            # Add settings observer if needed
            if config.observes_settings and controller:
                if name == "alerts" or name == "dashboard":
                    if hasattr(controller, 'on_config_change'):
                        self.config_manager.add_wazuh_observer(controller.on_config_change)
                        debug_logger.info(f"Added Wazuh observer for {name}: {controller.on_config_change}")
                elif name == "incident_history":
                    if hasattr(controller, 'on_config_change'):
                        self.config_manager.add_shuffle_observer(controller.on_config_change)
                        debug_logger.info(f"Added Shuffle observer for {name}: {controller.on_config_change}")

            logger.info(f"Created view: {name}")

        except Exception as e:
            logger.error(f"Error creating view {name}: {e}")
            debug_logger.error(f"Error creating view {name}: {e}")
            import traceback
            debug_logger.error(traceback.format_exc())
            raise

    def show(self, name: str) -> None:
        try:
            debug_logger.info(f"=== Router Show: {name} ===")
            debug_logger.info(f"Controller exists: {name in self.controllers}")
            debug_logger.info(f"View exists: {name in self.views}")

            # Ensure controllers have the latest configuration before showing view
            self.sync_controllers_with_config()

            # Store references to old views for proper cleanup
            old_views = {}
            for view_name, view in self.views.items():
                if view.winfo_ismapped():
                    old_views[view_name] = view

            # Properly destroy old views if needed
            for view_name, view in old_views.items():
                try:
                    view.grid_forget()
                    if view_name != name:  # Don't destroy the view we're about to show if it exists
                        debug_logger.info(f"Properly destroying old view: {view_name}")
                        self.views[view_name].destroy()
                        del self.views[view_name]
                except Exception as e:
                    debug_logger.error(f"Error removing old view {view_name}: {e}")

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
                    if hasattr(controller, 'update_dashboard'):
                        debug_logger.info("Calling dashboard update")
                        controller.update_dashboard()
                    elif hasattr(controller, 'update_alerts'):
                        debug_logger.info("Calling alerts update")
                        controller.update_alerts()

            debug_logger.info(f"Showed view: {name}")

        except Exception as e:
            error_msg = f"Error showing view {name}: {e}"
            debug_logger.error(error_msg)
            import traceback
            debug_logger.error(traceback.format_exc())

    def cleanup(self):
        """Cleanup resources when closing the application"""
        try:
            debug_logger.info("=== Router Cleanup ===")

            # Cleanup controllers
            for name, controller in self.controllers.items():
                debug_logger.info(f"Cleaning up controller: {name}")
                if hasattr(controller, 'cleanup'):
                    controller.cleanup()

            # Remove observers
            for name, controller in self.controllers.items():
                if hasattr(controller, 'on_config_change'):
                    debug_logger.info(f"Removing {name} from observers")
                    self.config_manager.remove_wazuh_observer(controller.on_config_change)

            # Cleanup views
            for name, view in self.views.items():
                debug_logger.info(f"Destroying view: {name}")
                try:
                    view.destroy()
                except Exception as e:
                    debug_logger.error(f"Error destroying view {name}: {e}")

            logger.info("Router cleanup completed")

        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            debug_logger.error(f"Error during cleanup: {e}")
            import traceback
            debug_logger.error(traceback.format_exc())