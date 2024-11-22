import tkinter as tk

# Function to handle version updates button (placeholder for future functionality)
def check_for_updates():
    update_message.set("You are using the latest version. No updates available.")

# Tkinter window setup
root = tk.Tk()
root.title("About Guardian")
root.geometry("600x400")
root.configure(bg="white")

# Header Frame
header_frame = tk.Frame(root, bg="red")
header_frame.pack(fill=tk.X)

header_label = tk.Label(
    header_frame, text="About Guardian", bg="red", fg="white", font=("Arial", 20, "bold")
)
header_label.pack(pady=5)

# Content Frame
content_frame = tk.Frame(root, bg="white", padx=20, pady=20)
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
    "- Contributor: Ali Ahmed\n"
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

# Run the App
root.mainloop()
