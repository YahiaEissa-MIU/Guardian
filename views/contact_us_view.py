import customtkinter as ctk
from tkinter import messagebox


class ContactView(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color="transparent")
        self.char_counter = None
        self.controller = controller
        self.feedback_textbox = None
        self.create_contact_us_page()

    def set_controller(self, controller):
        """Sets the controller reference"""
        self.controller = controller

    def create_contact_us_page(self):
        # Main container frame
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)
        main_frame.pack_propagate(False)  # Prevent shrinking

        # Title Section
        title_label = ctk.CTkLabel(main_frame,
                                   text="Contact Support",
                                   font=("Arial", 24, "bold"),
                                   )
        title_label.pack(pady=(0, 20))

        # Contact Information Card
        info_card = ctk.CTkFrame(main_frame, corner_radius=12, border_width=1, border_color="#e0e0e0")
        info_card.pack(fill="x", pady=10)

        contact_info = [
            ("📧 Email:", "GUARDIANSUPPORT@GMAIL.COM"),
            ("🕒 Support Hours:", "Mon-Fri: 9:00 AM - 5:00 PM EST"),
            ("📞 Emergency Hotline:", "+1 (555) 123-4567")
        ]

        for icon, text in contact_info:
            row = ctk.CTkFrame(info_card, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=4)
            ctk.CTkLabel(row, text=icon, font=("Arial", 14), width=40).pack(side="left")
            ctk.CTkLabel(row, text=text, font=("Arial", 14), anchor="w").pack(side="left", fill="x", expand=True)

        # Feedback Form
        ctk.CTkLabel(main_frame, text="Message", font=("Arial", 16, "bold"), anchor="w").pack(fill="x", pady=(10, 5))

        self.feedback_textbox = ctk.CTkTextbox(main_frame, width=600, height=100, corner_radius=8,
                                               border_width=1, border_color="#e0e0e0", font=("Arial", 14))
        self.feedback_textbox.pack(fill="x", pady=5)
        self.feedback_textbox.insert("1.0", "Please write your message here...")
        self.feedback_textbox.bind("<FocusIn>", self.clear_placeholder)

        # Character counter
        self.char_counter = ctk.CTkLabel(main_frame, text="0/1000 characters", font=("Arial", 12), text_color="#666666")
        self.char_counter.pack(anchor="e", pady=(5, 0))
        self.feedback_textbox.bind("<KeyRelease>", self.update_char_counter)

        # Submit Button (Now visible!)
        submit_button = ctk.CTkButton(main_frame, text="Send Message", command=self.submit_feedback,
                                      width=180, height=40, font=("Arial", 14, "bold"),
                                      )
        submit_button.pack(pady=15)  # Increased bottom padding

    def clear_placeholder(self, event):
        if self.feedback_textbox.get("1.0", "end-1c") == "Please write your message here...":
            self.feedback_textbox.delete("1.0", "end")
            self.feedback_textbox.configure(text_color="#000000")

    def update_char_counter(self, event):
        content = self.feedback_textbox.get("1.0", "end-1c")
        length = len(content)
        self.char_counter.configure(text=f"{length}/1000 characters")
        self.char_counter.configure(text_color="red" if length > 1000 else "#666666")

    def submit_feedback(self):
        """Handles feedback submission with controller"""
        feedback = self.feedback_textbox.get("1.0", "end-1c").strip()

        if not feedback or feedback == "Please write your message here...":
            messagebox.showwarning("Empty Message", "Please write your message before submitting.", parent=self)
            return

        if self.controller:
            title, message, msg_type = self.controller.handle_feedback(feedback)
            if msg_type == "info":
                messagebox.showinfo(title, message, parent=self)
                self.feedback_textbox.delete("1.0", "end")
                self.char_counter.configure(text="0/1000 characters", text_color="#666666")
            else:
                messagebox.showwarning(title, message, parent=self)
