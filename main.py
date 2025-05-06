from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import psutil
import os
import sys
import json
import time
from router import Router
from utils.config_manager import ConfigManager
from datetime import datetime
import importlib
import sys

# Force reload view modules on application start
view_modules = [
    'views.alerts_view',
    'views.incident_history_view',
    'views.dashboard_view',
    'views.settings_view',
    'views.about_system_view'
]

for module_name in view_modules:
    try:
        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])
            print(f"Reloaded module: {module_name}")
    except Exception as e:
        print(f"Error reloading {module_name}: {e}")

# Add debugging to check module paths
for module_name in view_modules:
    if module_name in sys.modules:
        module = sys.modules[module_name]
        if hasattr(module, '__file__'):
            print(f"Loading {module_name} from: {module.__file__}")

            # Check if class has VERSION attribute
            module_parts = module_name.split('.')
            class_name = module_parts[-1].replace('_view', '').title() + 'View'
            if hasattr(module, class_name) and hasattr(getattr(module, class_name), 'VERSION'):
                view_class = getattr(module, class_name)
                print(f"  {class_name} version: {view_class.VERSION}")


class ThemeManager:
    def __init__(self):
        self.config_file = os.path.join(os.getenv('APPDATA'), 'Guardian', 'theme_settings.json')
        self.create_config_directory()

    def create_config_directory(self):
        directory = os.path.dirname(self.config_file)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def save_theme(self, mode):
        with open(self.config_file, 'w') as f:
            json.dump({'theme_mode': mode}, f)

    def load_theme(self):
        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)
                return data.get('theme_mode', 'dark')
        except (FileNotFoundError, json.JSONDecodeError):
            return 'dark'


