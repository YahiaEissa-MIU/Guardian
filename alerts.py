import tkinter as tk
from tkinter import ttk

# Sample data with multiple alerts
alerts_data = [
    {"timestamp": "2024-11-22 10:45", "severity": "Critical", "type": "Locky", "file": "document1.docx", "actions": "Quarantined"},
    {"timestamp": "2024-11-22 11:15", "severity": "Medium", "type": "Cerber", "file": "spreadsheet.xls", "actions": "Blocked Access"},
    {"timestamp": "2024-11-22 11:30", "severity": "Low", "type": "Wannacry", "file": "notes.txt", "actions": "Logged"},
    {"timestamp": "2024-11-22 12:00", "severity": "Critical", "type": "Ryuk", "file": "invoice.pdf", "actions": "Quarantined"},
    {"timestamp": "2024-11-22 12:15", "severity": "Medium", "type": "Sodinokibi", "file": "backup.zip", "actions": "Blocked Access"},
    {"timestamp": "2024-11-22 12:30", "severity": "Low", "type": "Petya", "file": "readme.md", "actions": "Logged"},
]

# Function to display alert details
def display_details(event):
    selected_item = tree.focus()
    if not selected_item:
        return
    alert_details = tree.item(selected_item, "values")
    details_text.set(
        f"Type: {alert_details[1]}\n"
        f"Affected File: {alert_details[2]}\n"
        f"Actions Taken: {alert_details[3]}"
    )

# Function to handle Acknowledge button click
def acknowledge_alert():
    selected_item = tree.focus()
    if not selected_item:
        details_text.set("Please select an alert to acknowledge.")
        return
    tree.delete(selected_item)
    details_text.set("Alert acknowledged and removed.")

# Tkinter window setup
root = tk.Tk()
root.title("Ransomware Alerts Dashboard")
root.geometry("800x500")
root.configure(bg="white")

# Header Frame
header_frame = tk.Frame(root, bg="red")
header_frame.pack(fill=tk.X)
header_label = tk.Label(
    header_frame, text="Ransomware Alerts", bg="red", fg="white", font=("Arial", 20, "bold")
)
header_label.pack(pady=5)

# Main Content Frame
content_frame = tk.Frame(root, bg="white")
content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Treeview with Scrollbar
tree_frame = tk.Frame(content_frame, bg="white")
tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

columns = ("Timestamp", "Type", "File", "Actions")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)

# Scrollbar for Treeview
scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Define Treeview Columns
tree.heading("Timestamp", text="Timestamp")
tree.heading("Type", text="Threat Type")
tree.heading("File", text="Affected File")
tree.heading("Actions", text="Actions Taken")
tree.column("Timestamp", width=150, anchor=tk.CENTER)
tree.column("Type", width=150, anchor=tk.CENTER)
tree.column("File", width=200, anchor=tk.W)
tree.column("Actions", width=150, anchor=tk.CENTER)

# Insert Data into Treeview
for alert in alerts_data:
    severity = alert["severity"]
    color = "red" if severity == "Critical" else "orange" if severity == "Medium" else "green"
    tree.insert("", "end", values=(alert["timestamp"], alert["type"], alert["file"], alert["actions"]), tags=(color,))
tree.pack(fill=tk.BOTH, expand=True)

# Configure Severity Colors
tree.tag_configure("red", foreground="red")
tree.tag_configure("orange", foreground="orange")
tree.tag_configure("green", foreground="green")

# Details Frame
details_frame = tk.Frame(content_frame, bg="white", padx=10, pady=10)
details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

details_label = tk.Label(details_frame, text="Alert Details", bg="white", fg="black", font=("Arial", 14, "bold"))
details_label.pack(anchor=tk.W)

details_text = tk.StringVar()
details_box = tk.Label(details_frame, textvariable=details_text, bg="white", fg="black", font=("Arial", 12), justify=tk.LEFT, anchor="nw", wraplength=300)
details_box.pack(fill=tk.BOTH, expand=True)

# Button Frame
button_frame = tk.Frame(details_frame, bg="white")
button_frame.pack(fill=tk.X, pady=10)

acknowledge_button = tk.Button(button_frame, text="Acknowledge Alert", bg="red", fg="white", font=("Arial", 12), command=acknowledge_alert)
acknowledge_button.pack(side=tk.LEFT, padx=5)

investigate_button = tk.Button(button_frame, text="Investigate", bg="white", fg="black", font=("Arial", 12), command=lambda: details_text.set("Investigate functionality is not implemented yet."))
investigate_button.pack(side=tk.LEFT, padx=5)

# Bind Treeview Selection Event
tree.bind("<<TreeviewSelect>>", display_details)

# Run the App
root.mainloop()
