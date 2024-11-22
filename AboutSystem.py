import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import subprocess  # Used for opening the alert page (alert.py)

# Function to handle version updates button (placeholder for future functionality)
def check_for_updates():
    update_message.set("You are using the latest version. No updates available.")

# Function to switch between pages
def show_frame(frame):
    frame.tkraise()

# Function to open the alert page (alert.py)
def open_alert_page():
    subprocess.run(["python", "alerts.py"])

# Tkinter window setup
root = tk.Tk()
root.title("Guardian - Ransomware Detection System")
root.geometry("900x600")
root.configure(bg="white")


# Function to resize image icons (updated for newer Pillow versions)
def resize_icon(image_path, size=(40, 40)):
    image = Image.open(image_path)
    image = image.resize(size, Image.Resampling.LANCZOS)  # Replaced ANTIALIAS with LANCZOS
    return ImageTk.PhotoImage(image)


# Create resized navigation icons
alert_icon = resize_icon("alert.png")  # Replace with actual icon path
about_icon = resize_icon("about.png")  # Replace with actual icon path

# Vertical Navigation Bar
nav_bar = tk.Frame(root, bg="red", width=150)
nav_bar.pack(side=tk.LEFT, fill=tk.Y)

# Navigation Buttons

alert_button = tk.Button(
    nav_bar,
    text="Alerts",
    image=alert_icon,
    compound="top",
    bg="red",
    fg="white",
    font=("Arial", 12, "bold"),
    command=open_alert_page,  # Link to alert.py page
    relief=tk.FLAT
)
alert_button.pack(pady=20)

about_button = tk.Button(
    nav_bar,
    text="About",
    image=about_icon,
    compound="top",
    bg="red",
    fg="white",
    font=("Arial", 12, "bold"),
    command=lambda: show_frame(about_page),
    relief=tk.FLAT
)
about_button.pack(pady=20)



# Container for pages
main_frame = tk.Frame(root, bg="white")
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Pages
alert_page = tk.Frame(main_frame, bg="white")
about_page = tk.Frame(main_frame, bg="white")

for frame in (alert_page, about_page):
    frame.grid(row=0, column=0, sticky="nsew")

# -------------------- About Page --------------------
about_header = tk.Label(
    about_page, text="About Guardian", bg="red", fg="white", font=("Arial", 20, "bold")
)
about_header.pack(fill=tk.X, pady=5)

# Content Frame for About Page
content_frame = tk.Frame(about_page, bg="white", padx=20, pady=20)
content_frame.pack(fill=tk.BOTH, expand=True)

# Overview Section
overview_label = tk.Label(
    content_frame,
    text="Guardian: Your Ransomware Detection and Response Solution",
    bg="white",
    fg="black",
    font=("Arial", 14, "bold"),
    anchor="w",
)
overview_label.pack(anchor="w", pady=(0, 10))

overview_text = (
    "Guardian is an advanced desktop application that uses SOAR and Splunk "
    "to detect ransomware threats in real-time. Powered by threat intelligence, "
    "it provides automated responses to neutralize potential risks, ensuring "
    "the safety and integrity of your data."
)
overview_box = tk.Label(
    content_frame,
    text=overview_text,
    bg="white",
    fg="black",
    font=("Arial", 12),
    wraplength=550,
    justify="left",
)
overview_box.pack(anchor="w", pady=(0, 20))

# Credits Section
credits_label = tk.Label(
    content_frame, text="Developers & Contributors:", bg="white", fg="black", font=("Arial", 14, "bold"), anchor="w"
)
credits_label.pack(anchor="w", pady=(10, 5))

credits_text = (
    "- Lead Developer: Yahia Eissa\n"
    "- Contributor: Nada Abdelrahman\n"
    "- Contributor: Donya Hany\n"
    "- Contributor: Abdelrahman Walid\n"
    "- Contributor: Ali Ahmed \n"
)
credits_box = tk.Label(
    content_frame,
    text=credits_text,
    bg="white",
    fg="black",
    font=("Arial", 12),
    justify="left",
)
credits_box.pack(anchor="w", pady=(0, 20))

# Version Section
version_label = tk.Label(
    content_frame, text="Version Information:", bg="white", fg="black", font=("Arial", 14, "bold"), anchor="w"
)
version_label.pack(anchor="w", pady=(10, 5))

version_text = (
    "Guardian Version: 1.0.0\n"
    "Last Updated: November 22, 2024"
)
version_box = tk.Label(
    content_frame,
    text=version_text,
    bg="white",
    fg="black",
    font=("Arial", 12),
    justify="left",
)
version_box.pack(anchor="w", pady=(0, 10))

# Check for Updates Button
update_message = tk.StringVar(value="")
update_button = tk.Button(
    content_frame,
    text="Check for Updates",
    bg="red",
    fg="white",
    font=("Arial", 12),
    command=check_for_updates,
)
update_button.pack(anchor="w", pady=5)

update_label = tk.Label(
    content_frame, textvariable=update_message, bg="white", fg="black", font=("Arial", 12), anchor="w"
)
update_label.pack(anchor="w", pady=(5, 0))

# Footer Frame
footer_frame = tk.Frame(root, bg="red")
footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

footer_label = tk.Label(
    footer_frame, text="© 2024 Guardian Team. All rights reserved.", bg="red", fg="white", font=("Arial", 10)
)
footer_label.pack(pady=5)



# Run the application
root.mainloop()
