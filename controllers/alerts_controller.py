# alerts_controller.py
import requests
import urllib3
from datetime import datetime
import logging

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class AlertsController:
    def __init__(self, view=None):
        print("Initializing AlertsController...")
        self.view = view
        self.wazuh_base_url = "https://192.168.1.5:55000"
        self.wazuh_auth = {
            'user': 'wazuh-wui',
            'password': '1p.xwBLv9W*VwXGmwiYWn**Z9VwNLSn8'
        }
        self.verify_ssl = False
        self._token = None
        self._token_timestamp = None
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 10
        self.acknowledged_alerts = set()
        self.windows_agent_id = None

        # Ransomware-specific patterns
        self.ransomware_extensions = [
            '.encrypted', '.crypto', '.locked', '.crypted', '.crypt',
            '.wallet', '.ransom', '.write', '.wcry', '.wncry', '.wnry',
            '.tesla', '.locky', '.zepto', '.cerber', '.sage'
        ]

        self.suspicious_paths = [
            'desktop',
            'documents',
            'downloads',
            'pictures',
            'appdata\\local',
            'appdata\\roaming',
            'program files',
            'windows\\system32'
        ]

        # Initialize with system checks
        self.verify_api_configuration()
        self.get_windows_agent_id()

    def verify_api_configuration(self):
        """Verify Wazuh API configuration"""
        print("\n=== Verifying API Configuration ===")
        try:
            if self.get_wazuh_token():
                response = self.fetch_data('manager/configuration')
                if response and 'data' in response:
                    print("API Configuration available")
                    return True
        except Exception as e:
            print(f"Error verifying API configuration: {e}")
        return False

    def get_wazuh_token(self):
        """Get authentication token from Wazuh"""
        print("\n=== Getting Wazuh Token ===")
        try:
            if self._token and self._token_timestamp:
                if (datetime.now() - self._token_timestamp).seconds < 3000:
                    print("Using existing token")
                    return self._token

            print("Requesting new Wazuh token...")
            response = self.session.post(
                f"{self.wazuh_base_url}/security/user/authenticate",
                auth=(self.wazuh_auth['user'], self.wazuh_auth['password']),
                verify=False
            )

            if response.status_code == 200:
                self._token = response.json()['data']['token']
                self._token_timestamp = datetime.now()
                self.session.headers.update({'Authorization': f'Bearer {self._token}'})
                print("Successfully obtained token")
                return self._token

            print(f"Failed to get token. Response: {response.text}")
            return None
        except Exception as e:
            print(f"Error getting token: {e}")
            return None

    def get_windows_agent_id(self):
        """Get the ID of the Windows agent"""
        print("\n=== Getting Windows Agent ID ===")
        try:
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
                                return

                print("No Windows agents found")
        except Exception as e:
            print(f"Error getting Windows agent ID: {e}")

    def fetch_data(self, endpoint, params=None):
        """Fetch data from Wazuh API with error handling"""
        try:
            print(f"\nFetching data from endpoint: {endpoint}")
            print(f"Parameters: {params}")

            response = self.session.get(
                f"{self.wazuh_base_url}/{endpoint}",
                params=params
            )

            print(f"Response status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Response data structure: {list(data.keys())}")
                if 'data' in data:
                    print(f"Data structure: {list(data['data'].keys())}")
                return data
            print(f"Error response: {response.text}")
            return None
        except Exception as e:
            print(f"Error fetching {endpoint}: {e}")
            return None

    def get_alerts(self):
        """Enhanced ransomware detection using available FIM data"""
        print("\n=== Fetching Enhanced Ransomware Indicators ===")
        if not self.get_wazuh_token() or not self.windows_agent_id:
            return []

        try:
            all_alerts = []

            # Track patterns that indicate ransomware
            pattern_tracking = {
                'mass_operations': {'count': 0, 'timeframe': datetime.now()},
                'critical_files': set(),
                'extension_changes': set(),
                'system_files': set()
            }

            # Fetch FIM events
            syscheck_response = self.fetch_data(f'syscheck/{self.windows_agent_id}', {
                'limit': 100,
                'sort': 'date'
            })

            if syscheck_response and 'data' in syscheck_response:
                items = syscheck_response['data'].get('affected_items', [])

                for item in items:
                    try:
                        file_path = item.get('file', '').lower()
                        event_type = item.get('type', '').lower()

                        # Convert timestamp string to datetime object
                        timestamp_str = item.get('date', '')
                        try:
                            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        except (ValueError, AttributeError):
                            timestamp = datetime.now()

                        # Check for ransomware indicators
                        is_suspicious = False
                        severity = "low"
                        alert_type = "File Change"

                        # Check suspicious paths
                        if any(path in file_path for path in self.suspicious_paths):
                            is_suspicious = True
                            severity = "medium"

                        # Check ransomware extensions
                        if any(ext in file_path for ext in self.ransomware_extensions):
                            is_suspicious = True
                            severity = "high"
                            alert_type = "Potential Ransomware Activity"

                        # Check mass file operations
                        if event_type in ['modified', 'deleted']:
                            is_suspicious = True
                            severity = "high"

                        # Check for ransom notes
                        if 'readme' in file_path and 'ransom' in file_path:
                            is_suspicious = True
                            severity = "high"
                            alert_type = "Ransomware Note Detected"

                        if is_suspicious:
                            alert_id = f"{timestamp_str}_{file_path}_{event_type}"
                            if alert_id not in self.acknowledged_alerts:
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

                print(f"Found {len(sorted_alerts)} potential ransomware indicators")
                return sorted_alerts

        except Exception as e:
            print(f"Error in get_alerts: {e}")
            return []

    def acknowledge_alert(self):
        """Handle alert acknowledgment"""
        if self.view and self.view.tree:
            selected_item = self.view.tree.focus()
            if selected_item:
                try:
                    values = self.view.tree.item(selected_item)['values']
                    alert_id = f"{values[0]}_{values[3]}"
                    self.acknowledged_alerts.add(alert_id)
                    self.view.tree.delete(selected_item)
                    self.view.details_text.configure(state="normal")
                    self.view.details_text.delete("1.0", "end")
                    self.view.details_text.insert("1.0", "Alert acknowledged and removed")
                    self.view.details_text.configure(state="disabled")
                except Exception as e:
                    print(f"Error acknowledging alert: {e}")

    def _get_ransomware_indicators(self, file_path, event_type):
        """Analyze and return specific ransomware indicators"""
        indicators = []

        if event_type == 'modified':
            indicators.append("File content modification detected")
        if event_type == 'deleted':
            indicators.append("File deletion detected")
        if any(ext in file_path for ext in self.ransomware_extensions):
            indicators.append("Known ransomware file extension detected")
        if 'readme' in file_path.lower():
            indicators.append("Potential ransom note detected")
        if 'windows\\system32' in file_path.lower():
            indicators.append("System file manipulation detected")

        return indicators