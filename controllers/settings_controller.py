# controllers/settings_controller.py
import asyncio
import ctypes
import json
import os
import subprocess
import sys
from datetime import datetime
from plyer import notification
import customtkinter as ctk
from tkinter import messagebox
from models.incident_history_model import IncidentHistoryModel
from models.wazuh_config import WazuhConfig
from typing import Callable, List
import threading
from utils.config_manager import ConfigManager


def get_app_data_dir():
    """Get or create application data directory"""
    try:
        if sys.platform == "win32":
            app_data = os.path.join(os.environ['APPDATA'], 'Guardian')
        else:
            app_data = os.path.join(os.path.expanduser('~'), '.guardian')

        # Create directory if it doesn't exist
        os.makedirs(app_data, exist_ok=True)  # Changed to use exist_ok=True

        # Define config file paths
        wazuh_config = os.path.join(app_data, 'wazuh_config.json')
        shuffle_config = os.path.join(app_data, 'shuffle_config.json')

        # Initialize empty config files if they don't exist
        for config_file in [wazuh_config, shuffle_config]:
            if not os.path.exists(config_file):
                with open(config_file, 'w') as f:
                    json.dump({}, f)

        return app_data
    except Exception as e:
        print(f"Error creating app data directory: {e}")
        return None


class SettingsController:
    def __init__(self):
        print("Initializing SettingsController...")
        self.app_data_dir = get_app_data_dir()
        self.wazuh_config_path = os.path.join(self.app_data_dir, 'wazuh_config.json')
        self.shuffle_config_path = os.path.join(self.app_data_dir, 'shuffle_config.json')
        self.config_manager = ConfigManager()
        self.wazuh_config = self.config_manager.wazuh_config
        self.incident_model = self.config_manager.incident_model

        # UI Variables for Wazuh
        self.wazuh_url = ctk.StringVar()
        self.wazuh_username = ctk.StringVar()
        self.wazuh_password = ctk.StringVar()

        # UI Variables for Shuffle
        self.shuffle_url = ctk.StringVar()
        self.shuffle_api_key = ctk.StringVar()
        self.shuffle_workflow = ctk.StringVar()

        # Additional Settings Variables
        self.notify_var = ctk.BooleanVar(value=False)  # Start with notifications disabled
        self.auto_backup_var = ctk.BooleanVar(value=False)
        self.frequency_var = ctk.StringVar(value="Daily")
        self.recovery_var = ctk.StringVar(value="Most Recent Backup")

        # Observer pattern implementation
        self.observers: List[Callable] = []

        # For tracking connection test status
        self.is_testing = False

        # Agent Configuration initialization
        self.agent_config_path = self.get_agent_config_path()
        self.notification_enabled = self.notify_var.get()
        self.view = None

        # Load any existing configurations
        self.load_existing_configurations()
        print("SettingsController initialized")

    def load_existing_configurations(self):
        """Load existing configurations if they exist"""
        try:
            print("Loading existing configurations...")

            # Load Wazuh config
            wazuh_config_path = os.path.join(self.app_data_dir, 'wazuh_config.json')
            if os.path.exists(wazuh_config_path):
                print(f"Loading Wazuh config from: {wazuh_config_path}")
                self.wazuh_config = WazuhConfig.load_from_file(wazuh_config_path)
                if self.wazuh_config.is_configured:
                    self.wazuh_url.set(self.wazuh_config.url)
                    self.wazuh_username.set(self.wazuh_config.username)
                    self.wazuh_password.set(self.wazuh_config.password)
                    print("Wazuh config loaded successfully")

            # Load Shuffle config
            shuffle_config_path = os.path.join(self.app_data_dir, 'shuffle_config.json')
            if os.path.exists(shuffle_config_path):
                print(f"Loading Shuffle config from: {shuffle_config_path}")
                self.incident_model = IncidentHistoryModel.load_from_file(shuffle_config_path)
                if self.incident_model.is_configured:
                    self.shuffle_url.set(self.incident_model.shuffle_url)
                    self.shuffle_api_key.set(self.incident_model.shuffle_api_key)
                    self.shuffle_workflow.set(self.incident_model.workflow_name)
                    print("Shuffle config loaded successfully")

        except Exception as e:
            print(f"Error loading configurations: {e}")

    def set_view(self, view):
        """Set the view for this controller"""
        self.view = view
        print("View set for SettingsController")

    def test_connection(self):
        """Tests the Wazuh connection with current settings"""
        if self.is_testing:
            print("Connection test already in progress")
            return

        def test_connection_thread():
            self.is_testing = True
            try:
                print("Testing connection with current settings...")
                # Create temporary config with current UI values
                temp_config = WazuhConfig(
                    url=self.wazuh_url.get(),
                    username=self.wazuh_username.get(),
                    password=self.wazuh_password.get(),
                    suspicious_paths=self.wazuh_config.suspicious_paths
                )

                if temp_config.validate_connection():
                    print("Connection test successful")
                    messagebox.showinfo("Success", "Connection test successful!")
                    return True
                else:
                    print("Connection test failed")
                    messagebox.showerror("Error", "Connection test failed!")
                    return False
            except Exception as e:
                print(f"Connection test error: {e}")
                messagebox.showerror("Error", f"Connection test failed: {e}")
                return False
            finally:
                self.is_testing = False

        # Start connection test in separate thread
        print("Starting connection test thread")
        thread = threading.Thread(target=test_connection_thread)
        thread.daemon = True
        thread.start()

    def save_settings(self) -> bool:
        """Saves Wazuh settings after validation"""
        try:
            if not self.validate_settings():
                return False

            # Create new config with current values
            new_config = WazuhConfig(
                url=self.wazuh_url.get().strip(),
                username=self.wazuh_username.get().strip(),
                password=self.wazuh_password.get().strip(),
                suspicious_paths=self.wazuh_config.suspicious_paths,
                last_modified=datetime.now()
            )

            # Save configuration first
            config_path = os.path.join(self.app_data_dir, 'wazuh_config.json')
            if new_config.save_to_file(config_path):
                # Test connection after saving
                if new_config.validate_connection():
                    self.wazuh_config = new_config
                    self.notify_observers()
                    messagebox.showinfo("Success", "Settings saved and connection verified!")
                    return True
                else:
                    messagebox.showwarning("Warning", "Settings saved but connection test failed.")
                    return True

            messagebox.showerror("Error", "Failed to save settings!")
            return False

        except Exception as e:
            print(f"Error saving settings: {e}")
            messagebox.showerror("Error", f"Failed to save settings: {e}")
            return False

    def save_shuffle_settings(self) -> bool:
        """Saves Shuffle settings after validation"""
        try:
            shuffle_url = self.shuffle_url.get().strip()
            shuffle_api_key = self.shuffle_api_key.get().strip()
            workflow_name = self.shuffle_workflow.get().strip()

            if not all([shuffle_url, shuffle_api_key, workflow_name]):
                messagebox.showerror("Error", "All fields must be filled!")
                return False

            # Update model with new values
            self.incident_model.shuffle_url = shuffle_url
            self.incident_model.shuffle_api_key = shuffle_api_key
            self.incident_model.workflow_name = workflow_name
            self.incident_model.is_configured = True
            self.incident_model.last_modified = datetime.now()

            # Save to file
            config_path = os.path.join(self.app_data_dir, 'shuffle_config.json')
            if self.incident_model.save_to_file(config_path):
                messagebox.showinfo("Success", "Shuffle settings saved successfully!")
                return True

            messagebox.showerror("Error", "Failed to save Shuffle settings!")
            return False

        except Exception as e:
            print(f"Error saving Shuffle settings: {e}")
            messagebox.showerror("Error", f"Failed to save Shuffle settings: {e}")
            return False

    def validate_settings(self) -> bool:
        """Validates the current settings"""
        if not self.wazuh_url.get().strip():
            messagebox.showerror("Error", "Wazuh URL cannot be empty!")
            return False

        if not self.wazuh_username.get().strip():
            messagebox.showerror("Error", "Username cannot be empty!")
            return False

        if not self.wazuh_password.get().strip():
            messagebox.showerror("Error", "Password cannot be empty!")
            return False

        return True

    def add_suspicious_path(self, path: str) -> bool:
        """Adds a new suspicious path to the configuration"""
        print(f"Adding suspicious path: {path}")
        if not path.strip():
            messagebox.showwarning("Warning", "Please enter a valid path!")
            return False

        if self.wazuh_config.add_suspicious_path(path.strip()):
            print("Path added successfully")
            self.notify_observers()
            return True
        return False

    def remove_suspicious_path(self, path: str) -> bool:
        """Removes a suspicious path from the configuration"""
        print(f"Removing suspicious path: {path}")
        if self.wazuh_config.remove_suspicious_path(path):
            print("Path removed successfully")
            self.notify_observers()
            return True
        return False

    def get_suspicious_paths(self) -> List[str]:
        """Returns the current list of suspicious paths"""
        return self.wazuh_config.suspicious_paths

    def add_observer(self, callback: Callable):
        """Adds an observer to be notified of configuration changes"""
        print(f"Adding observer: {callback}")
        if callback not in self.observers:
            self.observers.append(callback)

    def remove_observer(self, callback: Callable):
        """Removes an observer from the notification list"""
        print(f"Removing observer: {callback}")
        if callback in self.observers:
            self.observers.remove(callback)

    def notify_observers(self):
        """Notifies all observers of configuration changes"""
        print(f"Notifying {len(self.observers)} observers of configuration changes")
        for observer in self.observers:
            try:
                observer(self.wazuh_config)
                print(f"Successfully notified observer: {observer}")
            except Exception as e:
                print(f"Error notifying observer {observer}: {e}")

    def toggle_notifications(self):
        """Toggles the notification system"""
        self.notification_enabled = self.notify_var.get()
        print(f"Notifications {'enabled' if self.notification_enabled else 'disabled'}")

        if self.notification_enabled:
            messagebox.showinfo(
                "Notifications Enabled",
                "You will now receive desktop notifications for security alerts."
            )
            try:
                notification.notify(
                    title='Guardian Security',
                    message='Notifications enabled successfully.',
                    app_name='Guardian',
                    timeout=10,
                )
            except Exception as e:
                print(f"Error sending confirmation notification: {e}")
        else:
            messagebox.showinfo(
                "Notifications Disabled",
                "Desktop notifications have been disabled."
            )

    def toggle_auto_backup(self):
        """Toggles the auto backup setting"""
        current_state = self.auto_backup_var.get()
        print(f"Auto backup {'enabled' if current_state else 'disabled'}")

    def get_agent_config_path(self):
        """Get the path to the Wazuh agent configuration file"""
        if sys.platform == "win32":
            return "C:\\Program Files (x86)\\ossec-agent\\ossec.conf"
        return "/var/ossec/etc/ossec.conf"

    def is_admin(self):
        """Check if the program has administrator privileges"""
        try:
            if sys.platform == "win32":
                return ctypes.windll.shell32.IsUserAnAdmin()
            return os.geteuid() == 0
        except:
            return False

    def update_agent_config(self):
        """Update the Wazuh agent configuration"""
        if not self.is_admin():
            messagebox.showerror(
                "Error",
                "Administrator privileges required to modify agent configuration."
            )
            return False

        # Check file permissions
        has_permissions, message = self.check_file_permissions()
        if not has_permissions:
            messagebox.showerror(
                "Error",
                f"Insufficient permissions: {message}"
            )
            return False

        if not self.view:
            messagebox.showerror("Error", "View not properly initialized")
            return False

        new_ip = self.view.get_agent_ip()
        if not new_ip:
            messagebox.showerror("Error", "Please enter a valid IP address")
            return False

        def update_config_thread():
            try:
                print(f"Starting configuration update for IP: {new_ip}")

                # Create backup
                print("Creating backup...")
                self.backup_agent_config()

                # Modify configuration
                print("Modifying configuration...")
                self.modify_agent_config(new_ip)

                # Restart service
                print("Restarting service...")
                self.restart_agent_service()

                # Verify the change
                print("Verifying changes...")
                with open(self.agent_config_path, 'r') as f:
                    content = f.read()
                    if new_ip not in content:
                        raise Exception("Failed to verify IP address change in configuration")

                # Show success message
                if self.view:
                    self.view.after(0, lambda: messagebox.showinfo(
                        "Success",
                        "Agent configuration updated successfully. The agent will restart to apply changes."
                    ))
                return True

            except Exception as e:
                print(f"Error during configuration update: {str(e)}")
                if self.view:
                    self.view.after(0, lambda: messagebox.showerror(
                        "Error",
                        f"Failed to update agent configuration: {str(e)}"
                    ))
                return False

        # Start update in separate thread
        thread = threading.Thread(target=update_config_thread)
        thread.daemon = True
        thread.start()
        return True

    def check_file_permissions(self):
        """Check if we have the necessary permissions to modify the config file"""
        try:
            # Check if file exists
            if not os.path.exists(self.agent_config_path):
                return False, "Configuration file not found"

            # Check read permission
            if not os.access(self.agent_config_path, os.R_OK):
                return False, "No read permission"

            # Check write permission
            if not os.access(self.agent_config_path, os.W_OK):
                return False, "No write permission"

            return True, "Permissions OK"
        except Exception as e:
            return False, str(e)

    def backup_agent_config(self):
        """Create a backup of the current agent configuration"""
        try:
            import shutil
            backup_path = f"{self.agent_config_path}.backup"
            shutil.copy2(self.agent_config_path, backup_path)
        except Exception as e:
            raise Exception(f"Failed to create backup: {str(e)}")

    def modify_agent_config(self, new_ip):
        """Modify the agent configuration file with the new IP"""
        try:
            import xml.etree.ElementTree as ET

            # Parse the configuration file
            tree = ET.parse(self.agent_config_path)
            root = tree.getroot()

            # Find and update the manager IP address
            for client in root.findall(".//client"):
                for server in client.findall("server"):
                    ip_elem = server.find("address")
                    if ip_elem is not None:
                        ip_elem.text = new_ip

            # Save the modified configuration
            tree.write(self.agent_config_path)

        except Exception as e:
            raise Exception(f"Failed to modify configuration: {str(e)}")

    def restart_agent_service(self):
        """Restart the Wazuh agent service"""
        try:
            if sys.platform == "win32":
                # Use subprocess.CREATE_NO_WINDOW to hide the CMD window
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE

                # Stop service
                subprocess.run(
                    ["net", "stop", "WazuhSvc"],
                    startupinfo=startupinfo,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    check=True
                )

                # Start service
                subprocess.run(
                    ["net", "start", "WazuhSvc"],
                    startupinfo=startupinfo,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    check=True
                )
            else:
                subprocess.run(["systemctl", "restart", "wazuh-agent"], check=True)
        except Exception as e:
            raise Exception(f"Failed to restart agent service: {str(e)}")

    def test_notification(self):
        """Sends a test notification"""
        if not self.notify_var.get():
            messagebox.showwarning(
                "Notifications Disabled",
                "Please enable notifications first to test them."
            )
            return

        try:
            notification.notify(
                title='Guardian Security - Test',
                message='This is a test notification. Your notification system is working correctly.',
                app_name='Guardian',
                timeout=10,
            )
            print("Test notification sent successfully")
            messagebox.showinfo(
                "Success",
                "Test notification sent successfully!\nIf you didn't see it, please check your system's notification settings."
            )
        except Exception as e:
            print(f"Failed to send test notification: {e}")
            messagebox.showerror(
                "Error",
                f"Failed to send test notification: {str(e)}\n"
                "Please check if notifications are enabled in your system settings."
            )

    def send_notification(self, title: str, message: str):
        """Sends a desktop notification if enabled"""
        if self.notification_enabled:
            try:
                notification.notify(
                    title=title,
                    message=message,
                    app_name='Guardian',
                    timeout=10,
                )
                print(f"Notification sent: {title}")
            except Exception as e:
                print(f"Failed to send notification: {e}")

    def test_shuffle_connection(self):
        """Tests the Shuffle connection with current settings"""
        if self.is_testing:
            print("Connection test already in progress")
            return

        def test_connection_thread():
            self.is_testing = True
            try:
                print("Testing Shuffle connection...")
                success = self.incident_model.update_shuffle_config(
                    url=self.shuffle_url.get(),
                    api_key=self.shuffle_api_key.get(),
                    workflow_name=self.shuffle_workflow.get()
                )

                if not success:
                    print("Failed to update Shuffle configuration")
                    messagebox.showerror("Error", "Failed to update Shuffle configuration!")
                    return False

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                if loop.run_until_complete(self.incident_model.validate_connection()):
                    print("Shuffle connection test successful")
                    messagebox.showinfo("Success", "Shuffle connection test successful!")
                    return True
                else:
                    print("Shuffle connection test failed")
                    messagebox.showerror("Error", "Shuffle connection test failed!")
                    return False
            except Exception as e:
                print(f"Shuffle connection test error: {e}")
                messagebox.showerror("Error", f"Shuffle connection test failed: {e}")
                return False
            finally:
                self.is_testing = False

        print("Starting Shuffle connection test thread")
        thread = threading.Thread(target=test_connection_thread)
        thread.daemon = True
        thread.start()

    def save_shuffle_settings(self) -> bool:
        """Saves Shuffle settings after validation"""
        try:
            print("Attempting to save Shuffle settings...")  # Debug print

            # Validate inputs
            shuffle_url = self.shuffle_url.get().strip()
            shuffle_api_key = self.shuffle_api_key.get().strip()
            workflow_name = self.shuffle_workflow.get().strip()

            if not all([shuffle_url, shuffle_api_key, workflow_name]):
                messagebox.showerror("Error", "All fields must be filled!")
                return False

            print(f"Updating Shuffle config with URL: {shuffle_url}")  # Debug print

            # Update incident model configuration
            self.incident_model.shuffle_url = shuffle_url
            self.incident_model.shuffle_api_key = shuffle_api_key
            self.incident_model.workflow_name = workflow_name
            self.incident_model.is_configured = True
            self.incident_model.last_modified = datetime.now()

            # Save to file with full path
            config_path = os.path.join(self.app_data_dir, 'shuffle_config.json')
            print(f"Saving to path: {config_path}")  # Debug print

            if self.incident_model.save_to_file(config_path):
                print("Save successful")  # Debug print
                messagebox.showinfo("Success", "Shuffle settings saved successfully!")
                return True

            print("Save failed")  # Debug print
            messagebox.showerror("Error", "Failed to save Shuffle settings!")
            return False

        except Exception as e:
            print(f"Error saving Shuffle settings: {e}")
            messagebox.showerror("Error", f"Failed to save Shuffle settings: {e}")
            return False
