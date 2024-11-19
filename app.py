import customtkinter as ctk

# Initialize the app
app = ctk.CTk()
app.geometry("1200x600")
app.title("Guardian")

# Sidebar visibility flag
sidebar_visible = True


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

# Sidebar Frame
sidebar_frame = ctk.CTkFrame(app, width=200, corner_radius=0)
sidebar_frame.grid(row=1, column=0, sticky="ns")

sidebar_label = ctk.CTkLabel(sidebar_frame, text="Menu", font=("Arial", 16))
sidebar_label.pack(pady=20)

dashboard_button = ctk.CTkButton(sidebar_frame, text="Dashboard", command=lambda: update_dashboard())
dashboard_button.pack(pady=10, padx=10, fill="x")

scan_button = ctk.CTkButton(sidebar_frame, text="Alerts", command=lambda: update_main_content("Viewing Alerts..."))
scan_button.pack(pady=10, padx=10, fill="x")

alerts_button = ctk.CTkButton(sidebar_frame, text="Threat Reports",
                              command=lambda: update_main_content("Loading Threats..."))
alerts_button.pack(pady=10, padx=10, fill="x")

settings_button = ctk.CTkButton(sidebar_frame, text="Settings", command=lambda: update_main_content("Settings Page..."))
settings_button.pack(pady=10, padx=10, fill="x")

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


# Set the initial dashboard
update_dashboard()

# Configure row/column weights for responsiveness
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(1, weight=1)

# Run the application
app.mainloop()
