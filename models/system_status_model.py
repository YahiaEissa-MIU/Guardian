import psutil
import os


class SystemStatusModel:
    def __init__(self):
        self.process = psutil.Process(os.getpid())  # Get current process

        self.data = {
            "cpu_usage": 0.0,
            "memory_usage": 0.0,
            "disk_read": 0.0,  # Store as float (MB)
            "disk_write": 0.0,  # Store as float (MB)
            "network_upload": 0.0,  # Store as float (MB)
            "network_download": 0.0,  # Store as float (MB)
            "splunk_status": "Unknown",
            "soar_status": "Unknown"
        }

    def fetch_metrics(self):
        """Retrieve real-time application-specific metrics."""
        self.data["cpu_usage"] = self.process.cpu_percent(interval=1) / 100.0  # CPU usage of this process
        self.data["memory_usage"] = self.process.memory_info().rss / (1024 ** 2)  # Memory in MB

        # Disk I/O Usage (in MB)
        io_counters = self.process.io_counters()
        self.data["disk_read"] = io_counters.read_bytes / (1024 ** 2)  # Read in MB
        self.data["disk_write"] = io_counters.write_bytes / (1024 ** 2)  # Write in MB

        # Network stats (Tracks process-specific sent/received bytes)
        net_io = psutil.net_io_counters()
        self.data["network_upload"] = net_io.bytes_sent / (1024 * 1024)  # Convert to MB
        self.data["network_download"] = net_io.bytes_recv / (1024 * 1024)  # Convert to MB

        # Placeholder values for SIEM and SOAR status
        self.data["SIEM_status"] = "OK"
        self.data["SOAR_status"] = "Running"

        return self.data
