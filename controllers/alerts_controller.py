# controllers/alerts_controller.py

import requests
import urllib3
from datetime import datetime
from utils.alert_manager import AlertManager
from utils.config_manager import ConfigManager

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class AlertsController:
    def __init__(self, view=None):
        print("Initializing AlertsController...")
        self.view = view
        self.config_manager = ConfigManager()
        self.wazuh_config = self.config_manager.wazuh_config
        self._token = None
        self._token_timestamp = None
        self.windows_agent_id = None
        self.alert_manager = AlertManager()

        # Create a persistent session
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 2

        # Initialize with system checks if config exists
        if self.wazuh_config and self.wazuh_config.url:
            self.get_windows_agent_id()

    def set_view(self, view):
        """Set the view and trigger initial update"""
        self.view = view
        if self.view:
            self.update_alerts()

    def get_wazuh_token(self):
        """Get authentication token from Wazuh"""
        try:
            if self._token and self._token_timestamp:
                if (datetime.now() - self._token_timestamp).seconds < 3000:
                    return self._token

            if not self.wazuh_config or not self.wazuh_config.url:
                print("No valid configuration available")
                return None

            print("Requesting new Wazuh token...")
            base_url = f"https://{self.wazuh_config.url}"
            if not base_url.endswith(':55000'):
                base_url = f"{base_url}:55000"

            response = self.session.post(
                f"{base_url}/security/user/authenticate",
                auth=(self.wazuh_config.username, self.wazuh_config.password)
            )

            if response.status_code == 200:
                self._token = response.json()['data']['token']
                self._token_timestamp = datetime.now()
                self.session.headers.update({'Authorization': f'Bearer {self._token}'})
                print("Successfully obtained token")
                return self._token

            print(f"Failed to get token. Status: {response.status_code}")
            return None
        except Exception as e:
            print(f"Error getting token: {e}")
            return None

    def get_windows_agent_id(self):
        """Get the ID of the Windows agent"""
        try:
            if self.windows_agent_id:  # Return if already set
                return self.windows_agent_id

            if self.get_wazuh_token():
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
            print(f"Error fetching agents: {e}")
            return None

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
                params=params
            )

            if response.status_code == 200:
                return response.json()
            print(f"Error response from {endpoint}: {response.status_code}")
            return None
        except Exception as e:
            print(f"Error fetching {endpoint}: {e}")
            return None

    def update_alerts(self):
        """Update alerts display using immediate checks"""
        print("\n=== Starting Alerts Update ===")
        print("AlertsController: Initializing alerts update process...")

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
                        file_path = item.get('file', '').lower()
                        event_type = item.get('type', '').lower()
                        timestamp_str = item.get('date', '')

                        alert_id = f"{timestamp_str}_{file_path}"
                        if self.alert_manager.is_acknowledged(alert_id):
                            print(f"Skipping acknowledged alert: {alert_id}")
                            continue

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

                    sorted_alerts = sorted(all_alerts,
                                           key=lambda x: {'high': 0, 'medium': 1, 'low': 2}[x['actions']])
                    print(f"Processing complete. Found {len(sorted_alerts)} unacknowledged alerts")

                    self.view.update_alerts(sorted_alerts)
                else:
                    print("No syscheck response or data")
                    self.view.update_alerts([])
            else:
                print("No windows ID or token available")
                self.view.update_alerts([])

        except Exception as e:
            print(f"Error in alerts update: {e}")
            self.view.update_alerts([])

    def acknowledge_alert(self):
        """Handle alert acknowledgment"""
        if self.view and self.view.tree:
            selected_item = self.view.tree.focus()
            if selected_item:
                values = self.view.tree.item(selected_item)['values']
                alert_id = f"{values[0]}_{values[3]}"
                self.alert_manager.add_acknowledged_alert(alert_id)
                self.update_alerts()

    def on_config_change(self, new_config):
        """Handle configuration updates"""
        print(f"AlertsController: Received new configuration. URL: {new_config.url}")
        try:
            self.wazuh_config = new_config
            self._token = None
            self._token_timestamp = None

            self.session.close()
            self.session = requests.Session()
            self.session.verify = False
            self.session.timeout = 2

            if self.wazuh_config.url:
                self.get_windows_agent_id()
                self.update_alerts()
        except Exception as e:
            print(f"Error updating configuration: {e}")