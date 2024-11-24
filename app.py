
import customtkinter as ctk
import subprocess
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox  # For feedback messages
from tkinter import ttk
from tkinter import messagebox


# Initialize the app
app = ctk.CTk()
app.geometry("1200x600")
app.title("Guardian")




#Design 1 Tabbed Layout
"""def create_system_status_page():
    for widget in main_content_frame.winfo_children():
        widget.destroy()

    # Title
    title_label = ctk.CTkLabel(main_content_frame, text="System Status", font=("Arial", 20, "bold"))
    title_label.pack(pady=10)

    # Custom style for notebook tabs
    style = ttk.Style()
    style.configure(
        "TNotebook.Tab",
        font=("Arial", 14, "bold"),  # Adjust font size and style here
        padding=[10, 5]  # Add padding for better appearance
    )

    # Notebook (Tabbed Interface)
    notebook = ttk.Notebook(main_content_frame)
    notebook.pack(fill="both", expand=True, padx=20, pady=10)

    # Splunk Status Tab
    splunk_frame = ctk.CTkFrame(notebook, corner_radius=10)
    notebook.add(splunk_frame, text="Splunk & SOAR")

    ctk.CTkLabel(splunk_frame, text="Splunk SIEM: Healthy", font=("Arial", 14)).pack(pady=10)
    ctk.CTkLabel(splunk_frame, text="SOAR: Running Playbooks", font=("Arial", 14)).pack(pady=10)
    ctk.CTkLabel(splunk_frame, text="Universal Forwarders: All Connected", font=("Arial", 14)).pack(pady=10)

    # Resource Usage Tab
    resource_frame = ctk.CTkFrame(notebook, corner_radius=10)
    notebook.add(resource_frame, text="Resource Usage")

    ctk.CTkLabel(resource_frame, text="CPU Usage: 45%", font=("Arial", 14)).pack(pady=10)
    ctk.CTkLabel(resource_frame, text="Memory Usage: 65%", font=("Arial", 14)).pack(pady=10)
    ctk.CTkLabel(resource_frame, text="Disk Usage: 75%", font=("Arial", 14)).pack(pady=10)

    # Network Activity Tab
    network_frame = ctk.CTkFrame(notebook, corner_radius=10)
    notebook.add(network_frame, text="Network Activity")

    ctk.CTkLabel(network_frame, text="Upload Speed: 10 Mbps", font=("Arial", 14)).pack(pady=10)
    ctk.CTkLabel(network_frame, text="Download Speed: 50 Mbps", font=("Arial", 14)).pack(pady=10)
    ctk.CTkLabel(network_frame, text="Potential Bottlenecks: None Detected", font=("Arial", 14)).pack(pady=10)

    for widget in main_content_frame.winfo_children():
        widget.destroy()

    # Title
    title_label = ctk.CTkLabel(main_content_frame, text="System Status", font=("Arial", 20, "bold"))
    title_label.pack(pady=10)

    # Notebook (Tabbed Interface)
    notebook = ttk.Notebook(main_content_frame)
    notebook.pack(fill="both", expand=True, padx=20, pady=10)

    # Splunk Status Tab
    splunk_frame = ctk.CTkFrame(notebook, corner_radius=10)
    notebook.add(splunk_frame, text="Splunk & SOAR")

    ctk.CTkLabel(splunk_frame, text="Splunk SIEM: Healthy", font=("Arial", 14)).pack(pady=10)
    ctk.CTkLabel(splunk_frame, text="SOAR: Running Playbooks", font=("Arial", 14)).pack(pady=10)
    ctk.CTkLabel(splunk_frame, text="Universal Forwarders: All Connected", font=("Arial", 14)).pack(pady=10)

    # Resource Usage Tab
    resource_frame = ctk.CTkFrame(notebook, corner_radius=10)
    notebook.add(resource_frame, text="Resource Usage")

    ctk.CTkLabel(resource_frame, text="CPU Usage: 45%", font=("Arial", 14)).pack(pady=10)
    ctk.CTkLabel(resource_frame, text="Memory Usage: 65%", font=("Arial", 14)).pack(pady=10)
    ctk.CTkLabel(resource_frame, text="Disk Usage: 75%", font=("Arial", 14)).pack(pady=10)

    # Network Activity Tab
    network_frame = ctk.CTkFrame(notebook, corner_radius=10)
    notebook.add(network_frame, text="Network Activity")

    ctk.CTkLabel(network_frame, text="Upload Speed: 10 Mbps", font=("Arial", 14)).pack(pady=10)
    ctk.CTkLabel(network_frame, text="Download Speed: 50 Mbps", font=("Arial", 14)).pack(pady=10)
    ctk.CTkLabel(network_frame, text="Potential Bottlenecks: None Detected", font=("Arial", 14)).pack(pady=10)"""

