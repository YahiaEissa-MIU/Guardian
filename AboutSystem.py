import customtkinter as ctk
import tkinter as tk
import subprocess

# Function to check for updates
def check_for_updates():
    update_message.set("You are using the latest version. No updates available.")

# Initialize the app
app = ctk.CTk()
app.state("zoomed")  # Set window to fullscreen mode
app.title("Guardian")

# Function to open the alert page (alerts.py)
def open_alert_page():
    subprocess.run(["python", "alerts.py"])

# Function to open the dashboard page (app.py)
def open_dashboard_page():
    subprocess.run(["python", "app.py"])

# Configure grid layout for the app
app.grid_rowconfigure(0, weight=0)  # Row for the top navbar
app.grid_rowconfigure(1, weight=1)  # Row for the main content area
app.grid_columnconfigure(1, weight=1)  # Main content area takes the remaining space

# Sidebar Frame
sidebar_frame = ctk.CTkFrame(app, width=200, corner_radius=0)
sidebar_frame.grid(row=1, column=0, sticky="ns")  # Sidebar at row 1, column 0

# Sidebar Buttons
buttons = [
    {"text": "Dashboard", "command": open_dashboard_page},
    {"text": "Alerts", "command": open_alert_page},
    {"text": "Incident Response History", "command": lambda: print("Incident clicked")},
    {"text": "System Status", "command": lambda: print("System clicked")},
    {"text": "Contact Us", "command": lambda: print("Contact clicked")},
    {"text": "About System", "command": lambda: print("About clicked")},
    {"text": "Settings", "command": lambda: print("Settings clicked")},
]
for button in buttons:
    ctk.CTkButton(sidebar_frame, text=button["text"], width=150).pack(pady=10, padx=10, fill="x")

# Main Content Frame
main_content_frame = ctk.CTkFrame(app, corner_radius=10)
main_content_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

# Add a scrollable canvas to make the page scrollable
canvas = tk.Canvas(main_content_frame, bg="gray90", highlightthickness=0)
scrollbar = ctk.CTkScrollbar(
    main_content_frame, orientation="vertical", command=canvas.yview
)
scrollable_frame = ctk.CTkFrame(canvas, corner_radius=10)

scrollable_frame.bind(
    "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Content Header
header = ctk.CTkLabel(
    scrollable_frame, text="About Guardian", font=("Arial", 20, "bold")
)
header.pack(pady=(10, 20))

# Purpose Section
purpose_section = ctk.CTkFrame(scrollable_frame, corner_radius=10)
purpose_section.pack(fill="x", padx=10, pady=10)

purpose_header = ctk.CTkLabel(
    purpose_section, text="Purpose", font=("Arial", 16, "bold")
)
purpose_header.pack(anchor="w", pady=(5, 10), padx=10)

# Purpose Content with bold headers
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
overview_section = ctk.CTkFrame(scrollable_frame, corner_radius=10)
overview_section.pack(fill="x", padx=10, pady=10)

overview_header = ctk.CTkLabel(
    overview_section, text="Overview of Guardian’s Objectives", font=("Arial", 16, "bold")
)
overview_header.pack(anchor="w", pady=(5, 10), padx=10)

overview_content = (
    "The application is a desktop interface designed for end-users.\n\n"
    "Integration: It integrates with Splunk's Security Information and Event Management (SIEM) system and utilizes a customized Security Orchestration, Automation, and Response (SOAR) solution.\n\n"
    "Functionality: The application will provide real-time alerts, enable isolation of infected files, and facilitate automated recovery processes."
)
ctk.CTkLabel(
    overview_section, text=overview_content, font=("Arial", 12), wraplength=900, justify="left"
).pack(anchor="w", padx=10, pady=10)

# Developers & Contributors Section
developers_section = ctk.CTkFrame(scrollable_frame, corner_radius=10)
developers_section.pack(fill="x", padx=10, pady=10)

developers_header = ctk.CTkLabel(
    developers_section, text="Developers & Contributors", font=("Arial", 16, "bold")
)
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
version_section = ctk.CTkFrame(scrollable_frame, corner_radius=10)
version_section.pack(fill="x", padx=10, pady=10)

version_header = ctk.CTkLabel(
    version_section, text="Version Details", font=("Arial", 16, "bold")
)
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

# Top Navigation Bar
nav_bar = ctk.CTkFrame(app, height=50, corner_radius=0)
nav_bar.grid(row=0, column=0, columnspan=2, sticky="ew")  # Placed at the top, row 0

toggle_button = ctk.CTkButton(nav_bar, text="☰", width=40, command=toggle_sidebar)
toggle_button.pack(side="left", padx=10)


# Title in the navigation bar
title_label = ctk.CTkLabel(nav_bar, text="Guardian", font=("Arial", 18, "bold"))
title_label.pack(side="left", padx=20)

sidebar_visible = True  # Track the sidebar visibility

app.mainloop()
