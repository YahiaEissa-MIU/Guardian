class AlertModel:
    def __init__(self):
        self.alerts_data = [
            {"timestamp": "2024-11-22 10:45", "type": "Locky", "file": "document1.docx", "actions": "Quarantined"},
            {"timestamp": "2024-11-22 11:15", "type": "Cerber", "file": "spreadsheet.xls", "actions": "Blocked Access"},
            {"timestamp": "2024-11-22 11:30", "type": "Wannacry", "file": "notes.txt", "actions": "Logged"},
            {"timestamp": "2024-11-22 12:00", "type": "Ryuk", "file": "invoice.pdf", "actions": "Quarantined"},
            {"timestamp": "2024-11-22 12:15", "type": "Sodinokibi", "file": "backup.zip", "actions": "Blocked Access"},
            {"timestamp": "2024-11-22 12:30", "type": "Petya", "file": "readme.md", "actions": "Logged"},
        ]

    def get_alerts(self):
        """ Returns the list of alerts """
        return self.alerts_data

    def acknowledge_alert(self, index):
        """ Removes an alert from the list based on index """
        if 0 <= index < len(self.alerts_data):
            del self.alerts_data[index]