#Design 2 Card Layout
"""def create_system_status_page():
    for widget in main_content_frame.winfo_children():
        widget.destroy()

    # Title
    title_label = ctk.CTkLabel(main_content_frame, text="System Status", font=("Arial", 20, "bold"))
    title_label.pack(pady=10)

    # Splunk Status Card
    splunk_frame = ctk.CTkFrame(main_content_frame, corner_radius=10)
    splunk_frame.pack(fill="x", padx=20, pady=10)
    ctk.CTkLabel(splunk_frame, text="Splunk & SOAR Status", font=("Arial", 16, "bold")).pack(anchor="w", padx=10, pady=5)
    ctk.CTkLabel(splunk_frame, text="Splunk SIEM: Healthy", font=("Arial", 14)).pack(anchor="w", padx=10)
    ctk.CTkLabel(splunk_frame, text="SOAR: Running Playbooks", font=("Arial", 14)).pack(anchor="w", padx=10)
    ctk.CTkLabel(splunk_frame, text="Universal Forwarders: All Connected", font=("Arial", 14)).pack(anchor="w", padx=10)

    # Resource Usage Card
    resource_frame = ctk.CTkFrame(main_content_frame, corner_radius=10)
    resource_frame.pack(fill="x", padx=20, pady=10)
    ctk.CTkLabel(resource_frame, text="Resource Usage", font=("Arial", 16, "bold")).pack(anchor="w", padx=10, pady=5)
    ctk.CTkLabel(resource_frame, text="CPU Usage: 45%", font=("Arial", 14)).pack(anchor="w", padx=10)
    ctk.CTkLabel(resource_frame, text="Memory Usage: 65%", font=("Arial", 14)).pack(anchor="w", padx=10)
    ctk.CTkLabel(resource_frame, text="Disk Usage: 75%", font=("Arial", 14)).pack(anchor="w", padx=10)

    # Network Activity Card
    network_frame = ctk.CTkFrame(main_content_frame, corner_radius=10)
    network_frame.pack(fill="x", padx=20, pady=10)
    ctk.CTkLabel(network_frame, text="Network Activity", font=("Arial", 16, "bold")).pack(anchor="w", padx=10, pady=5)
    ctk.CTkLabel(network_frame, text="Upload Speed: 10 Mbps", font=("Arial", 14)).pack(anchor="w", padx=10)
    ctk.CTkLabel(network_frame, text="Download Speed: 50 Mbps", font=("Arial", 14)).pack(anchor="w", padx=10)
    ctk.CTkLabel(network_frame, text="Potential Bottlenecks: None Detected", font=("Arial", 14)).pack(anchor="w", padx=10)
"""

#Design 3 Interactive Buttons
"""def create_system_status_page():
    for widget in main_content_frame.winfo_children():
        widget.destroy()

    # Title
    title_label = ctk.CTkLabel(main_content_frame, text="System Status", font=("Arial", 20, "bold"))
    title_label.pack(pady=10)

    # Button to Show Splunk Status
    def show_splunk_status():
        messagebox.showinfo("Splunk Status", "Splunk SIEM: Healthy\nSOAR: Running Playbooks\nUniversal Forwarders: All Connected")

    ctk.CTkButton(main_content_frame, text="Check Splunk Status", command=show_splunk_status).pack(pady=10)

    # Button to Show Resource Usage
    def show_resource_usage():
        messagebox.showinfo("Resource Usage", "CPU Usage: 45%\nMemory Usage: 65%\nDisk Usage: 75%")

    ctk.CTkButton(main_content_frame, text="Check Resource Usage", command=show_resource_usage).pack(pady=10)

    # Button to Show Network Activity
    def show_network_activity():
        messagebox.showinfo("Network Activity", "Upload Speed: 10 Mbps\nDownload Speed: 50 Mbps\nPotential Bottlenecks: None Detected")

    ctk.CTkButton(main_content_frame, text="Check Network Activity", command=show_network_activity).pack(pady=10)
"""

