import customtkinter as ctk
from router import Router

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Guardian")
        self.geometry("1200x600")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.sidebar_visible = True

        # Navigation Bar
        self.nav_bar = ctk.CTkFrame(self, height=50, corner_radius=0)
        self.nav_bar.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.toggle_button = ctk.CTkButton(
            self.nav_bar,
            text="≡",  # Hamburger icon
            command=self.toggle_sidebar,
            width=50,
            fg_color="transparent",
            hover_color=("gray70", "gray30")
        )
        self.toggle_button.pack(side="left", padx=10, pady=5)

        self.nav_title = ctk.CTkLabel(self.nav_bar, text="Guardian", font=("Arial", 18, "bold"))
        self.nav_title.pack(side="left", padx=20)

        # Sidebar with improved styling
        self.sidebar_frame = ctk.CTkFrame(
            self,
            width=200,
            corner_radius=15,
            fg_color=("gray90", "gray13")  # Slightly different background
        )
        self.sidebar_frame.grid(row=1, column=0, sticky="ns", padx=(10, 0), pady=10)

        # Sidebar Header
        self.sidebar_header = ctk.CTkLabel(
            self.sidebar_frame,
            text="Menu",
            font=("Arial", 14, "bold"),
            pady=15
        )
        self.sidebar_header.pack(fill="x")

        # Sidebar Buttons with improved styling
        button_options = {
            "anchor": "w",
            "corner_radius": 8,
            "fg_color": "transparent",
            "hover_color": ("gray80", "gray20"),
            "border_spacing": 10,
            "font": ("Arial", 14),
            "height": 40
        }

        self.dashboard_button = ctk.CTkButton(
            self.sidebar_frame,
            text=" Dashboard",
            command=lambda: self.router.show("dashboard"),
            **button_options
        )
        self.dashboard_button.pack(fill="x", padx=10, pady=(0, 5))

        self.alerts_button = ctk.CTkButton(
            self.sidebar_frame,
            text=" Alerts",
            command=lambda: self.router.show("alerts"),
            **button_options
        )
        self.alerts_button.pack(fill="x", padx=10, pady=5)

        self.status_button = ctk.CTkButton(
            self.sidebar_frame,
            text=" System Status",
            command=lambda: self.router.show("system_status"),
            **button_options
        )
        self.status_button.pack(fill="x", padx=10, pady=5)

        self.incident_button = ctk.CTkButton(
            self.sidebar_frame,
            text=" Incident History",
            command=lambda: self.router.show("incident_history"),
            **button_options
        )
        self.incident_button.pack(fill="x", padx=10, pady=5)

        self.about_system_button = ctk.CTkButton(
            self.sidebar_frame,
            text=" About System",
            command=lambda: self.router.show("about_system"),
            **button_options
        )
        self.about_system_button.pack(fill="x", padx=10, pady=5)

        self.contact_button = ctk.CTkButton(
            self.sidebar_frame,
            text=" Contact Us",
            command=lambda: self.router.show("contact_us"),
            **button_options
        )
        self.contact_button.pack(fill="x", padx=10, pady=5)

        self.settings_button = ctk.CTkButton(
            self.sidebar_frame,
            text=" Settings",
            command=lambda: self.router.show("settings"),
            **button_options
        )
        self.settings_button.pack(fill="x", padx=10, pady=(5, 15))

        # Main Content Frame
        self.main_content_frame = ctk.CTkFrame(
            self,
            corner_radius=15,
            fg_color=("gray95", "gray10")
        )
        self.main_content_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.main_content_frame.grid_rowconfigure(0, weight=1)
        self.main_content_frame.grid_columnconfigure(0, weight=1)

        self.router = Router(self)
        self.router.show("dashboard")

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar_frame.grid_forget()
            self.toggle_button.configure(text="≡")
        else:
            self.sidebar_frame.grid(row=1, column=0, sticky="ns", padx=(10, 0), pady=10)
            self.toggle_button.configure(text="✕")  # X icon
        self.sidebar_visible = not self.sidebar_visible


app = App()
app.mainloop()
