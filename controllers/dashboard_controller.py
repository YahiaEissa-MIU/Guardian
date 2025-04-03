import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class DashboardController:
    def __init__(self, view):
        self.view = view
        self.wazuh_base_url = "https://192.168.1.5:55000"
        self.wazuh_auth = {
            'user': 'wazuh-wui',
            'password': '1p.xwBLv9W*VwXGmwiYWn**Z9VwNLSn8'
        }
        self.verify_ssl = False
        self._token = None
        self._token_timestamp = None
        # Create a persistent session
        self.session = requests.Session()
        # Configure session with default settings
        self.session.verify = False
        self.session.timeout = 2  # Set default timeout to 2 seconds

    def __del__(self):
        """Cleanup method"""
        if hasattr(self, 'session'):
            self.session.close()

    def get_wazuh_token(self):
        """Get authentication token from Wazuh"""
        try:
            # Use existing token if valid
            if self._token and self._token_timestamp:
                if (datetime.now() - self._token_timestamp).seconds < 3000:
                    return self._token

            response = self.session.post(
                f"{self.wazuh_base_url}/security/user/authenticate",
                auth=(self.wazuh_auth['user'], self.wazuh_auth['password']),
                timeout=2
            )
            if response.status_code == 200:
                self._token = response.json()['data']['token']
                self._token_timestamp = datetime.now()
                # Add token to session headers for subsequent requests
                self.session.headers.update({'Authorization': f'Bearer {self._token}'})
                return self._token
            return None
        except Exception as e:
            print(f"Token error: {e}")
            return None

    def fetch_data(self, endpoint, params=None):
        """Fetch data from Wazuh API with error handling"""
        try:
            response = self.session.get(
                f"{self.wazuh_base_url}/{endpoint}",
                params=params,
                timeout=2
            )
            return response.json() if response.status_code == 200 else None
        except requests.exceptions.Timeout:
            print(f"Timeout fetching {endpoint}")
            return None
        except Exception as e:
            print(f"Error fetching {endpoint}: {e}")
            return None

    def get_system_status(self):
        """Get system status focusing on critical services"""
        try:
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

                return "Secure" if critical_services_status else "Warning"
            return "Unknown"
        except Exception as e:
            print(f"Status error: {e}")
            return "Unknown"

    def format_time_difference(self, timestamp):
        """Format time difference in a human-readable format"""
        try:
            now = datetime.now()
            if isinstance(timestamp, (int, float)):
                timestamp = datetime.fromtimestamp(timestamp)

            # Check if the timestamp is from the future (like our 2025 date)
            if timestamp.year > now.year:
                return "Recently"  # or "Active" or whatever makes sense for your use case

            diff = now - timestamp
            seconds = int(diff.total_seconds())

            if seconds < 30:
                return "Just now"
            elif seconds < 60:
                return "Less than a minute ago"
            elif seconds < 3600:
                minutes = seconds // 60
                return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
            elif seconds < 86400:  # 24 hours
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                if minutes > 0:
                    return f"{hours} hour{'s' if hours != 1 else ''} and {minutes} minute{'s' if minutes != 1 else ''} ago"
                return f"{hours} hour{'s' if hours != 1 else ''} ago"
            elif seconds < 604800:  # 7 days
                days = seconds // 86400
                hours = (seconds % 86400) // 3600
                if hours > 0:
                    return f"{days} day{'s' if days != 1 else ''} and {hours} hour{'s' if hours != 1 else ''} ago"
                return f"{days} day{'s' if days != 1 else ''} ago"
            else:
                weeks = seconds // 604800
                days = (seconds % 604800) // 86400
                if days > 0:
                    return f"{weeks} week{'s' if weeks != 1 else ''} and {days} day{'s' if days != 1 else ''} ago"
                return f"{weeks} week{'s' if weeks != 1 else ''} ago"
        except Exception as e:
            print(f"Error formatting time: {e}")
            return "Unknown"

    def update_dashboard(self):
        """Update dashboard data concurrently"""
        try:
            if not self.get_wazuh_token():
                self.view.show_message("Failed to authenticate with Wazuh", "red")
                return

            # Define data fetching tasks
            tasks = {
                'alerts': ('alerts', {'level>': '7', 'timeframe': '24h'}),
                'status': ('manager/status', None),
                'summary': ('alerts/summary', None)
            }

            # Fetch all data concurrently
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = {
                    name: executor.submit(self.fetch_data, endpoint, params)
                    for name, (endpoint, params) in tasks.items()
                }

                results = {
                    name: future.result(timeout=3)
                    for name, future in futures.items()
                }

            # Get scan status
            scan_status = self.fetch_data('syscheck/000/last_scan')
            print("Scan info response:", scan_status)

            # Get current time in 12-hour format
            current_time = datetime.now().strftime("%I:%M %p")  # e.g., "02:30 PM"

            # Determine scan status text
            if scan_status and 'data' in scan_status:
                if 'affected_items' in scan_status['data'] and scan_status['data']['affected_items']:
                    scan_data = scan_status['data']['affected_items'][0]
                    if scan_data.get('end'):
                        scan_text = f"Last checked at {current_time}"
                    elif scan_data.get('start'):
                        scan_text = f"Scanning now ({current_time})"
                    else:
                        scan_text = f"Waiting for scan ({current_time})"
                else:
                    scan_text = f"Ready for scan ({current_time})"
            else:
                scan_text = f"System check at {current_time}"

            # Process results
            data = {
                "active_threats": len(results['alerts']['data']['affected_items']) if results['alerts'] else 0,
                "last_scan": scan_text,
                "system_status": self.get_system_status(),
                "total_alerts": (
                    results['summary']['data']['total_affected_items']
                    if results['summary'] and 'data' in results['summary']
                    else 0
                )
            }

            print(f"Final scan status: {data['last_scan']}")
            self.view.update_stats(data)

        except Exception as e:
            self.view.show_message(f"Error updating dashboard: {e}", "red")