#Design 4 Dynamic Dashboard Style
def create_system_status_page():
    for widget in main_content_frame.winfo_children():
        widget.destroy()

    # Create a frame to hold the canvas and horizontal scrollbar
    scrollable_frame_container = ctk.CTkFrame(main_content_frame, corner_radius=0)
    scrollable_frame_container.pack(fill="both", expand=True)

    # Create a canvas and horizontal scrollbar
    canvas = tk.Canvas(scrollable_frame_container, bg="gray90", highlightthickness=0)
    h_scrollbar = ctk.CTkScrollbar(scrollable_frame_container, orientation="horizontal", command=canvas.xview)
    scrollable_frame = ctk.CTkFrame(canvas, corner_radius=10)

    # Configure canvas for horizontal scrolling
    def update_scrollregion(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.xview_moveto(0)  # Reset horizontal scroll position

    scrollable_frame.bind("<Configure>", update_scrollregion)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(xscrollcommand=h_scrollbar.set)

    # Pack canvas and horizontal scrollbar
    canvas.grid(row=0, column=0, sticky="nsew")
    h_scrollbar.grid(row=1, column=0, sticky="ew")

    # Configure grid weights for resizing
    scrollable_frame_container.grid_rowconfigure(0, weight=1)
    scrollable_frame_container.grid_columnconfigure(0, weight=1)

    # Bind horizontal scroll events only
    def _on_horizontal_scroll(event):
        canvas.xview_scroll(-1 * (event.delta // 120), "units")

    canvas.bind_all("<Shift-MouseWheel>", _on_horizontal_scroll)  # Horizontal scroll with Shift key

    # Title
    title_label = ctk.CTkLabel(scrollable_frame, text="System Status", font=("Arial", 24, "bold"))
    title_label.grid(row=0, column=0, columnspan=3, pady=10)

    # Splunk & SOAR Status (Left Column)
    splunk_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
    splunk_frame.grid(row=1, column=0, padx=20, pady=10, sticky="n")

    splunk_title = ctk.CTkLabel(splunk_frame, text="Splunk & SOAR Status", font=("Arial", 18, "bold"))
    splunk_title.pack(anchor="w", padx=10, pady=5)

    splunk_status = ctk.CTkLabel(splunk_frame, text="Splunk SIEM: ✅ Healthy", font=("Arial", 14), fg_color="green", corner_radius=5, width=200)
    splunk_status.pack(anchor="w", padx=20, pady=2)

    soar_status = ctk.CTkLabel(splunk_frame, text="SOAR: ⚙️ Running Playbooks", font=("Arial", 14), fg_color="green", corner_radius=5, width=250)
    soar_status.pack(anchor="w", padx=20, pady=2)

    forwarders_status = ctk.CTkLabel(splunk_frame, text="Universal Forwarders: 🔗 All Connected", font=("Arial", 14), fg_color="green", corner_radius=5, width=300)
    forwarders_status.pack(anchor="w", padx=20, pady=2)

    # Resource Usage (Center Column)
    resource_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
    resource_frame.grid(row=1, column=1, padx=20, pady=10, sticky="n")

    resource_title = ctk.CTkLabel(resource_frame, text="Resource Usage", font=("Arial", 18, "bold"))
    resource_title.pack(anchor="w", padx=10, pady=5)

    # CPU Usage
    ctk.CTkLabel(resource_frame, text="CPU Usage", font=("Arial", 14)).pack(anchor="w", padx=20, pady=2)
    cpu_bar_frame = ctk.CTkFrame(resource_frame)
    cpu_bar_frame.pack(fill="x", padx=20, pady=2)
    cpu_bar = ctk.CTkProgressBar(cpu_bar_frame, progress_color="red", height=10)
    cpu_bar.set(0.45)  # 45%
    cpu_bar.pack(side="left", fill="x", expand=True)
    cpu_value = ctk.CTkLabel(cpu_bar_frame, text="45%", font=("Arial", 14))
    cpu_value.pack(side="left", padx=10)

    # Memory Usage
    ctk.CTkLabel(resource_frame, text="Memory Usage", font=("Arial", 14)).pack(anchor="w", padx=20, pady=2)
    memory_bar_frame = ctk.CTkFrame(resource_frame)
    memory_bar_frame.pack(fill="x", padx=20, pady=2)
    memory_bar = ctk.CTkProgressBar(memory_bar_frame, progress_color="orange", height=10)
    memory_bar.set(0.65)  # 65%
    memory_bar.pack(side="left", fill="x", expand=True)
    memory_value = ctk.CTkLabel(memory_bar_frame, text="65%", font=("Arial", 14))
    memory_value.pack(side="left", padx=10)

    # Disk Usage
    ctk.CTkLabel(resource_frame, text="Disk Usage", font=("Arial", 14)).pack(anchor="w", padx=20, pady=2)
    disk_bar_frame = ctk.CTkFrame(resource_frame)
    disk_bar_frame.pack(fill="x", padx=20, pady=2)
    disk_bar = ctk.CTkProgressBar(disk_bar_frame, progress_color="blue", height=10)
    disk_bar.set(0.75)  # 75%
    disk_bar.pack(side="left", fill="x", expand=True)
    disk_value = ctk.CTkLabel(disk_bar_frame, text="75%", font=("Arial", 14))
    disk_value.pack(side="left", padx=10)

    # Network Activity (Right Column)
    network_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
    network_frame.grid(row=1, column=2, padx=20, pady=10, sticky="n")

    network_title = ctk.CTkLabel(network_frame, text="Network Activity", font=("Arial", 18, "bold"))
    network_title.pack(anchor="w", padx=10, pady=5)

    upload_status = ctk.CTkLabel(network_frame, text="Upload Speed: 📤 10 Mbps", font=("Arial", 14), fg_color="blue", corner_radius=5, width=200)
    upload_status.pack(anchor="w", padx=20, pady=2)

    download_status = ctk.CTkLabel(network_frame, text="Download Speed: 📥 50 Mbps", font=("Arial", 14), fg_color="blue", corner_radius=5, width=220)
    download_status.pack(anchor="w", padx=20, pady=2)

    bottleneck_status = ctk.CTkLabel(network_frame, text="Potential Bottlenecks: ❌ None Detected", font=("Arial", 14), fg_color="green", corner_radius=5, width=300)
    bottleneck_status.pack(anchor="w", padx=20, pady=2)




# Sidebar visibility flag
sidebar_visible = True

def create_incident_response_history_page():
    for widget in main_content_frame.winfo_children():
        widget.destroy()

    # Title
    title_label = ctk.CTkLabel(main_content_frame, text="Incident Response History", font=("Arial", 20, "bold"))
    title_label.pack(pady=20)

    # Example list of incidents
    incidents = [
        {"Date": "2024-11-01", "Incident": "Detected ransomware: LockBit", "Action": "Files isolated"},
        {"Date": "2024-11-10", "Incident": "Backup initiated", "Action": "All files backed up"},
    ]

    # Display incidents
    for incident in incidents:
        frame = ctk.CTkFrame(main_content_frame, corner_radius=10)
        frame.pack(fill="x", pady=5, padx=20)

        details = f"{incident['Date']} - {incident['Incident']} - Action: {incident['Action']}"
        label = ctk.CTkLabel(frame, text=details, font=("Arial", 14))
        label.pack(anchor="w", pady=5, padx=10)

    # Buttons
    button_frame = ctk.CTkFrame(main_content_frame)
    button_frame.pack(pady=20)

    # Export as PDF Button
    export_button = ctk.CTkButton(
        button_frame,
        text="Export as PDF",
        command=lambda: print("Exporting to PDF...")  # Replace with actual export logic
    )
    export_button.pack(side="left", padx=10)

    # Print Button
    printer_button = ctk.CTkButton(
        button_frame,
        text=" 🖨️ Print",
        command=lambda: print("Printing...")  # Replace with actual print logic
    )
    printer_button.pack(side="left", padx=10)

def create_settings_page():
    # Clear the main content frame
    for widget in main_content_frame.winfo_children():
        widget.destroy()

    # Create a scrollable frame
    scrollable_frame = ctk.CTkScrollableFrame(main_content_frame, width=600, height=500, corner_radius=10)
    scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Title
    title_label = ctk.CTkLabel(scrollable_frame, text="Settings", font=("Arial", 20, "bold"))
    title_label.pack(pady=20)

    # General Settings Frame
    general_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
    general_frame.pack(pady=10, padx=20, fill="x")

    general_label = ctk.CTkLabel(general_frame, text="General Settings", font=("Arial", 16, "bold"))
    general_label.pack(anchor="w", pady=10, padx=10)

    # Auto-Response Toggle
    auto_response_var = ctk.BooleanVar(value=False)

    def toggle_auto_response():
        print(f"Auto-Response Mode: {'Enabled' if auto_response_var.get() else 'Disabled'}")

    auto_response_toggle = ctk.CTkSwitch(
        general_frame,
        text="Automatically detect and respond to ransomware threats.",
        variable=auto_response_var,
        command=toggle_auto_response,
    )
    auto_response_toggle.pack(anchor="w", padx=20, pady=5)

    # Notification Preferences
    notify_var = ctk.BooleanVar(value=True)

    def toggle_notifications():
        print(f"Notifications: {'Enabled' if notify_var.get() else 'Disabled'}")

    notify_toggle = ctk.CTkSwitch(
        general_frame,
        text="Notify me when threats are detected or resolved.",
        variable=notify_var,
        command=toggle_notifications,
    )
    notify_toggle.pack(anchor="w", padx=20, pady=5)

    # Security Settings Frame
    security_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
    security_frame.pack(pady=10, padx=20, fill="x")

    security_label = ctk.CTkLabel(security_frame, text="Security Settings", font=("Arial", 16, "bold"))
    security_label.pack(anchor="w", pady=10, padx=10)

    # Real-Time Protection Toggle
    real_time_var = ctk.BooleanVar(value=True)

    def toggle_real_time():
        print(f"Real-Time Protection: {'Enabled' if real_time_var.get() else 'Disabled'}")

    real_time_toggle = ctk.CTkSwitch(
        security_frame,
        text="Continuously monitor for ransomware activities.",
        variable=real_time_var,
        command=toggle_real_time,
    )
    real_time_toggle.pack(anchor="w", padx=20, pady=5)

    # Backup & Recovery Settings Frame
    backup_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
    backup_frame.pack(pady=10, padx=20, fill="x")

    backup_label = ctk.CTkLabel(backup_frame, text="Backup & Recovery Settings", font=("Arial", 16, "bold"))
    backup_label.pack(anchor="w", pady=10, padx=10)

    # File Recovery Options
    recovery_var = ctk.StringVar(value="Most Recent Backup")

    recovery_label = ctk.CTkLabel(backup_frame, text="File Recovery Options:", font=("Arial", 14))
    recovery_label.pack(anchor="w", padx=20, pady=5)

    recovery_dropdown = ctk.CTkOptionMenu(
        backup_frame, values=["Most Recent Backup", "Custom Recovery Point"], variable=recovery_var
    )
    recovery_dropdown.pack(anchor="w", padx=20, pady=5)

    # Automatic Backup Toggle
    auto_backup_var = ctk.BooleanVar(value=True)

    def toggle_auto_backup():
        print(f"Automatic Backup: {'Enabled' if auto_backup_var.get() else 'Disabled'}")

    auto_backup_toggle = ctk.CTkSwitch(
        backup_frame,
        text="Enable automatic backup of critical files.",
        variable=auto_backup_var,
        command=toggle_auto_backup,
    )
    auto_backup_toggle.pack(anchor="w", padx=20, pady=5)

    # Backup Frequency Dropdown
    frequency_var = ctk.StringVar(value="Daily")

    frequency_label = ctk.CTkLabel(backup_frame, text="Backup Frequency:", font=("Arial", 14))
    frequency_label.pack(anchor="w", padx=20, pady=5)

    frequency_dropdown = ctk.CTkOptionMenu(backup_frame, values=["Hourly", "Daily", "Weekly"], variable=frequency_var)
    frequency_dropdown.pack(anchor="w", padx=20, pady=5)

    # Advanced Options (Expandable)
    advanced_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
    advanced_frame.pack(pady=10, padx=20, fill="x")

    advanced_label = ctk.CTkLabel(advanced_frame, text="Advanced Options", font=("Arial", 16, "bold"))
    advanced_label.pack(anchor="w", pady=10, padx=10)

    # Exclude Files/Folders
    exclude_label = ctk.CTkLabel(advanced_frame, text="Exclude Files/Folders from backups:", font=("Arial", 14))
    exclude_label.pack(anchor="w", padx=20, pady=5)

    exclude_entry = ctk.CTkEntry(advanced_frame, placeholder_text="Enter file/folder paths")
    exclude_entry.pack(anchor="w", padx=20, pady=5)

    # Reset to Default Button
    def reset_to_default():
        auto_response_var.set(False)
        notify_var.set(True)
        real_time_var.set(True)
        recovery_var.set("Most Recent Backup")
        auto_backup_var.set(True)
        frequency_var.set("Daily")
        exclude_entry.delete(0, "end")
        print("Settings reset to default.")

    reset_button = ctk.CTkButton(advanced_frame, text="Reset to Default", command=reset_to_default)
    reset_button.pack(anchor="w", padx=20, pady=10)

    # Educational Resources Frame
    resources_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10)
    resources_frame.pack(pady=10, padx=20, fill="x")

    resources_label = ctk.CTkLabel(resources_frame, text="Educational Resources", font=("Arial", 16, "bold"))
    resources_label.pack(anchor="w", pady=10, padx=10)

    # Learn About Ransomware Button
    def open_guide():
        print("Opening ransomware guide...")  # Replace with actual functionality

    guide_button = ctk.CTkButton(resources_frame, text="Learn About Ransomware", command=open_guide)
    guide_button.pack(anchor="w", padx=20, pady=5)
# Toggle sidebar visibility
def toggle_sidebar():
    global sidebar_visible
    if sidebar_visible:
        sidebar_frame.grid_forget()  # Remove sidebar from grid
        toggle_button.configure(text="☰")  # Show the menu icon
    else:
        sidebar_frame.grid(row=1, column=0, sticky="ns")  # Restore sidebar
        toggle_button.configure(text="X")  # Show the close icon
    sidebar_visible = not sidebar_visible


# Top Navigation Bar
nav_bar = ctk.CTkFrame(app, height=50, corner_radius=0)
nav_bar.grid(row=0, column=0, columnspan=2, sticky="ew")

toggle_button = ctk.CTkButton(nav_bar, text="X", command=toggle_sidebar, width=50)
toggle_button.pack(side="left", padx=10, pady=5)

nav_title = ctk.CTkLabel(nav_bar, text="Guardian", font=("Arial", 18))
nav_title.pack(side="left", padx=20)
  
# Main Content Frame
main_content_frame = ctk.CTkFrame(app, corner_radius=10)
main_content_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

main_content_frame.grid_rowconfigure((0, 1), weight=1)
main_content_frame.grid_columnconfigure((0, 1), weight=1)


# Update Main Content for non-dashboard views
def update_main_content(message):
    for widget in main_content_frame.winfo_children():
        widget.destroy()

    label = ctk.CTkLabel(main_content_frame, text=message, font=("Arial", 20))
    label.pack(expand=True)


# Update Main Content for dashboard
def update_dashboard():
    for widget in main_content_frame.winfo_children():
        widget.destroy()

    stats = [
        {"title": "Active Threats", "value": "0"},
        {"title": "Last Scan", "value": "2 hours ago"},
        {"title": "System Status", "value": "Secure"},
        {"title": "Total Alerts", "value": "5"},
    ]

    for i, stat in enumerate(stats):
        frame = ctk.CTkFrame(main_content_frame, corner_radius=10)
        frame.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky="nsew")

        title_label = ctk.CTkLabel(frame, text=stat["title"], font=("Arial", 16)) 
        title_label.pack(pady=10)

        value_label = ctk.CTkLabel(frame, text=stat["value"], font=("Arial", 24))
        value_label.pack()

# Alerts page
# Function to create the Alerts Page (Integrated from alerts.py)
def create_alerts_page():
    for widget in main_content_frame.winfo_children():
        widget.destroy()

    # Title
    title_label = ctk.CTkLabel(main_content_frame, text="Ransomware Alerts", font=("Arial", 20, "bold"))
    title_label.pack(pady=10)

    # Treeview-style alert display
    alerts_frame = ctk.CTkFrame(main_content_frame, corner_radius=10)
    alerts_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Treeview (from ttk)
    tree = ttk.Treeview(alerts_frame, columns=("Timestamp", "Type", "File", "Actions"), show="headings", height=12)

    # Define Treeview columns
    tree.heading("Timestamp", text="Timestamp")
    tree.heading("Type", text="Threat Type")
    tree.heading("File", text="Affected File")
    tree.heading("Actions", text="Actions Taken")
    tree.column("Timestamp", anchor="center", width=150)
    tree.column("Type", anchor="center", width=150)
    tree.column("File", anchor="w", width=300)
    tree.column("Actions", anchor="center", width=150)

    # Sample Alerts Data
    alerts_data = [
        {"timestamp": "2024-11-22 10:45", "severity": "Critical", "type": "Locky", "file": "document1.docx", "actions": "Quarantined"},
    {"timestamp": "2024-11-22 11:15", "severity": "Medium", "type": "Cerber", "file": "spreadsheet.xls", "actions": "Blocked Access"},
    {"timestamp": "2024-11-22 11:30", "severity": "Low", "type": "Wannacry", "file": "notes.txt", "actions": "Logged"},
    {"timestamp": "2024-11-22 12:00", "severity": "Critical", "type": "Ryuk", "file": "invoice.pdf", "actions": "Quarantined"},
    {"timestamp": "2024-11-22 12:15", "severity": "Medium", "type": "Sodinokibi", "file": "backup.zip", "actions": "Blocked Access"},
    {"timestamp": "2024-11-22 12:30", "severity": "Low", "type": "Petya", "file": "readme.md", "actions": "Logged"},
    ]

    # Insert data into Treeview
    for alert in alerts_data:
        tree.insert("", "end", values=(alert["timestamp"], alert["type"], alert["file"], alert["actions"]))

    tree.pack(fill="both", expand=True)

    # Details Section
    details_frame = ctk.CTkFrame(main_content_frame)
    details_frame.pack(fill="x", padx=20, pady=10)

    details_label = ctk.CTkLabel(details_frame, text="Alert Details:", font=("Arial", 14, "bold"))
    details_label.grid(row=0, column=0, sticky="w", padx=10)

    details_text = ctk.CTkLabel(details_frame, text="", font=("Arial", 12), justify="left")
    details_text.grid(row=1, column=0, sticky="w", padx=10)

    # Display alert details
    def display_details(event):
        selected_item = tree.focus()
        if selected_item:
            alert_details = tree.item(selected_item, "values")
            details_text.configure(
                text=f"Type: {alert_details[1]}\n"
                     f"Affected File: {alert_details[2]}\n"
                     f"Actions Taken: {alert_details[3]}"
            )

    tree.bind("<ButtonRelease-1>", display_details)

    # Acknowledge Button
    def acknowledge_alert():
        selected_item = tree.focus()
        if selected_item:
            tree.delete(selected_item)
            details_text.configure(text="Alert acknowledged and removed.")
        else:
            details_text.configure(text="Please select an alert to acknowledge.")

    acknowledge_button = ctk.CTkButton(main_content_frame, text="Acknowledge Alert", command=acknowledge_alert)
    acknowledge_button.pack(pady=10)

    # About page 
def create_about_page():
    global update_message
    # Clear the main content area before adding new content
    for widget in main_content_frame.winfo_children():
        widget.destroy()

    # Create a scrollable frame for the About page content
    about_canvas = tk.Canvas(main_content_frame, bg="gray90", highlightthickness=0)
    about_scrollbar = ctk.CTkScrollbar(main_content_frame, orientation="vertical", command=about_canvas.yview)
    about_scrollable_frame = ctk.CTkFrame(about_canvas, corner_radius=10)

    about_scrollable_frame.bind(
        "<Configure>", lambda e: about_canvas.configure(scrollregion=about_canvas.bbox("all"))
    )
    about_canvas.create_window((0, 0), window=about_scrollable_frame, anchor="nw")
    about_canvas.configure(yscrollcommand=about_scrollbar.set)

    about_canvas.pack(side="left", fill="both", expand=True)
    about_scrollbar.pack(side="right", fill="y")

    # Header: About Guardian
    header = ctk.CTkLabel(about_scrollable_frame, text="About Guardian", font=("Arial", 20, "bold"))
    header.pack(pady=(10, 20))

    # Purpose Section
    purpose_section = ctk.CTkFrame(about_scrollable_frame, corner_radius=10)
    purpose_section.pack(fill="x", padx=10, pady=10)

    purpose_header = ctk.CTkLabel(purpose_section, text="Purpose", font=("Arial", 16, "bold"))
    purpose_header.pack(anchor="w", pady=(5, 10), padx=10)

    purpose_content = [
        {"title": "Automated Detection and Response:", 
         "text": "Automates identification, containment, and recovery from ransomware attacks, minimizing manual intervention and reducing recovery time."},
        {"title": "Enhancing Personal Cybersecurity:", 
         "text": "Equips users with strong cybersecurity tools, typically accessible to large organizations, enhancing defense against advanced threats."},
        {"title": "User-Friendly Interface:", 
         "text": "Designed for users without technical expertise, the application delivers clear, actionable alerts and instructions."},
        {"title": "Continuous Threat Intelligence:", 
         "text": "Incorporates real-time threat intelligence feeds for up-to-date detection of ransomware variants."},
        {"title": "Cost-Effective Solution:", 
         "text": "Provides an affordable cybersecurity solution targeted at individuals and small businesses."},
    ]

    for item in purpose_content:
        ctk.CTkLabel(purpose_section, text=item["title"], font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
        ctk.CTkLabel(purpose_section, text=item["text"], font=("Arial", 12), wraplength=900, justify="left").pack(anchor="w", padx=10, pady=(0, 10))

    # Overview Section
    overview_section = ctk.CTkFrame(about_scrollable_frame, corner_radius=10)
    overview_section.pack(fill="x", padx=10, pady=10)

    overview_header = ctk.CTkLabel(overview_section, text="Overview of Guardian’s Objectives", font=("Arial", 16, "bold"))
    overview_header.pack(anchor="w", pady=(5, 10), padx=10)

    overview_content = (
        "The application is a desktop interface designed for end-users.\n\n"
        "Integration: It integrates with Splunk's Security Information and Event Management (SIEM) system and utilizes a customized Security Orchestration, Automation, and Response (SOAR) solution.\n\n"
        "Functionality: The application will provide real-time alerts, enable isolation of infected files, and facilitate automated recovery processes."
    )
    ctk.CTkLabel(overview_section, text=overview_content, font=("Arial", 12), wraplength=900, justify="left").pack(anchor="w", padx=10, pady=10)

    # Developers & Contributors Section
    developers_section = ctk.CTkFrame(about_scrollable_frame, corner_radius=10)
    developers_section.pack(fill="x", padx=10, pady=10)

    developers_header = ctk.CTkLabel(developers_section, text="Developers & Contributors", font=("Arial", 16, "bold"))
    developers_header.pack(anchor="w", pady=(5, 10), padx=10)

    developers_content = ctk.CTkLabel(
        developers_section,
        text=(  
            "- Lead Developer: Yahia Eissa\n"
            "- Contributor: Nada Abdelrahman\n"
            "- Contributor: Donya Hany\n"
            "- Contributor: Abdelrahman Walid\n"
            "- Contributor: Ali Ahmed"
        ),
        font=("Arial", 12),
        justify="left",
        wraplength=900,
    )
    developers_content.pack(anchor="w", padx=10)

    # Version Information Section
    version_section = ctk.CTkFrame(about_scrollable_frame, corner_radius=10)
    version_section.pack(fill="x", padx=10, pady=10)

    version_header = ctk.CTkLabel(version_section, text="Version Details", font=("Arial", 16, "bold"))
    version_header.pack(anchor="w", pady=(5, 10), padx=10)

    version_content = ctk.CTkLabel(
        version_section,
        text=(  
            "Version 1.0: Released on November 9, 2021 - This version outlined the specifications for the initial proposal.\n"
            "Version 1.1: Released on November 10, 2021 - This version incorporated updates to the project's scope.\n"
        ),
        font=("Arial", 12),
        justify="left",
        wraplength=900,
    )
    version_content.pack(anchor="w", padx=10)

    # Check for Updates Section
    update_message = ctk.StringVar(value="")
    update_button = ctk.CTkButton(
        version_section,
        text="Check for Updates",
        command=check_for_updates,
    )
    update_button.pack(anchor="w", pady=10, padx=10)

    update_label = ctk.CTkLabel(
        version_section, textvariable=update_message, font=("Arial", 12)
    )
    update_label.pack(anchor="w", pady=(5, 0))

update_message = ctk.StringVar(value="")
# Function to check for updates
def check_for_updates():
    global update_message  # Declare that you're using the global variable
    update_message.set("You are using the latest version. No updates available.")
    
    
# Contact Us Page
def create_contact_us_page():
    for widget in main_content_frame.winfo_children():
        widget.destroy()

    # Title
    title_label = ctk.CTkLabel(main_content_frame, text="Contact Us", font=("Arial", 20, "bold"))
    title_label.pack(pady=20)

    # Email
    email_label = ctk.CTkLabel(main_content_frame, text="Email: GUARDIANSUPPORT@GMAIL.COM", font=("Arial", 14))
    email_label.pack(pady=10)

    # Feedback Textbox
    feedback_label = ctk.CTkLabel(main_content_frame, text="Write to Us:", font=("Arial", 14))
    feedback_label.pack(pady=10)

    feedback_textbox = ctk.CTkTextbox(main_content_frame, width=400, height=150)
    feedback_textbox.pack(pady=10)

    # Submit Button
    def submit_feedback():
        feedback = feedback_textbox.get("1.0", "end").strip()
        if feedback:
            print(f"Feedback Submitted: {feedback}")  # Replace with actual submission logic
            feedback_textbox.delete("1.0", "end")
            messagebox.showinfo("Thank you!", "Your feedback has been submitted.")
        else:
            messagebox.showwarning("Empty Message", "Please write something before submitting.")

    submit_button = ctk.CTkButton(main_content_frame, text="Submit", command=submit_feedback)
    submit_button.pack(pady=20)

# Sidebar Frame
sidebar_frame = ctk.CTkFrame(app, width=200, corner_radius=0)
sidebar_frame.grid(row=1, column=0, sticky="ns")

sidebar_label = ctk.CTkLabel(sidebar_frame, text="Menu", font=("Arial", 16))
sidebar_label.pack(pady=20)

dashboard_button = ctk.CTkButton(sidebar_frame, text="Dashboard", command=update_dashboard)
dashboard_button.pack(pady=10, padx=10, fill="x")

alerts_button = ctk.CTkButton(sidebar_frame, text="Alerts", command=create_alerts_page)
alerts_button.pack(pady=10, padx=10, fill="x")

incident_button = ctk.CTkButton(
    sidebar_frame,
    text="Incident Response History",
    command=create_incident_response_history_page
)
incident_button.pack(pady=10, padx=10, fill="x")

system_status_button = ctk.CTkButton(sidebar_frame, text="System Status",
                                     command=create_system_status_page)
system_status_button.pack(pady=10, padx=10, fill="x")

contact_button = ctk.CTkButton(sidebar_frame, text="Contact Us", command=create_contact_us_page)
contact_button.pack(pady=10, padx=10, fill="x")

about_button = ctk.CTkButton(sidebar_frame, text="About System", command=create_about_page)
about_button.pack(pady=10, padx=10, fill="x")

settings_button = ctk.CTkButton(sidebar_frame, text="Settings", command=create_settings_page)
settings_button.pack(pady=10, padx=10, fill="x")
# Set the initial dashboard
update_dashboard()

# Configure row/column weights for responsiveness
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(1, weight=1)

# Run the application
app.mainloop()