class StatusBar(ctk.CTkFrame):
    def __init__(self, master, colors):
        super().__init__(master, height=25)
        self.colors = colors
        self.setup_status_bar()
        self.start_updates()

    def setup_status_bar(self):
        # CPU Usage
        self.cpu_label = ctk.CTkLabel(
            self,
            text="CPU: 0%",
            font=("Arial", 11),
            padx=10
        )
        self.cpu_label.pack(side="left")

        # Memory Usage
        self.memory_label = ctk.CTkLabel(
            self,
            text="Memory: 0%",
            font=("Arial", 11),
            padx=10
        )
        self.memory_label.pack(side="left")

        # Time
        self.time_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 11),
            padx=10
        )
        self.time_label.pack(side="right")

    def start_updates(self):
        self.update_status()

    def update_status(self):
        # Update CPU
        cpu_percent = psutil.cpu_percent()
        self.cpu_label.configure(text=f"CPU: {cpu_percent}%")

        # Update Memory
        memory = psutil.virtual_memory()
        self.memory_label.configure(text=f"Memory: {memory.percent}%")

        # Update Time
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=current_time)

        # Schedule next update
        self.after(1000, self.update_status)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.theme_manager = ThemeManager()
        config_manager = ConfigManager()

        # Initialize theme
        self.current_theme = self.theme_manager.load_theme()
        ctk.set_appearance_mode(self.current_theme)
        ctk.set_default_color_theme("blue")
        self.load_icons()

        # Window setup
        self.title("Guardian")
        self.geometry("1200x600")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.sidebar_visible = True
        self.is_changing_theme = False

        # Theme colors
        self.colors = {
            "dark": {
                "sidebar": "#1E2124",  # Deep charcoal
                "main_content": "#282B30",  # Slightly lighter charcoal
                "button_hover": "#32363B",  # Lighter gray for hover
                "text": "#DCDDDE",  # Off-white text
                "nav_bar": "#1A1D1F",  # Slightly darker than sidebar for hierarchy
                "button_active": "#3B4048",  # Highlighted button
                "accent": "#5865F2",  # Discord-like blue
                "border": "#323639",  # Subtle border for better separation
                "header": "#FFFFFF",  # Pure white for headers
                "status_bar": "#1A1D1F"  # Match nav_bar
            },
            "light": {
                "sidebar": "#F0F2F5",  # Light gray for sidebar
                "main_content": "#FFFFFF",  # White for content area
                "button_hover": "#E3E5E8",  # Subtle hover state
                "text": "#1A1D21",  # Darker text for better contrast
                "nav_bar": "#E8EAED",  # Slightly darker than sidebar for visual hierarchy
                "button_active": "#D4D7DC",  # Subtle active state
                "accent": "#4361EE",  # Adjusted accent for better contrast in light mode
                "border": "#E1E3E6",  # Subtle border to define sections
                "header": "#0A0C10",  # Darker header text
                "status_bar": "#E8EAED"  # Match nav_bar
            }
        }

        # Load icons
        self.load_icons()

        # Create UI elements
        self.create_navigation_bar()
        self.create_sidebar()
        self.create_main_content()
        self.create_status_bar()

        # Initialize Router
        self.router = Router(self)
        self.router.show("dashboard")

        # Initialize notification count
        self.notification_count = 0
        self.start_notification_check()

    def load_icons(self):
        # Define icon paths
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icons")
        icon_files = {
            "dashboard": "dashboard.png",
            "alerts": "alert.png",
            "incident": "incident.png",
            "about": "about.png",
            "settings": "settings.png",
            "sun": "sun.png",  # Make sure you have this file
            "moon": "moon.png",  # Make sure you have this file
            "menu": "menu.png",
            "close": "close.png"
        }

        # Load icons
        self.icons = {}
        for name, file in icon_files.items():
            try:
                path = os.path.join(icon_path, file)
                image = Image.open(path)
                self.icons[name] = ctk.CTkImage(light_image=image, dark_image=image, size=(20, 20))
            except Exception as e:
                print(f"Failed to load icon {file}: {e}")
                self.icons[name] = None

    def update_theme_button(self):
        """Update theme button icon based on current theme"""
        # When in dark mode, show sun icon (to switch to light)
        # When in light mode, show moon icon (to switch to dark)
        icon_name = "sun" if self.current_theme == "dark" else "moon"

        # Recreate the theme button to ensure it's visible
        self.theme_button.destroy()
        self.theme_button = ctk.CTkButton(
            self.nav_bar,
            text="",
            image=self.icons[icon_name],
            command=self.toggle_theme,
            width=50,
            fg_color="transparent",
            hover_color=(self.colors["light"]["button_hover"], self.colors["dark"]["button_hover"])
        )
        self.theme_button.pack(side="right", padx=10, pady=5)

    def create_navigation_bar(self):
        self.nav_bar = ctk.CTkFrame(
            self,
            height=50,
            corner_radius=0,
            fg_color=(self.colors["light"]["nav_bar"], self.colors["dark"]["nav_bar"]),
            border_width=1,
            border_color=(self.colors["light"]["border"], self.colors["dark"]["border"])
        )
        self.nav_bar.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Menu toggle button
        self.toggle_button = ctk.CTkButton(
            self.nav_bar,
            text="",
            image=self.icons["menu"],
            command=self.toggle_sidebar,
            width=50,
            fg_color="transparent",
            hover_color=(self.colors["light"]["button_hover"], self.colors["dark"]["button_hover"]),
            text_color=(self.colors["light"]["text"], self.colors["dark"]["text"])
        )
        self.toggle_button.pack(side="left", padx=10, pady=5)

        # Application title
        self.nav_title = ctk.CTkLabel(
            self.nav_bar,
            text="Guardian",
            font=("Arial", 20, "bold"),
            text_color=(self.colors["light"]["header"], self.colors["dark"]["header"])
        )
        self.nav_title.pack(side="left", padx=20)

        # Theme toggle button - set correct initial icon based on current theme
        icon_name = "sun" if self.current_theme == "dark" else "moon"
        self.theme_button = ctk.CTkButton(
            self.nav_bar,
            text="",
            image=self.icons[icon_name],  # Use the correct icon based on current theme
            command=self.toggle_theme,
            width=50,
            fg_color="transparent",
            hover_color=(self.colors["light"]["button_hover"], self.colors["dark"]["button_hover"])
        )
        self.theme_button.pack(side="right", padx=10, pady=5)

    def create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(
            self,
            width=200,
            corner_radius=0,  # Remove corner radius
            fg_color=(self.colors["light"]["sidebar"], self.colors["dark"]["sidebar"]),
            border_width=0  # Remove border
        )
        self.sidebar_frame.grid(row=1, column=0, sticky="ns", padx=0, pady=0)  # Remove padding

        # Sidebar Header
        self.sidebar_header = ctk.CTkLabel(
            self.sidebar_frame,
            text="Menu",
            font=("Arial", 14, "bold"),
            text_color=(self.colors["light"]["header"], self.colors["dark"]["header"]),
            pady=15
        )
        self.sidebar_header.pack(fill="x")

        # Button configurations
        button_configs = [
            ("dashboard", " Dashboard", self.icons["dashboard"], lambda: self.router.show("dashboard")),
            ("alerts", " Alerts", self.icons["alerts"], lambda: self.router.show("alerts")),
            ("incident_history", " Incident History", self.icons["incident"],
             lambda: self.router.show("incident_history")),
            ("about_system", " About System", self.icons["about"], lambda: self.router.show("about_system")),
            ("settings", " Settings", self.icons["settings"], lambda: self.router.show("settings"))
        ]

        # Create buttons with notification badges
        self.sidebar_buttons = {}
        self.notification_badges = {}

        for btn_id, text, icon, command in button_configs:
            # Create a frame for each button and its badge
            button_container = ctk.CTkFrame(
                self.sidebar_frame,
                fg_color="transparent"
            )
            button_container.pack(fill="x", padx=5, pady=2)

            # Create the button
            button = ctk.CTkButton(
                button_container,
                text=text,
                image=icon,
                command=command,
                anchor="w",
                corner_radius=8,
                fg_color="transparent",
                hover_color=(self.colors["light"]["button_hover"], self.colors["dark"]["button_hover"]),
                text_color=(self.colors["light"]["text"], self.colors["dark"]["text"]),
                height=40
            )
            button.pack(side="left", fill="x", expand=True)

            self.sidebar_buttons[btn_id] = button

    def create_main_content(self):
        self.main_content_frame = ctk.CTkFrame(
            self,
            corner_radius=8,  # Add subtle corner radius
            fg_color=(self.colors["light"]["main_content"], self.colors["dark"]["main_content"]),
            border_width=0  # Remove border for seamless look
        )
        self.main_content_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 10), pady=(10, 10))  # Add padding
        self.main_content_frame.grid_rowconfigure(0, weight=1)
        self.main_content_frame.grid_columnconfigure(0, weight=1)

    def create_status_bar(self):
        self.status_bar = StatusBar(
            self,
            self.colors
        )
        self.status_bar.grid(row=2, column=0, columnspan=2, sticky="ew")

    def toggle_theme(self):
        """Toggle between light and dark themes with animation"""
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self.current_theme = new_theme

        # Create fade effect
        self.attributes('-alpha', 0.95)

        # Remember which view is currently visible
        current_view = None
        if hasattr(self, 'router') and self.router:
            for name, view in self.router.views.items():
                if view.winfo_ismapped():
                    current_view = name
                    break

        # Apply theme change
        ctk.set_appearance_mode(self.current_theme)
        self.theme_manager.save_theme(self.current_theme)

        # Update colors
        self.update_colors()

        # Update theme button icon
        # When in dark mode, show sun icon (to switch to light)
        # When in light mode, show moon icon (to switch to dark)
        icon_name = "sun" if self.current_theme == "dark" else "moon"
        if hasattr(self, 'theme_button'):
            self.theme_button.configure(image=self.icons[icon_name])

        # Reset and reload current view if needed
        if current_view and hasattr(self, 'router') and self.router:
            # Force view recreation for the current view
            if current_view in self.router.views:
                try:
                    self.router.views[current_view].destroy()
                    del self.router.views[current_view]
                except Exception as e:
                    print(f"Error destroying view {current_view}: {e}")
            # Show the view again (this will create a new instance)
            self.router.show(current_view)

        # Restore opacity with animation
        self.after(100, lambda: self.attributes('-alpha', 0.97))
        self.after(200, lambda: self.attributes('-alpha', 1.0))

    def update_colors(self):
        """Update colors for all components"""
        theme = self.current_theme

        self.nav_bar.configure(
            fg_color=(self.colors["light"]["nav_bar"], self.colors["dark"]["nav_bar"]),
            border_color=(self.colors["light"]["border"], self.colors["dark"]["border"])
        )

        self.sidebar_frame.configure(
            fg_color=(self.colors["light"]["sidebar"], self.colors["dark"]["sidebar"]),
            border_color=(self.colors["light"]["border"], self.colors["dark"]["border"])
        )

        self.main_content_frame.configure(
            fg_color=(self.colors["light"]["main_content"], self.colors["dark"]["main_content"]),
            border_color=(self.colors["light"]["border"], self.colors["dark"]["border"])
        )

    def toggle_sidebar(self):
        """Toggle sidebar with smooth animation"""
        if self.sidebar_visible:
            self.sidebar_frame.grid_remove()
            # Ensure the menu icon is always used when sidebar is hidden
            self.toggle_button.configure(image=self.icons["menu"])
        else:
            self.sidebar_frame.grid(row=1, column=0, sticky="ns", padx=(0, 0), pady=0)
            # Ensure the close icon is always used when sidebar is visible
            self.toggle_button.configure(image=self.icons["close"])
        self.sidebar_visible = not self.sidebar_visible

    def start_notification_check(self):
        """Start periodic notification check"""
        self.check_notifications()
        self.after(30000, self.start_notification_check)  # Check every 30 seconds

    def check_notifications(self):
        """Check for new notifications"""
        try:
            # This is a placeholder - implement your actual notification checking logic
            # For demonstration, we'll just toggle between 0 and 3 notifications
            self.notification_count = 3 if self.notification_count == 0 else 0

            if "alerts" in self.notification_badges:
                badge = self.notification_badges["alerts"]
                if badge:
                    self.after(100, lambda: badge.update_count(self.notification_count))
        except Exception as e:
            print(f"Error updating notifications: {e}")


