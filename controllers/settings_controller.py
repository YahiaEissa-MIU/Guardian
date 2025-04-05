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


class SettingsController:
    def __init__(self):
        print("Initializing SettingsController...")
        # Load Wazuh configuration
        self.wazuh_config = WazuhConfig.load_from_file()

        # Load Shuffle Configuration
        self.incident_model = IncidentHistoryModel.load_from_file()

        # UI Variables
        self.wazuh_url = ctk.StringVar(value=self.wazuh_config.url)
        self.wazuh_username = ctk.StringVar(value=self.wazuh_config.username)
        self.wazuh_password = ctk.StringVar(value=self.wazuh_config.password)

        # UI Variables for Shuffle
        self.shuffle_url = ctk.StringVar(value=self.incident_model.shuffle_url)
        self.shuffle_api_key = ctk.StringVar(value=self.incident_model.shuffle_api_key)
        self.shuffle_workflow = ctk.StringVar(value=self.incident_model.workflow_name)

        # Additional Settings Variables
        self.notify_var = ctk.BooleanVar(value=True)
        self.auto_backup_var = ctk.BooleanVar(value=True)
        self.frequency_var = ctk.StringVar(value="Daily")
        self.recovery_var = ctk.StringVar(value="Most Recent Backup")

        # Observer pattern implementation
        self.observers: List[Callable] = []

        # For tracking connection test status
        self.is_testing = False
        print("SettingsController initialized")
        # Agent Configuration initialization
        self.agent_config_path = self.get_agent_config_path()

        self.notification_enabled = self.notify_var.get()

        self.view = None

        # UI Variables for Shuffle
        self.shuffle_url = ctk.StringVar(value="http://192.168.1.5:3001")
        self.shuffle_api_key = ctk.StringVar(value="fefe8649-81bc-4aa8-8eee-46d20fb3a8f4")
        self.shuffle_workflow = ctk.StringVar(value="test")

    def set_view(self, view):
        """Set the view for this controller"""
        self.view = view
        print("View set for SettingsController")

    def test_connection(self):
        """
        Tests the Wazuh connection with current settings in a separate thread.
        Updates UI to show testing status.
        """
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
        """
        Saves the current settings after validation.
        Returns True if successful, False otherwise.
        """
        try:
            print("Attempting to save settings...")
            # First test the connection
            temp_config = WazuhConfig(
                url=self.wazuh_url.get(),
                username=self.wazuh_username.get(),
                password=self.wazuh_password.get(),
                suspicious_paths=self.wazuh_config.suspicious_paths
            )

            print("Validating connection before saving...")
            if not temp_config.validate_connection():
                print("Connection validation failed")
                messagebox.showerror("Error", "Cannot save settings: Connection test failed!")
                return False

            # Update model with current UI values
            print("Updating configuration...")
            self.wazuh_config.url = self.wazuh_url.get()
            self.wazuh_config.username = self.wazuh_username.get()
            self.wazuh_config.password = self.wazuh_password.get()

            # Save configuration
            if self.wazuh_config.save_to_file():
                print("Settings saved successfully")
                # Notify all observers of the change
                self.notify_observers()
                messagebox.showinfo("Success", "Settings saved and applied successfully!")
                return True
            else:
                print("Failed to save settings")
                messagebox.showerror("Error", "Failed to save settings!")
                return False

        except Exception as e:
            print(f"Error saving settings: {e}")
            messagebox.showerror("Error", f"Failed to save settings: {e}")
            return False

    def add_suspicious_path(self, path: str) -> bool:
        """
        Adds a new suspicious path to the configuration.
        Returns True if successful, False otherwise.
        """
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
        """
        Removes a suspicious path from the configuration.
        Returns True if successful, False otherwise.
        """
        print(f"Removing suspicious path: {path}")
        if self.wazuh_config.remove_suspicious_path(path):
            print("Path removed successfully")
            self.notify_observers()
            return True
        return False

    def get_suspicious_paths(self) -> List[str]:
        """Returns the current list of suspicious paths."""
        return self.wazuh_config.suspicious_paths

    def reset_wazuh_to_default(self):
        """Resets Wazuh settings to their default values."""
        try:
            print("Resetting Wazuh settings to default values...")
            # Load default configuration
            with open('default_wazuh_config.json', 'r') as f:
                default_config = json.load(f)

            # Update UI variables
            self.wazuh_url.set(default_config['url'])
            self.wazuh_username.set(default_config['username'])
            self.wazuh_password.set(default_config['password'])

            print("Wazuh settings reset to default values")
            messagebox.showinfo("Success", "Wazuh settings reset to default values!")

            # Save and notify observers
            self.save_settings()

        except Exception as e:
            print(f"Error resetting Wazuh settings: {e}")
            messagebox.showerror("Error", f"Failed to reset Wazuh settings: {e}")

    def add_observer(self, callback: Callable):
        """Adds an observer to be notified of configuration changes."""
        print(f"Adding observer: {callback}")
        if callback not in self.observers:
            self.observers.append(callback)

    def remove_observer(self, callback: Callable):
        """Removes an observer from the notification list."""
        print(f"Removing observer: {callback}")
        if callback in self.observers:
            self.observers.remove(callback)

    def notify_observers(self):
        """Notifies all observers of configuration changes."""
        print(f"Notifying {len(self.observers)} observers of configuration changes")
        for observer in self.observers:
            try:
                observer(self.wazuh_config)
                print(f"Successfully notified observer: {observer}")
            except Exception as e:
                print(f"Error notifying observer {observer}: {e}")

    def toggle_notifications(self):
        """Toggles the notification setting."""
        current_state = self.notify_var.get()
        print(f"Notifications {'enabled' if current_state else 'disabled'}")

    def toggle_auto_backup(self):
        """Toggles the auto backup setting."""
        current_state = self.auto_backup_var.get()
        print(f"Auto backup {'enabled' if current_state else 'disabled'}")

    def validate_settings(self) -> bool:
        """
        Validates all current settings.
        Returns True if all settings are valid, False otherwise.
        """
        print("Validating settings...")
        # Validate URL
        url = self.wazuh_url.get().strip()
        if not url:
            print("URL validation failed: empty URL")
            messagebox.showerror("Error", "Wazuh URL cannot be empty!")
            return False

        # Validate username
        username = self.wazuh_username.get().strip()
        if not username:
            print("Username validation failed: empty username")
            messagebox.showerror("Error", "Username cannot be empty!")
            return False

        # Validate password
        password = self.wazuh_password.get().strip()
        if not password:
            print("Password validation failed: empty password")
            messagebox.showerror("Error", "Password cannot be empty!")
            return False

        print("Settings validation successful")
        return True

    def apply_settings(self) -> bool:
        """
        Validates and applies all settings.
        Returns True if successful, False otherwise.
        """
        print("Applying settings...")
        if not self.validate_settings():
            print("Settings validation failed")
            return False

        if self.test_connection():
            print("Connection test successful, saving settings")
            return self.save_settings()
        print("Connection test failed, settings not saved")
        return False

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

        try:
            if not self.view:
                messagebox.showerror("Error", "View not properly initialized")
                return False

            new_ip = self.view.get_agent_ip()  # New method needed in view
            if not new_ip:
                messagebox.showerror("Error", "Please enter a valid IP address")
                return False

            # Backup current configuration
            self.backup_agent_config()

            # Update the configuration file
            self.modify_agent_config(new_ip)

            # Restart the agent service
            self.restart_agent_service()

            messagebox.showinfo(
                "Success",
                "Agent configuration updated successfully. The agent will restart to apply changes."
            )
            return True

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update agent configuration: {str(e)}")
            return False

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
                subprocess.run(["net", "stop", "WazuhSvc"], check=True)
                subprocess.run(["net", "start", "WazuhSvc"], check=True)
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

    def toggle_notifications(self):
        """Toggles the notification system."""
        self.notification_enabled = self.notify_var.get()
        print(f"Notifications {'enabled' if self.notification_enabled else 'disabled'}")

        if self.notification_enabled:
            messagebox.showinfo(
                "Notifications Enabled",
                "You will now receive desktop notifications for security alerts."
            )
            # Send a test notification to confirm it's working
            try:
                notification.notify(
                    title='Guardian Security',
                    message='Notifications enabled successfully. You will now receive security alerts.',
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
        """Tests the Shuffle connection with current settings."""
        if self.is_testing:
            print("Connection test already in progress")
            return

        def test_connection_thread():
            self.is_testing = True
            try:
                print("Testing Shuffle connection...")
                # Use the directly loaded incident model
                success = self.incident_model.update_shuffle_config(
                    url=self.shuffle_url.get(),
                    api_key=self.shuffle_api_key.get(),
                    workflow_name=self.shuffle_workflow.get()
                )

                if not success:
                    print("Failed to update Shuffle configuration")
                    messagebox.showerror("Error", "Failed to update Shuffle configuration!")
                    return False

                # Create new event loop for async operation
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
        """Saves the Shuffle settings."""
        try:
            print("Attempting to save Shuffle settings...")
            # Update model with current UI values
            if self.incident_model.update_shuffle_config(
                    url=self.shuffle_url.get(),
                    api_key=self.shuffle_api_key.get(),
                    workflow_name=self.shuffle_workflow.get()
            ):
                # Save configuration
                if self.incident_model.save_to_file():
                    print("Shuffle settings saved successfully")
                    self.notify_observers()
                    messagebox.showinfo("Success", "Shuffle settings saved successfully!")
                    return True
                else:
                    print("Failed to save Shuffle settings")
                    messagebox.showerror("Error", "Failed to save Shuffle settings!")
                    return False
            return False

        except Exception as e:
            print(f"Error saving Shuffle settings: {e}")
            messagebox.showerror("Error", f"Failed to save Shuffle settings: {e}")
            return False

    def reset_shuffle_to_default(self):
        """Resets Shuffle settings to their default values."""
        try:
            print("Resetting Shuffle settings to default values...")
            # Create new instance with default values
            default_model = IncidentHistoryModel()

            # Update UI variables
            self.shuffle_url.set(default_model.shuffle_url)
            self.shuffle_api_key.set(default_model.shuffle_api_key)
            self.shuffle_workflow.set(default_model.workflow_name)

            # Update model
            self.incident_model.update_shuffle_config(
                url=default_model.shuffle_url,
                api_key=default_model.shuffle_api_key,
                workflow_name=default_model.workflow_name
            )

            # Save configuration
            if self.incident_model.save_to_file():
                print("Shuffle settings reset to default values")
                messagebox.showinfo("Success", "Shuffle settings reset to default values!")
                return True

            return False

        except Exception as e:
            print(f"Error resetting Shuffle settings: {e}")
            messagebox.showerror("Error", f"Failed to reset Shuffle settings: {e}")
            return False
