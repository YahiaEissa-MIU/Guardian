import os
from dataclasses import dataclass
from datetime import datetime
import json
import aiohttp
import asyncio
import csv
import logging


@dataclass
class IncidentHistoryModel:
    shuffle_url: str = "http://192.168.1.5:3001"
    shuffle_api_key: str = "fefe8649-81bc-4aa8-8eee-46d20fb3a8f4"
    workflow_name: str = "test"
    workflow_id: str = None
    incidents: list = None
    observers: list = None
    last_modified: datetime = None

    def __post_init__(self):
        if self.incidents is None:
            self.incidents = []
        if self.observers is None:
            self.observers = []
        if self.last_modified is None:
            self.last_modified = datetime.now()

    def add_observer(self, observer):
        """Adds an observer to the model"""
        self.observers.append(observer)

    def notify_observers(self):
        """Notifies all observers of data changes"""
        for observer in self.observers:
            observer()

    async def get_workflow_id(self):
        """Fetches workflow ID based on workflow name"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.shuffle_api_key}",
                    "Content-Type": "application/json"
                }
                url = f"{self.shuffle_url}/api/v1/workflows"
                print(f"Fetching workflows from: {url}")
                print(f"Using headers: {headers}")

                async with session.get(url, headers=headers) as response:
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
        try:
            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                headers = {"Authorization": f"Bearer {self.shuffle_api_key}"}
                url = f"{self.shuffle_url}/api/v1/workflows"

                print(f"Testing connection to: {url}")
                async with session.get(url, headers=headers) as response:
                    print(f"Response status: {response.status}")
                    if response.status == 200:
                        # Connection successful, now check if workflow exists
                        workflows = await response.json()
                        workflow_exists = any(
                            workflow.get('name') == self.workflow_name
                            for workflow in workflows
                        )

                        if workflow_exists:
                            print("Connection and workflow validation successful")
                            return True
                        else:
                            print(f"Workflow '{self.workflow_name}' not found")
                            return False
                    print(f"Connection failed: {await response.text()}")
                    return False
        except aiohttp.ClientError as e:
            print(f"Connection error: {e}")
            return False
        except Exception as e:
            print(f"Validation error: {e}")
            return False

    async def fetch_shuffle_incidents(self):
        """Fetches incidents from Shuffle SOAR"""
        if not self.workflow_id:
            self.workflow_id = await self.get_workflow_id()
            if not self.workflow_id:
                return []

        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.shuffle_api_key}",
                "Content-Type": "application/json"
            }
            try:
                url = f"{self.shuffle_url}/api/v1/workflows/{self.workflow_id}/executions"
                print(f"Fetching executions from: {url}")
                print(f"Using headers: {headers}")

                async with session.get(url, headers=headers) as response:
                    print(f"Response status: {response.status}")
                    if response.status == 200:
                        data = await response.json()
                        return self._transform_shuffle_data(data)
                    else:
                        error_text = await response.text()
                        print(f"Failed with status {response.status}")
                        print(f"Error details: {error_text}")
                        return []
            except Exception as e:
                print(f"Exception during fetch: {str(e)}")
                return []

    def _transform_shuffle_data(self, shuffle_data):
        """Transforms Shuffle execution data into incident format"""
        transformed_incidents = []
        try:
            for execution in shuffle_data:
                results = execution.get('results', [])
                for result in results:
                    try:
                        result_data = result.get('result', {})
                        if isinstance(result_data, str):
                            result_data = json.loads(result_data)

                        message = result_data.get('message', '')
                        if 'Generated incident:' in message:
                            incident_json = message.split('Generated incident:', 1)[1].strip()
                            incident_data = json.loads(incident_json)

                            transformed_incidents.append({
                                "Date": datetime.fromtimestamp(incident_data['timestamp']).strftime("%Y-%m-%d %H:%M"),
                                "Incident": incident_data['type'],
                                "Action": incident_data['action_taken']
                            })
                    except Exception as e:
                        print(f"Error processing result: {e}")
                        continue
        except Exception as e:
            print(f"Error transforming data: {e}")

        return transformed_incidents

    def get_incidents(self, filter_type=None, filter_value=None):
        """Returns filtered list of incidents based on criteria."""
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
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            shuffle_incidents = loop.run_until_complete(self.fetch_shuffle_incidents())
            loop.close()

            if shuffle_incidents:
                self.incidents = shuffle_incidents
                self.notify_observers()
                return True
            return False
        except Exception as e:
            print(f"Sync error: {e}")
            return False

    def update_shuffle_config(self, url: str, api_key: str, workflow_name: str) -> bool:
        """Updates Shuffle configuration"""
        try:
            self.shuffle_url = url
            self.shuffle_api_key = api_key
            self.workflow_name = workflow_name
            self.workflow_id = None  # Reset workflow ID so it will be fetched again
            self.last_modified = datetime.now()
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
    def load_from_file(cls, filepath: str = "shuffle_config.json") -> 'IncidentHistoryModel':
        """Loads Shuffle configuration from file"""
        default_config = {
            "shuffle_url": "http://192.168.1.5:3001",
            "shuffle_api_key": "fefe8649-81bc-4aa8-8eee-46d20fb3a8f4",
            "workflow_name": "test",
            "last_modified": datetime.now().isoformat()
        }

        try:
            if os.path.exists(filepath):
                print(f"Loading Shuffle configuration from {filepath}")
                with open(filepath, 'r') as f:
                    config_data = json.load(f)
                    config_data['last_modified'] = datetime.fromisoformat(
                        config_data.get('last_modified', datetime.now().isoformat())
                    )
                    return cls(**config_data)
            print(f"No Shuffle configuration file found at {filepath}, using defaults")
            return cls(**default_config)
        except Exception as e:
            print(f"Error loading Shuffle config: {e}")
            return cls(**default_config)

    def save_to_file(self, filepath: str = "shuffle_config.json") -> bool:
        """Saves current Shuffle configuration to file."""
        try:
            config_dict = {
                "shuffle_url": self.shuffle_url,
                "shuffle_api_key": self.shuffle_api_key,
                "workflow_name": self.workflow_name,
                "last_modified": datetime.now().isoformat()
            }

            with open(filepath, 'w') as f:
                json.dump(config_dict, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving Shuffle config: {e}")
            return False