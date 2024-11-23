import customtkinter as ctk
import subprocess
from tkinter import ttk  # Import ttk for Treeview

# Initialize the app
app = ctk.CTk()
app.geometry("1200x600")
app.title("Guardian")

# Sidebar visibility flag
sidebar_visible = True

# Sample data with multiple alerts
alerts_data = [
    {"timestamp": "2024-11-22 10:45", "severity": "Critical", "type": "Locky", "file": "document1.docx", "actions": "Quarantined"},
    {"timestamp": "2024-11-22 11:15", "severity": "Medium", "type": "Cerber", "file": "spreadsheet.xls", "actions": "Blocked Access"},
    {"timestamp": "2024-11-22 11:30", "severity": "Low", "type": "Wannacry", "file": "notes.txt", "actions": "Logged"},
    {"timestamp": "2024-11-22 12:00", "severity": "Critical", "type": "Ryuk", "file": "invoice.pdf", "actions": "Quarantined"},
    {"timestamp": "2024-11-22 12:15", "severity": "Medium", "type": "Sodinokibi", "file": "backup.zip", "actions": "Blocked Access"},
    {"timestamp": "2024-11-22 12:30", "severity": "Low", "type": "Petya", "file": "readme.md", "actions": "Logged"},
]

# Function to toggle sidebar visibility
def toggle_sidebar():
    global sidebar_visible
    if sidebar_visible:
        sidebar_frame.grid_forget()  # Hide the sidebar
        toggle_button.configure(text="☰")  # Show menu icon
    else:
        sidebar_frame.grid(row=1, column=0, sticky="ns")  # Show the sidebar
        toggle_button.configure(text="X")  # Show close icon
    sidebar_visible = not sidebar_visible
# Function to open the about page (AboutSystem.py)
def open_about_page():
    subprocess.run(["python", "AboutSystem.py"])

    # Function to open the about page (AboutSystem.py)
def open_dashboard_page():
    subprocess.run(["python", "app.py"])

# Function to display alerts page with acknowledgment functionality
def show_alerts_page():
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

    def display_details(event):
        selected_item = tree.focus()
        if selected_item:
            alert_details = tree.item(selected_item, "values")
            details_text.configure(
                text=f"Type: {alert_details[1]}\n"
                     f"Affected File: {alert_details[2]}\n"
                     f"Actions Taken: {alert_details[3]}"
            )

    def acknowledge_alert():
        selected_item = tree.focus()
        if selected_item:
            tree.delete(selected_item)
            details_text.configure(text="Alert acknowledged and removed.")
        else:
            details_text.configure(text="Please select an alert to acknowledge.")

    tree.bind("<ButtonRelease-1>", display_details)

    # Acknowledge Button
    acknowledge_button = ctk.CTkButton(main_content_frame, text="Acknowledge Alert", command=acknowledge_alert)
    acknowledge_button.pack(pady=10)

# Top Navigation Bar
nav_bar = ctk.CTkFrame(app, height=50, corner_radius=0)
nav_bar.grid(row=0, column=0, columnspan=2, sticky="ew")

toggle_button = ctk.CTkButton(nav_bar, text="X", command=toggle_sidebar, width=50)
toggle_button.pack(side="left", padx=10, pady=5)

nav_title = ctk.CTkLabel(nav_bar, text="Guardian", font=("Arial", 18))
nav_title.pack(side="left", padx=20)

# Sidebar Frame
sidebar_frame = ctk.CTkFrame(app, width=200, corner_radius=0)
sidebar_frame.grid(row=1, column=0, sticky="ns")

# Sidebar Buttons
buttons = [
    {"text": "Dashboard", "command": open_dashboard_page},
    {"text": "Alerts", "command": show_alerts_page},
    {"text": "Incident Response History", "command": lambda: update_main_content("Incident Response Content")},
    {"text": "System Status", "command": lambda: update_main_content("Status...")},
    {"text": "Contact Us", "command": lambda: update_main_content("Contact Us")},
    {"text": "About System", "command":open_about_page},
    {"text": "Settings", "command": lambda: update_main_content("Settings Content")},
]
for button in buttons:
    ctk.CTkButton(sidebar_frame, text=button["text"], command=button["command"]).pack(pady=10, padx=10, fill="x")

# Main Content Frame
main_content_frame = ctk.CTkFrame(app, corner_radius=10)
main_content_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

# Default Content
def update_main_content(message):
    for widget in main_content_frame.winfo_children():
        widget.destroy()
    label = ctk.CTkLabel(main_content_frame, text=message, font=("Arial", 20))
    label.pack(expand=True)

# Grid configuration
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(1, weight=1)

# Show Alerts Page by Default
show_alerts_page()

# Run the app
app.mainloop()