def verify_configurations(self):
    """Verify all configurations are properly loaded on startup"""
    try:
        # Get the config manager
        config_manager = ConfigManager()

        # Get current configurations
        wazuh_config = config_manager.get_wazuh_config()
        shuffle_config = config_manager.get_shuffle_config()

        # Log current configuration state
        print(f"Startup Config Verification:")
        print(f"Wazuh configured: {wazuh_config.is_configured}")
        if wazuh_config.is_configured:
            print(f"Wazuh URL: {wazuh_config.url}")
            print(f"Wazuh username: {wazuh_config.username}")
            print(f"Wazuh password: {'*' * len(wazuh_config.password) if wazuh_config.password else 'None'}")

        print(f"Shuffle configured: {shuffle_config.is_configured}")
        if shuffle_config.is_configured:
            print(f"Shuffle URL: {shuffle_config.shuffle_url}")

        # If you have multiple controllers, make sure they all have the current config
        if hasattr(self, 'alerts_controller'):
            self.alerts_controller.wazuh_config = wazuh_config

        if hasattr(self, 'dashboard_controller'):
            if hasattr(self.dashboard_controller, 'wazuh_config'):
                self.dashboard_controller.wazuh_config = wazuh_config

        if hasattr(self, 'settings_controller'):
            self.settings_controller.wazuh_config = wazuh_config
            self.settings_controller.wazuh_url.set(wazuh_config.url)
            self.settings_controller.wazuh_username.set(wazuh_config.username)
            self.settings_controller.wazuh_password.set(wazuh_config.password)

    except Exception as e:
        print(f"Error during configuration verification: {e}")


def check_admin():
    try:
        import ctypes
        if sys.platform == 'win32':
            print("Checking administrator privileges...")
            if ctypes.windll.shell32.IsUserAnAdmin():
                print("Running with administrator privileges")
                return True
            else:
                print("Not running with administrator privileges")
                if not ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1):
                    print("Failed to restart with administrator privileges")
                    return False
                sys.exit(0)
    except Exception as e:
        print(f"Error checking admin privileges: {e}")
        return False


if __name__ == "__main__":
    if not check_admin():
        messagebox.showerror("Error", "Administrator privileges required!")
        sys.exit(1)
    app = App()
    app.mainloop()
