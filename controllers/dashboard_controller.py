# controllers/dashboard_controller.py
import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from controllers.alerts_controller import AlertsController
from models.wazuh_config import WazuhConfig
from utils.alert_manager import AlertManager

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from utils.config_manager import ConfigManager


class DashboardController:
    def __init__(self):
        print("Initializing DashboardController...")
        self.view = None
        self.config_manager = ConfigManager()
        self.wazuh_config = self.config_manager.wazuh_config
        self._token = None
        self._token_timestamp = None
        self.acknowledged_alerts = set()  # Add acknowledged alerts set
        self.windows_agent_id = None  # Initialize but don't fetch yet
        self.alert_manager = AlertManager()
        self.alert_manager.add_observer(self)

        # Create a persistent session
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 2
        print("DashboardController initialized")

        # Load acknowledged alerts
        self.load_acknowledged_alerts()
        print("DashboardController initialized")

        # Add as observer
        self.config_manager.add_wazuh_observer(self.on_config_change)

    def on_alerts_updated(self):
        """Called when alerts are acknowledged"""
        self.update_dashboard()

    def load_acknowledged_alerts(self):
        """Load acknowledged alerts from file"""
        try:
            with open('acknowledged_alerts.txt', 'r') as f:
                self.acknowledged_alerts = set(line.strip() for line in f)
            print(f"Loaded {len(self.acknowledged_alerts)} acknowledged alerts")
        except FileNotFoundError:
            print("No acknowledged alerts file found")
            self.acknowledged_alerts = set()

    def get_windows_agent_id(self):
        """Get the ID of the Windows agent"""
        try:
            if self.windows_agent_id:  # Return if already set
                return self.windows_agent_id

            print("\n=== Getting Windows Agent ID ===")
            if not self.get_wazuh_token():
                print("Failed to get token for Windows agent ID fetch")
                return None

            queries = [
                {'q': 'os.platform=windows', 'select': 'id,name'},
                {'q': 'os.name=windows', 'select': 'id,name'},
                None
            ]

            for query in queries:
                response = self.fetch_data('agents', query)
                if response and 'data' in response:
                    agents = response['data'].get('affected_items', [])
                    for agent in agents:
                        if agent.get('os', {}).get('platform') == 'windows' or \
                                agent.get('os', {}).get('name', '').lower() == 'windows':
                            self.windows_agent_id = agent['id']
                            print(f"Found Windows agent with ID: {self.windows_agent_id}")
                            return self.windows_agent_id

            print("No Windows agents found")
            return None
        except Exception as e:
            print(f"Error getting Windows agent ID: {e}")
            return None

    def set_view(self, view):
        """Set the view for this controller"""
        self.view = view
        print("View set for DashboardController")

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
        """Update dashboard data by directly fetching alerts"""
        print("\n=== Starting Dashboard Update ===")
        print("DashboardController: Initializing dashboard update process...")

        if not self.view:
            print("Error: View not set")
            return

        try:
            all_alerts = []
            windows_id = self.get_windows_agent_id()

            if windows_id and self.get_wazuh_token():
                print(f"Fetching alerts for Windows agent ID: {windows_id}")
                syscheck_response = self.fetch_data(f'syscheck/{windows_id}', {
                    'limit': 100,
                    'sort': 'date'
                })

                if syscheck_response and 'data' in syscheck_response:
                    items = syscheck_response['data'].get('affected_items', [])
                    print(f"Found {len(items)} potential alerts")

                    for item in items:
                        try:
                            file_path = item.get('file', '').lower()
                            event_type = item.get('type', '').lower()
                            timestamp_str = item.get('date', '')

                            # Check if alert is acknowledged using AlertManager
                            alert_id = f"{timestamp_str}_{file_path}"
                            if self.alert_manager.is_acknowledged(alert_id):
                                print(f"Skipping acknowledged alert: {alert_id}")
                                continue

                            # Process alert only if not acknowledged
                            is_suspicious = False
                            severity = "low"
                            alert_type = "File Change"

                            if any(path in file_path for path in self.wazuh_config.suspicious_paths):
                                is_suspicious = True
                                severity = "medium"

                            if event_type in ['modified', 'deleted']:
                                is_suspicious = True
                                severity = "high"

                            if 'readme' in file_path and 'ransom' in file_path:
                                is_suspicious = True
                                severity = "high"
                                alert_type = "Ransomware Note Detected"

                            if is_suspicious:
                                all_alerts.append({
                                    "timestamp": timestamp_str,
                                    "actions": severity,
                                    "type": alert_type,
                                    "file": file_path
                                })

                        except Exception as e:
                            print(f"Error processing alert item: {e}")
                            continue

                    # Sort alerts by severity
                    sorted_alerts = sorted(
                        all_alerts,
                        key=lambda x: {'high': 0, 'medium': 1, 'low': 2}[x['actions']]
                    )
                    all_alerts = sorted_alerts

                print(f"Processing complete. Found {len(all_alerts)} unacknowledged alerts")

            # Count alerts
            total_alerts = len(all_alerts)
            active_threats = sum(1 for alert in all_alerts if alert.get('actions') == 'high')

            current_time = datetime.now().strftime("%I:%M %p")

            stats = {
                "active_threats": active_threats,
                "last_scan": f"Last checked at {current_time}",
                "system_status": self.get_system_status(),
                "total_alerts": total_alerts
            }

            print(f"Updating dashboard with stats: {stats}")
            self.view.update_stats(stats)
            print("Dashboard update complete")

        except Exception as e:
            print(f"DashboardController: Error in update_dashboard: {e}")
            if self.view:
                self.view.show_message(f"Error updating dashboard: {e}", "red")
