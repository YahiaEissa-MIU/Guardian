# models/incident_history_model.py
import sys
import traceback
from dataclasses import dataclass, field
from datetime import datetime
import json
import aiohttp
import asyncio
import csv
import logging
import os
from typing import List, Optional


@dataclass
class IncidentHistoryModel:
    shuffle_url: str = field(default="")
    shuffle_api_key: str = field(default="")
    workflow_name: str = field(default="")
    workflow_id: Optional[str] = field(default=None)
    incidents: List[dict] = field(default_factory=list)
    observers: List[callable] = field(default_factory=list)
    last_modified: datetime = field(default_factory=datetime.now)
    is_configured: bool = field(default=False)

    def __post_init__(self):
        """Post initialization validation"""
        self.is_configured = bool(
            self.shuffle_url and
            self.shuffle_api_key and
            self.workflow_name
        )
        print(f"IncidentHistoryModel initialized with is_configured={self.is_configured}")

    def add_observer(self, observer):
        """Adds an observer to the model"""
        if observer not in self.observers:
            self.observers.append(observer)

    def notify_observers(self):
        """Notifies all observers of data changes"""
        for observer in self.observers:
            observer()

    async def get_workflow_id(self):
        """Fetches workflow ID based on workflow name"""
        try:
            if not self.shuffle_url.startswith('http'):
                url = f"http://{self.shuffle_url}"
            else:
                url = self.shuffle_url

            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.shuffle_api_key}",
                    "Content-Type": "application/json"
                }
                api_url = f"{url}/api/v1/workflows"
                print(f"Fetching workflows from: {api_url}")
                print(f"Using headers: {headers}")

                async with session.get(api_url, headers=headers) as response:
                    print(f"Response status: {response.status}")
                    if response.status == 200:
                        workflows = await response.json()
                        for workflow in workflows:
                            if workflow.get('name') == self.workflow_name:
                                self.workflow_id = workflow.get('id')
                                print(f"Found workflow ID: {self.workflow_id}")
                                return self.workflow_id
                        print(f"No workflow found with name: {self.workflow_name}")
                        return None
                    else:
                        error_text = await response.text()
                        print(f"Failed to fetch workflows: {response.status}")
                        print(f"Error details: {error_text}")
                        return None
        except Exception as e:
            print(f"Error fetching workflow ID: {e}")
            return None

    async def validate_connection(self) -> bool:
        """Validates the Shuffle connection and workflow name"""
        if not all([self.shuffle_url, self.shuffle_api_key, self.workflow_name]):
            print("Missing configuration parameters")
            return False

        try:
            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                headers = {"Authorization": f"Bearer {self.shuffle_api_key}"}

                url = self.shuffle_url
                if not url.startswith('http'):
                    url = f"http://{url}"

                api_url = f"{url}/api/v1/workflows"
                print(f"Testing connection to: {api_url}")

                async with session.get(api_url, headers=headers) as response:
                    print(f"Response status: {response.status}")
                    if response.status == 200:
                        workflows = await response.json()
                        workflow_exists = any(
                            workflow.get('name') == self.workflow_name
                            for workflow in workflows
                        )

                        if workflow_exists:
                            self.is_configured = True
                            print("Connection and workflow validation successful")
                            return True
                        else:
                            print(f"Workflow '{self.workflow_name}' not found")
                            return False
                    print(f"Connection failed: {await response.text()}")
                    return False
        except Exception as e:
            print(f"Validation error: {e}")
            return False

    async def fetch_shuffle_incidents(self):
        """Fetches incidents from Shuffle SOAR"""
        print("\n=== Fetching Shuffle Incidents ===")

        if not self.workflow_id:
            print("No workflow ID, fetching...")
            self.workflow_id = await self.get_workflow_id()
            if not self.workflow_id:
                print("Failed to get workflow ID")
                return None

        url = self.shuffle_url
        if not url.startswith(('http://', 'https://')):
            url = f"http://{url}"

        headers = {
            "Authorization": f"Bearer {self.shuffle_api_key}",
            "Content-Type": "application/json"
        }

        try:
            timeout = aiohttp.ClientTimeout(total=30)  # Increased timeout
            async with aiohttp.ClientSession(timeout=timeout) as session:
                api_url = f"{url}/api/v1/workflows/{self.workflow_id}/executions"
                print(f"Requesting: {api_url}")
                print(f"Headers: {headers}")

                async with session.get(api_url, headers=headers) as response:
                    print(f"Response Status: {response.status}")

                    if response.status == 200:
                        data = await response.json()
                        print(f"Raw data length: {len(data) if data else 0}")

                        if not data:
                            print("No data received from Shuffle")
                            return []

                        transformed = self._transform_shuffle_data(data)
                        print(f"Transformed incidents: {len(transformed)}")
                        return transformed
                    else:
                        error_text = await response.text()
                        print(f"Error response: {error_text}")
                        return None

        except aiohttp.ClientError as e:
            print(f"Network error: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            traceback.print_exc()
            return None

    def _transform_shuffle_data(self, shuffle_data):
        """Transforms Shuffle execution data into incident format"""
        transformed_incidents = []
        print(f"\nTransforming data:")
        print(f"Input data length: {len(shuffle_data) if shuffle_data else 0}")

        try:
            for execution in shuffle_data:
                results = execution.get('results', [])
                print(f"Processing execution with {len(results)} results")
                for result in results:
                    try:
                        result_data = result.get('result', {})
                        if isinstance(result_data, str):
                            result_data = json.loads(result_data)

                        message = result_data.get('message', '')
                        print(f"Processing message: {message[:100]}...")  # First 100 chars
                        if 'Generated incident:' in message:
                            incident_json = message.split('Generated incident:', 1)[1].strip()
                            incident_data = json.loads(incident_json)

                            transformed_incidents.append({
                                "Date": datetime.fromtimestamp(incident_data['timestamp']).strftime("%Y-%m-%d %H:%M"),
                                "Incident": incident_data['type'],
                                "Action": incident_data['action_taken']
                            })
                            print(f"Added incident: {transformed_incidents[-1]}")
                    except Exception as e:
                        print(f"Error processing result: {e}")
                        continue
        except Exception as e:
            print(f"Error transforming data: {e}")

        print(f"Total transformed incidents: {len(transformed_incidents)}")
        return transformed_incidents

    def get_incidents(self, filter_type=None, filter_value=None):
        """Returns filtered list of incidents based on criteria"""
        if not filter_type or not filter_value or filter_type == "All":
            return self.incidents

        filtered = []
        for incident in self.incidents:
            if filter_type == "Date" and filter_value in incident["Date"]:
                filtered.append(incident)
            elif filter_type == "Incident" and filter_value.lower() in incident["Incident"].lower():
                filtered.append(incident)
            elif filter_type == "Action" and filter_value.lower() in incident["Action"].lower():
                filtered.append(incident)
        return filtered

    def sync_incidents(self):
        """Synchronizes incidents with Shuffle SOAR"""
        try:
            print("\n=== Starting Incident Sync ===")
            print(f"Current Configuration State:")
            print(f"URL: {self.shuffle_url}")
            print(f"API Key: {'Set' if self.shuffle_api_key else 'Not Set'}")
            print(f"Workflow Name: {self.workflow_name}")
            print(f"Workflow ID: {self.workflow_id}")
            print(f"Is Configured: {self.is_configured}")

            if not self.is_configured:
                print("Configuration incomplete, attempting to load from file...")
                loaded_config = self.load_from_file()
                if loaded_config and loaded_config.is_configured:
                    self.shuffle_url = loaded_config.shuffle_url
                    self.shuffle_api_key = loaded_config.shuffle_api_key
                    self.workflow_name = loaded_config.workflow_name
                    self.is_configured = True
                    print("Successfully loaded configuration from file")
                else:
                    print("Failed to load valid configuration")
                    return False

            # Validate URL format
            if not self.shuffle_url.startswith(('http://', 'https://')):
                self.shuffle_url = f"http://{self.shuffle_url}"
                print(f"Updated URL to: {self.shuffle_url}")

            # Create new event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                # First validate connection
                connection_valid = loop.run_until_complete(self.validate_connection())
                if not connection_valid:
                    print("Failed to validate Shuffle connection")
                    return False

                # Then fetch incidents
                shuffle_incidents = loop.run_until_complete(self.fetch_shuffle_incidents())
                if shuffle_incidents is None:
                    print("Failed to fetch incidents")
                    return False

                print(f"Successfully fetched {len(shuffle_incidents)} incidents")
                self.incidents = shuffle_incidents
                self.notify_observers()
                return True

            finally:
                loop.close()

        except Exception as e:
            print(f"Error in sync_incidents: {str(e)}")
            traceback.print_exc()
            return False

    def update_shuffle_config(self, url: str, api_key: str, workflow_name: str) -> bool:
        """Updates Shuffle configuration"""
        try:
            self.shuffle_url = url.strip()
            self.shuffle_api_key = api_key.strip()
            self.workflow_name = workflow_name.strip()
            self.workflow_id = None  # Reset workflow ID
            self.last_modified = datetime.now()

            # Set is_configured if all required fields are present
            self.is_configured = all([
                self.shuffle_url,
                self.shuffle_api_key,
                self.workflow_name
            ])

            return True
        except Exception as e:
            print(f"Error updating Shuffle config: {e}")
            return False

    def export_to_csv(self, filename="incident_history.csv"):
        """Exports incidents to a CSV file"""
        try:
            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["Date", "Incident", "Action"])
                writer.writeheader()
                writer.writerows(self.incidents)
            return True, f"Exported successfully to {filename}"
        except Exception as e:
            logging.error(f"Error exporting to CSV: {str(e)}")
            return False, f"Error exporting file: {str(e)}"

    @classmethod
    def create_empty(cls) -> 'IncidentHistoryModel':
        """Creates a new instance with empty credentials"""
        return cls()

    @classmethod
    def load_from_file(cls, filepath: str) -> 'IncidentHistoryModel':
        """Loads configuration from file"""
        try:
            print(f"Loading configuration from {filepath}")
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    config_data = json.load(f)
                    print(f"Loaded data from file: {config_data}")

                    instance = cls(
                        shuffle_url=config_data.get('shuffle_url', ''),
                        shuffle_api_key=config_data.get('shuffle_api_key', ''),
                        workflow_name=config_data.get('workflow_name', ''),
                        last_modified=datetime.fromisoformat(
                            config_data.get('last_modified', datetime.now().isoformat())
                        )
                    )

                    # Set is_configured based on actual values
                    instance.is_configured = bool(
                        instance.shuffle_url and
                        instance.shuffle_api_key and
                        instance.workflow_name
                    )

                    print(f"Created instance with:")
                    print(f"URL: {instance.shuffle_url}")
                    print(f"API Key set: {'Yes' if instance.shuffle_api_key else 'No'}")
                    print(f"Workflow Name: {instance.workflow_name}")
                    print(f"Is Configured: {instance.is_configured}")

                    return instance

            print(f"No configuration file found at {filepath}, creating empty configuration")
            return cls.create_empty()
        except Exception as e:
            print(f"Error loading Shuffle config: {e}")
            return cls.create_empty()

    def save_to_file(self, filepath: str = None) -> bool:
        """Saves current configuration to file"""
        try:
            if filepath is None:
                if sys.platform == "win32":
                    app_data = os.path.join(os.environ['APPDATA'], 'Guardian')
                else:
                    app_data = os.path.join(os.path.expanduser('~'), '.guardian')
                filepath = os.path.join(app_data, 'shuffle_config.json')

            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            # Update is_configured based on current values
            self.is_configured = bool(
                self.shuffle_url and
                self.shuffle_api_key and
                self.workflow_name
            )

            config_dict = {
                "shuffle_url": self.shuffle_url,
                "shuffle_api_key": self.shuffle_api_key,
                "workflow_name": self.workflow_name,
                "last_modified": self.last_modified.isoformat(),
                "is_configured": self.is_configured
            }

            print(f"Saving Shuffle config to: {filepath}")
            print(f"Config data: {config_dict}")

            with open(filepath, 'w') as f:
                json.dump(config_dict, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving Shuffle config: {e}")
            return False

    def validate_config(self):
        """Validates the current configuration"""
        if not all([self.shuffle_url, self.shuffle_api_key, self.workflow_name]):
            print("Missing required configuration parameters")
            return False

        # Basic URL validation
        if not self.shuffle_url.startswith(('http://', 'https://')):
            self.shuffle_url = f"http://{self.shuffle_url}"

        # Basic API key validation
        if len(self.shuffle_api_key) < 32:  # Assuming minimum length for API key
            print("API key appears invalid")
            return False

        self.is_configured = True
        return True

    def reload_config(self):
        """Reloads configuration from file"""
        loaded_config = self.load_from_file()
        if loaded_config and loaded_config.is_configured:
            self.shuffle_url = loaded_config.shuffle_url
            self.shuffle_api_key = loaded_config.shuffle_api_key
            self.workflow_name = loaded_config.workflow_name
            self.is_configured = True
            return True
        return False

