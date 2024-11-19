import customtkinter as ctk

# Create the application window
app = ctk.CTk()
app.geometry("600x400")
app.title("Ransomware Defense")

# Add a label
label = ctk.CTkLabel(app, text="Welcome to Ransomware Defense App", font=("Arial", 20))
label.pack(pady=20)


# Add a button
def on_scan_click():
    print("Scan started...")
    # Connect to backend logic for scanning


scan_button = ctk.CTkButton(app, text="Start Scan", command=on_scan_click)
scan_button.pack(pady=10)

# Run the app
app.mainloop()
