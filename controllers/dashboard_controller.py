# controllers/dashboard_controller.py
import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from .alerts_controller import AlertsController, acknowledged_alerts_storage
from models.wazuh_config import WazuhConfig

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class DashboardController:
    def __init__(self, view):
        print("Initializing DashboardController...")
        self.view = view
        self.wazuh_config = WazuhConfig.load_from_file()
        self.alerts_controller = AlertsController()
        self._token = None
        self._token_timestamp = None

        # Create a persistent session
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 2
        print("DashboardController initialized")

    def __del__(self):
        """Cleanup method"""
        if hasattr(self, 'session'):
            self.session.close()
            print("DashboardController session closed")

    def on_config_change(self, new_config: WazuhConfig):
        """Observer method for configuration changes"""
        print(f"DashboardController: Received new configuration. URL: {new_config.url}")
        try:
            # Update configuration
            self.wazuh_config = new_config
            self.alerts_controller.wazuh_config = new_config

            # Reset connection-related attributes
            self._token = None
            self._token_timestamp = None

            # Close existing session and create new one
            self.session.close()
            self.session = requests.Session()
            self.session.verify = False
            self.session.timeout = 2

            print("DashboardController: Updating dashboard with new configuration...")
            # Refresh dashboard with new settings
            self.update_dashboard()
            print("DashboardController: Dashboard updated with new configuration")

        except Exception as e:
            print(f"DashboardController: Error updating configuration: {e}")
            self.view.show_message("Failed to update dashboard with new settings", "red")

    def get_wazuh_token(self):
        """Get authentication token from Wazuh"""
        try:
            # Use existing token if valid
            if self._token and self._token_timestamp:
                if (datetime.now() - self._token_timestamp).seconds < 3000:
                    return self._token

            print("DashboardController: Requesting new Wazuh token...")
            base_url = f"https://{self.wazuh_config.url}"
            if not base_url.endswith(':55000'):
                base_url = f"{base_url}:55000"

            response = self.session.post(
                f"{base_url}/security/user/authenticate",
                auth=(self.wazuh_config.username, self.wazuh_config.password),
                timeout=2
            )

            if response.status_code == 200:
                self._token = response.json()['data']['token']
                self._token_timestamp = datetime.now()
                self.session.headers.update({'Authorization': f'Bearer {self._token}'})
                print("DashboardController: Successfully obtained new token")
                return self._token

            print(f"DashboardController: Failed to get token. Status: {response.status_code}")
            return None
        except Exception as e:
            print(f"DashboardController: Token error: {e}")
            return None

    def get_system_status(self):
        """Get system status focusing on critical services"""
        try:
            print("DashboardController: Checking system status...")
            data = self.fetch_data("manager/status")
            if data and 'data' in data and 'affected_items' in data['data'] and data['data']['affected_items']:
                services = data['data']['affected_items'][0]

                # Critical services that must be running
                critical_services = [
                    'wazuh-analysisd',
                    'wazuh-execd',
                    'wazuh-remoted',
                    'wazuh-syscheckd',
                    'wazuh-modulesd',
                    'wazuh-db',
                    'wazuh-apid'
                ]

                critical_services_status = all(
                    services.get(service) == 'running'
                    for service in critical_services
                )

                status = "Secure" if critical_services_status else "Warning"
                print(f"DashboardController: System status: {status}")
                return status
            return "Unknown"
        except Exception as e:
            print(f"DashboardController: Status error: {e}")
            return "Unknown"

    def fetch_data(self, endpoint, params=None):
        """Fetch data from Wazuh API with error handling"""
        try:
            if not self._token:
                if not self.get_wazuh_token():
                    return None

            base_url = f"https://{self.wazuh_config.url}"
            if not base_url.endswith(':55000'):
                base_url = f"{base_url}:55000"

            response = self.session.get(
                f"{base_url}/{endpoint}",
                params=params,
                timeout=2
            )

            if response.status_code == 200:
                return response.json()
            print(f"DashboardController: Error response from {endpoint}: {response.status_code}")
            return None
        except requests.exceptions.Timeout:
            print(f"DashboardController: Timeout fetching {endpoint}")
            return None
        except Exception as e:
            print(f"DashboardController: Error fetching {endpoint}: {e}")
            return None

    def update_dashboard(self):
        """Update dashboard data using AlertsController's logic"""
        print("\n=== Starting Dashboard Update ===")
        print("DashboardController: Initializing dashboard update process...")

        try:
            # Get alerts using AlertsController's method
            alerts = self.alerts_controller.get_alerts()

            # Count alerts by severity
            active_threats = sum(1 for alert in alerts if alert['actions'] == 'high')
            total_alerts = len(alerts)

            # Get current time
            current_time = datetime.now().strftime("%I:%M %p")

            # Update dashboard statistics
            stats = {
                "active_threats": active_threats,
                "last_scan": f"Last checked at {current_time}",
                "system_status": self.get_system_status(),
                "total_alerts": total_alerts
            }

            print(f"DashboardController: Dashboard update complete. Stats: {stats}")
            self.view.update_stats(stats)

        except Exception as e:
            print(f"DashboardController: Error in update_dashboard: {e}")
            self.view.show_message(f"Error updating dashboard: {e}", "red")