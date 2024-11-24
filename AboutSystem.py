import customtkinter as ctk
import subprocess  # For launching other scripts

# Function to handle version updates button (placeholder for future functionality)
def check_for_updates():
    update_message.set("You are using the latest version. No updates available.")

# Function to switch between pages
def show_frame(frame):
    frame.tkraise()

# Function to open the alert page (alert.py)
def open_alert_page():
    subprocess.run(["python", "alerts.py"])

# Function to open the dashboard page (app.py)
def open_dashboard_page():
    subprocess.run(["python", "app.py"])

# Function to open the About System page (AboutSystem.py)
def open_about_page():
    subprocess.run(["python", "AboutSystem.py"])

# Initialize the app
app = ctk.CTk()
app.geometry("1200x700")
app.title("Guardian")

# Sidebar visibility toggle
sidebar_visible = True

def toggle_sidebar():
    global sidebar_visible
    if sidebar_visible:
        sidebar_frame.grid_forget()  # Hide sidebar
        toggle_button.configure(text="☰")  # Show menu icon
    else:
        sidebar_frame.grid(row=1, column=0, sticky="ns")  # Show sidebar
        toggle_button.configure(text="X")  # Show close icon
    sidebar_visible = not sidebar_visible

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
    {"text": "Alerts", "command": open_alert_page},
    {"text": "Incident Response History", "command": lambda: update_main_content("Incident Response Content")},
    {"text": "System Status", "command": lambda: update_main_content("Status...")},
    {"text": "Contact Us", "command": lambda: update_main_content("Contact Us")},
    {"text": "About System", "command": open_about_page},
    {"text": "Settings", "command": lambda: update_main_content("Settings Content")},
]
for button in buttons:
    ctk.CTkButton(sidebar_frame, text=button["text"], command=button["command"], width=150).pack(pady=10, padx=10, fill="x")

# Main Content Frame
main_content_frame = ctk.CTkFrame(app, corner_radius=10)
main_content_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

# Pages within the main content frame
alert_page = ctk.CTkFrame(main_content_frame, corner_radius=10)
about_page = ctk.CTkFrame(main_content_frame, corner_radius=10)

for frame in (alert_page, about_page):
    frame.grid(row=0, column=0, sticky="nsew")

# -------------------- About Page --------------------
about_header = ctk.CTkLabel(
    about_page, text="About Guardian", font=("Arial", 20, "bold")
)
about_header.pack(fill="x", pady=5)

content_frame = ctk.CTkFrame(about_page)
content_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Overview Section
overview_label = ctk.CTkLabel(
    content_frame,
    text="Guardian: Your Ransomware Detection and Response Solution",
    font=("Arial", 14, "bold"),
)
overview_label.pack(anchor="w", pady=(0, 10))

overview_text = (
    "Guardian is an advanced desktop application that uses SOAR and Splunk "
    "to detect ransomware threats in real-time. Powered by threat intelligence, "
    "it provides automated responses to neutralize potential risks, ensuring "
    "the safety and integrity of your data."
)
overview_box = ctk.CTkLabel(
    content_frame,
    text=overview_text,
    font=("Arial", 12),
    wraplength=550,
    justify="left",
)
overview_box.pack(anchor="w", pady=(0, 20))

# Credits Section
credits_label = ctk.CTkLabel(
    content_frame, text="Developers & Contributors:", font=("Arial", 14, "bold")
)
credits_label.pack(anchor="w", pady=(10, 5))

credits_text = (
    "- Lead Developer: Yahia Eissa\n"
    "- Contributor: Nada Abdelrahman\n"
    "- Contributor: Donya Hany\n"
    "- Contributor: Abdelrahman Walid\n"
    "- Contributor: Ali Ahmed\n"
)
credits_box = ctk.CTkLabel(
    content_frame, text=credits_text, font=("Arial", 12), justify="left"
)
credits_box.pack(anchor="w", pady=(0, 20))

# Version Section
version_label = ctk.CTkLabel(
    content_frame, text="Version Information:", font=("Arial", 14, "bold")
)
version_label.pack(anchor="w", pady=(10, 5))

version_text = (
    "Guardian Version: 1.0.0\n"
    "Last Updated: November 22, 2024"
)
version_box = ctk.CTkLabel(
    content_frame, text=version_text, font=("Arial", 12), justify="left"
)
version_box.pack(anchor="w", pady=(0, 10))

# Check for Updates Button
update_message = ctk.StringVar(value="")

update_button = ctk.CTkButton(
    content_frame, text="Check for Updates", command=check_for_updates
)
update_button.pack(anchor="w", pady=5)

update_label = ctk.CTkLabel(
    content_frame, textvariable=update_message, font=("Arial", 12)
)
update_label.pack(anchor="w", pady=(5, 0))

# Footer Frame
footer_frame = ctk.CTkFrame(app, height=30, corner_radius=0)
footer_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

footer_label = ctk.CTkLabel(
    footer_frame, text="© 2024 Guardian Team. All rights reserved.", font=("Arial", 10)
)
footer_label.pack(pady=5)

# Run the app
app.mainloop()
