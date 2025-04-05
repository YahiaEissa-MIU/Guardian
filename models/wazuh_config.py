# models/wazuh_config.py
from dataclasses import dataclass
from typing import List, Optional
import json
import os
from datetime import datetime


@dataclass
class WazuhConfig:
    url: str
    username: str
    password: str
    suspicious_paths: List[str]
    last_modified: datetime = None
    is_default: bool = True

    @classmethod
    def load_from_file(cls, filepath: str = "wazuh_config.json") -> 'WazuhConfig':
        default_config = {
            "url": "192.168.1.5:55000",
            "username": "wazuh-wui",
            "password": "1p.xwBLv9W*VwXGmwiYWn**Z9VwNLSn8",
            "suspicious_paths": [
                "system32",
                "program files",
                "windows",
                "desktop",
                "documents",
                "downloads",
                "pictures",
                "appdata\\local",
                "appdata\\roaming"
            ],
            "last_modified": datetime.now().isoformat()
        }

        try:
            if os.path.exists(filepath):
                print(f"Loading configuration from {filepath}")
                with open(filepath, 'r') as f:
                    config_data = json.load(f)
                    print(f"Loaded config data: {config_data}")
                    config_data['last_modified'] = datetime.fromisoformat(
                        config_data.get('last_modified', datetime.now().isoformat())
                    )
                    return cls(**config_data)
            print(f"No configuration file found at {filepath}, using defaults")
            return cls(**default_config)
        except Exception as e:
            print(f"Error loading Wazuh config: {e}")
            return cls(**default_config)

    def save_to_file(self, filepath: str = "wazuh_config.json") -> bool:
        try:
            config_dict = {
                "url": self.url,
                "username": self.username,
                "password": self.password,
                "suspicious_paths": self.suspicious_paths,
                "last_modified": self.last_modified.isoformat(),
                "is_default": self.is_default
            }
            # If it's the first change, save as default
            if self.is_default:
                with open('default_wazuh_config.json', 'w') as f:
                    json.dump(config_dict, f, indent=4)
                self.is_default = False
                config_dict["is_default"] = False

            with open(filepath, 'w') as f:
                json.dump(config_dict, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def validate_connection(self) -> bool:
        """
        Validates the Wazuh connection by attempting to authenticate and make a test API call.
        Returns True if successful, False otherwise.
        """
        import requests
        from requests.auth import HTTPBasicAuth
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        try:
            # Format the base URL
            base_url = f"https://{self.url}"
            if not base_url.endswith(':55000'):
                base_url = f"{base_url}:55000"

            print(f"Testing connection to: {base_url}")

            # Step 1: Authenticate and get token
            auth_endpoint = f"{base_url}/security/user/authenticate"
            auth_response = requests.get(
                auth_endpoint,
                auth=HTTPBasicAuth(self.username, self.password),
                verify=False,  # Skip SSL verification
                timeout=5  # Add timeout
            )

            print(f"Auth response status: {auth_response.status_code}")

            if auth_response.status_code != 200:
                print(f"Authentication failed: {auth_response.text}")
                return False

            token = auth_response.json().get('data', {}).get('token')
            if not token:
                print("No token received")
                return False

            # Step 2: Test API access with token
            headers = {
                'Authorization': f'Bearer {token}'
            }

            # Test endpoint - get manager info
            test_endpoint = f"{base_url}/manager/info"
            test_response = requests.get(
                test_endpoint,
                headers=headers,
                verify=False,
                timeout=5
            )

            print(f"Test response status: {test_response.status_code}")

            if test_response.status_code != 200:
                print(f"API test failed: {test_response.text}")
                return False

            print("Connection test successful")
            return True

        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
            return False
        except Exception as e:
            print(f"Validation error: {e}")
            return False

    def add_suspicious_path(self, path: str) -> bool:
        """Add a new suspicious path and save the configuration"""
        print(f"Adding suspicious path: {path}")
        if path and path not in self.suspicious_paths:
            self.suspicious_paths.append(path)
            return self.save_to_file()
        return False

    def remove_suspicious_path(self, path: str) -> bool:
        """Remove a suspicious path and save the configuration"""
        print(f"Removing suspicious path: {path}")
        if path in self.suspicious_paths:
            self.suspicious_paths.remove(path)
            return self.save_to_file()
        return False
