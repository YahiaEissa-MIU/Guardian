import customtkinter as ctk


class SystemStatusView(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.metrics_grid = None
        self.controller = controller
        self.metric_frames = {}
        self.create_widgets()

    def set_controller(self, controller):
        self.controller = controller
        self.controller.start_updates()

    def create_widgets(self):
        # Configure main frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        title_label = ctk.CTkLabel(self, text="System Status",
                                   font=("Arial", 24, "bold"),
                                   anchor="center")
        title_label.grid(row=0, column=0, pady=(10, 15), sticky="ew")

        # Metrics grid container
        self.metrics_grid = ctk.CTkFrame(self, fg_color="transparent")
        self.metrics_grid.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Configure grid layout (2 rows, 3 columns)
        for i in range(2):
            self.metrics_grid.rowconfigure(i, weight=1, uniform="metrics_row")
        for j in range(3):
            self.metrics_grid.columnconfigure(j, weight=1, uniform="metrics_col")

        # Metric configuration
        metrics = [
            ("CPU", "cpu_usage", "%"),
            ("Memory", "memory_usage", "MB"),
            ("Disk", "disk_usage", "MB"),
            ("Network", "network", "Mbps"),
            ("SIEM", "SIEM_status", ""),
            ("SOAR", "SOAR_status", "",)
        ]

        for idx, (title, metric_key, unit) in enumerate(metrics):
            row = idx // 3
            col = idx % 3

            frame = ctk.CTkFrame(self.metrics_grid,
                                 corner_radius=15,
                                 border_width=2,
                                 fg_color="#2d3436",
                                 )
            frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            frame.grid_propagate(False)

            # Configure frame grid
            frame.grid_rowconfigure(1, weight=1)
            frame.grid_columnconfigure(0, weight=1)

            # Title section
            title_label = ctk.CTkLabel(frame, text=title,
                                       font=("Arial", 16, "bold"),
                                       )
            title_label.grid(row=0, column=0, pady=(12, 5), sticky="n")

            # Value display area
            value_frame = ctk.CTkFrame(frame, fg_color="transparent")
            value_frame.grid(row=1, column=0, sticky="nsew")

            # Create different layouts based on metric type
            if metric_key in ["disk_usage", "network"]:
                self._create_double_line(value_frame, metric_key, unit)
            else:
                self._create_single_line(value_frame, metric_key, unit,)

    def _create_single_line(self, parent, metric_key, unit):
        value_label = ctk.CTkLabel(parent,
                                   text="0" + unit,
                                   font=("Arial", 18),
                                   )
        value_label.pack(expand=True)
        self.metric_frames[metric_key] = value_label

    def _create_double_line(self, parent, metric_key, unit):
        grid_frame = ctk.CTkFrame(parent, fg_color="transparent")
        grid_frame.pack(expand=True, fill="both")

        for i in range(2):
            grid_frame.rowconfigure(i, weight=1)
            grid_frame.columnconfigure(0, weight=1)
            grid_frame.columnconfigure(1, weight=1)

        labels = {
            "disk_usage": ["Read", "Write"],
            "network": ["Upload", "Download"]
        }[metric_key]

        value_labels = []
        for i, label in enumerate(labels):
            ctk.CTkLabel(grid_frame,
                         text=label + ":",
                         font=("Arial", 12),
                         anchor="e").grid(row=i, column=0, padx=(10, 2), pady=2)

            val_label = ctk.CTkLabel(grid_frame,
                                     text="0.00",
                                     font=("Arial", 14),
                                     anchor="w")
            val_label.grid(row=i, column=1, padx=(2, 10), pady=2, sticky="w")
            value_labels.append(val_label)

        self.metric_frames[metric_key] = value_labels

    def update_metrics(self, metrics):
        # Update single-value metrics
        self.metric_frames["cpu_usage"].configure(
            text=f"{metrics['cpu_usage'] * 100:.1f}%"
        )
        self.metric_frames["memory_usage"].configure(
            text=f"{metrics['memory_usage']:.2f} MB"
        )
        self.metric_frames["SIEM_status"].configure(
            text=metrics["SIEM_status"]
        )
        self.metric_frames["SOAR_status"].configure(
            text=metrics["SOAR_status"]
        )

        # Update multi-value metrics
        self.metric_frames["disk_usage"][0].configure(
            text=f"{metrics['disk_read']:.2f} MB"
        )
        self.metric_frames["disk_usage"][1].configure(
            text=f"{metrics['disk_write']:.2f} MB"
        )
        self.metric_frames["network"][0].configure(
            text=f"{metrics['network_upload']:.2f} MB"
        )
        self.metric_frames["network"][1].configure(
            text=f"{metrics['network_download']:.2f} MB"
        )
