import customtkinter as ctk


class SettingsController:
    def __init__(self):
        self.auto_response_var = ctk.BooleanVar(value=False)
        self.notify_var = ctk.BooleanVar(value=True)
        self.real_time_var = ctk.BooleanVar(value=True)
        self.recovery_var = ctk.StringVar(value="Most Recent Backup")
        self.auto_backup_var = ctk.BooleanVar(value=True)
        self.frequency_var = ctk.StringVar(value="Daily")

    def toggle_notifications(self):
        print(f"Notifications: {'Enabled' if self.notify_var.get() else 'Disabled'}")

    def toggle_auto_backup(self):
        print(f"Automatic Backup: {'Enabled' if self.auto_backup_var.get() else 'Disabled'}")

    def reset_to_default(self):
        self.auto_response_var.set(False)
        self.notify_var.set(True)
        self.real_time_var.set(True)
        self.recovery_var.set("Most Recent Backup")
        self.auto_backup_var.set(True)
        self.frequency_var.set("Daily")
        print("Settings reset to default.")

    def open_guide(self):
        print("Opening ransomware guide...")
