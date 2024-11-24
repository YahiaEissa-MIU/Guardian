
import customtkinter as ctk
import subprocess
from tkinter import ttk
from tkinter import messagebox  # For feedback messages

# Initialize the app
app = ctk.CTk()
app.geometry("1200x600")
app.title("Guardian")

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

# Function to open the alert page (AboutSystem.py)
def open_alert_page():
    subprocess.run(["python", "alerts.py"])

# Function to open the about page (AboutSystem.py)
def open_about_page():
    subprocess.run(["python", "AboutSystem.py"])

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
                                     command=lambda: update_main_content("Status..."))
system_status_button.pack(pady=10, padx=10, fill="x")

contact_button = ctk.CTkButton(sidebar_frame, text="Contact Us", command=create_contact_us_page)
contact_button.pack(pady=10, padx=10, fill="x")

about_button = ctk.CTkButton(sidebar_frame, text="About System", command=open_about_page)
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
