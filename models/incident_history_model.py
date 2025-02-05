import csv


def export_to_csv(incidents, filename="incident_history.csv"):
    """Exports given incidents to a CSV file."""
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Date", "Incident", "Action"])
            writer.writeheader()
            writer.writerows(incidents)
        return f"Exported successfully to {filename}"
    except Exception as e:
        return f"Error exporting file: {e}"


class IncidentHistoryModel:
    def __init__(self):
        self.incidents = [
            {"Date": "2024-11-01", "Incident": "Detected ransomware: LockBit", "Action": "Files isolated"},
            {"Date": "2024-11-10", "Incident": "Backup initiated", "Action": "All files backed up"},
        ]

    def get_incidents(self, filter_type=None, filter_value=None):
        """Returns filtered list of incidents based on criteria."""
        if not filter_type or not filter_value:
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
