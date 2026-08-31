import customtkinter as ctk
from PIL import Image
from pathlib import Path
from helperFiles.toast import show_toast
from helperFiles.center_window_on_screen import center_window_on_screen
from helperFiles.localDataManager import *

class Login(ctk.CTkToplevel):
    def __init__(self, parent=None, on_submit=None):
        super().__init__(parent)
        ctk.register_project_fonts(self, Path(__file__).resolve().parent / "assets" / "fonts")
        self.title("Login")
        self.geometry("520x500")
        self.minsize(335, 380)
        self.grab_set()
        self.after(50, lambda: center_window_on_screen(self, 520, 500))  # Center the window after it has been created

        # ====== Initialize variables ======
        self.username_data = None
        self.password_data = None
        self.remember_username_data = None
        self.request_signup_flag = False
        self.on_submit = on_submit

        # ====== Build the UI ======
        self.protocol("WM_DELETE_WINDOW", self._close_dialog)
        self._build_ui()

        self.bind("<Return>", lambda event: self.submit_login())
        self.bind("<Escape>", lambda event: self._close_dialog())
        self.bind("<space>", lambda event: print(self.geometry()))
        if rememberUsername() and rememberUsername() != False:
            self.after(100, self.field_password.focus_set)
        else:
            self.after(100, self.field_username.focus_set)

    def _build_ui(self):
        # Preload images so they are not garbage-collected
        self.eye_img = ctk.CTkImage(light_image=Image.open('assets/images/eye.png'), dark_image=Image.open('assets/images/eye.png'), size=(20, 20))
        self.eye_off_img = ctk.CTkImage(light_image=Image.open('assets/images/eye-off.png'), dark_image=Image.open('assets/images/eye-off.png'), size=(20, 20))

        self.main_cont_v = ctk.CTkFrame(
            self,
            width=520,
            height=380,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='#2b2b2b',
        )
        self.main_cont_v.place(relwidth=1.0, relheight=1.0, x=0, y=0)

        self.main_cont_v.pack_propagate(False)
        self.main_cont_v.grid_propagate(False)

        self.login_title = ctk.CTkLabel(
            self.main_cont_v,
            width=500,
            corner_radius=0,
            padx=0,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text='LOGIN',
            font_wrap=True,
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
            font=ctk.CTkFont(family='Ravie', size=50, weight="normal", slant="roman"),
        )
        self.login_title.pack(side="top", fill="both", expand=True, pady=2)
        self.login_title._ctkmaker_min = 16

        self.username = ctk.CTkFrame(
            self.main_cont_v,
            width=520,
            height=50,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.username.pack(side="top", pady=2)
        self.username._ctkmaker_min = 20
        self.username._ctkmaker_fixed = True

        self.username.pack_propagate(False)
        self.username.grid_propagate(False)

        self.label_username = ctk.CTkLabel(
            self.username,
            width=110,
            height=50,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=10,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text='Username',
            font_wrap=True,
            anchor='w',
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
            font=ctk.CTkFont(size=20, weight="normal", slant="roman"),
        )
        self.label_username.pack(side="left", padx=2)
        self.label_username._ctkmaker_min = 132
        self.label_username._ctkmaker_fixed = True

        self.field_username = ctk.CTkEntry(
            self.username,
            height=40,
            corner_radius=10,
            border_width=2,
            border_color='#565b5e',
            placeholder_text='Enter username…',
            fg_color='#343638',
            text_color='#dce4ee',
            placeholder_text_color='#9ea0a2',
            justify='left',
        )
        self.field_username.pack(side="left", fill="both", expand=True, padx=2)
        self.field_username._ctkmaker_min = 50
        if rememberUsername() and rememberUsername() != False:
            self.field_username.insert(0, rememberUsername())

        self.username.bind("<Configure>", lambda _e, _c=self.username: ctk.balance_pack(_c, 'width'))

        self.password = ctk.CTkFrame(
            self.main_cont_v,
            width=520,
            height=50,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.password.pack(side="top", pady=2)
        self.password._ctkmaker_min = 20
        self.password._ctkmaker_fixed = True

        self.password.pack_propagate(False)
        self.password.grid_propagate(False)

        self.label_password = ctk.CTkLabel(
            self.password,
            width=110,
            height=50,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=10,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text='Password',
            font_wrap=True,
            anchor='w',
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
            font=ctk.CTkFont(size=20, weight="normal", slant="roman"),
        )
        self.label_password.pack(side="left", padx=2)
        self.label_password._ctkmaker_min = 126
        self.label_password._ctkmaker_fixed = True

        self.field_password = ctk.CTkEntry(
            self.password,
            height=40,
            corner_radius=10,
            border_width=2,
            border_color='#565b5e',
            placeholder_text='Enter password…',
            fg_color='#343638',
            text_color='#dce4ee',
            placeholder_text_color='#9ea0a2',
            justify='left',
            show="•",
        )
        self.field_password.pack(side="left", fill="both", expand=True, padx=2)
        self.field_password._ctkmaker_min = 50

        self.show_hide_password = ctk.CTkButton(
            self.password,
            width=150,
            height=40,
            corner_radius=6,
            border_width=0,
            border_color='#efefef',
            text='Show Password',
            text_color='#ffffff',
            full_circle=True,
            fg_color='transparent',
            pressed_color='#2b2b2b',
            image=self.eye_img,
            command=self._toggle_password,
        )
        self.show_hide_password.pack(side="left", padx=2)
        self.show_hide_password._ctkmaker_min = 40
        self.show_hide_password._ctkmaker_fixed = True

        self.password.bind("<Configure>", lambda _e, _c=self.password: ctk.balance_pack(_c, 'width'))

        self.remember_username = ctk.CTkCheckBox(
            self.main_cont_v,
            width=20,
            height=10,
            corner_radius=6,
            border_width=3,
            border_color='#949A9F',
            checkmark_color='#e5e5e5',
            text='Remember Username',
            text_color='#dce4ee',
            text_color_disabled='#737373',
        )
        self.remember_username.pack(side="top", pady=2)
        self.remember_username._ctkmaker_min = 28
        self.remember_username._ctkmaker_fixed = True
        self.remember_username.select()

        self.login_button = ctk.CTkButton(
            self.main_cont_v,
            height=32,
            corner_radius=6,
            border_width=0,
            border_color='#efefef',
            text='Login',
            text_color='#ffffff',
            full_circle=True,
            command=self.submit_login,
        )
        self.login_button.pack(side="top", pady=2)
        self.login_button._ctkmaker_min = 32
        self.login_button._ctkmaker_fixed = True

        self.create_cont_v = ctk.CTkFrame(
            self.main_cont_v,
            width=240,
            height=180,
            corner_radius=6,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.create_cont_v.pack(side="top", fill="both", expand=True, pady=2)
        self.create_cont_v._ctkmaker_min = 20

        self.create_cont_v.pack_propagate(False)
        self.create_cont_v.grid_propagate(False)

        self.label_create = ctk.CTkLabel(
            self.create_cont_v,
            width=365,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=0,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text="Don't Have an Account?",
            font_wrap=True,
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
            font=ctk.CTkFont(size=30, weight="normal", slant="roman"),
        )
        self.label_create.pack(side="top", pady=2)
        self.label_create._ctkmaker_min = 16
        self.label_create._ctkmaker_fixed = True

        self.button_create = ctk.CTkButton(
            self.create_cont_v,
            width=185,
            height=52,
            corner_radius=6,
            border_width=0,
            border_color='#efefef',
            text='Create One',
            text_color='#ffffff',
            full_circle=True,
            font=ctk.CTkFont(size=30, weight="normal", slant="roman"),
            command=self.request_signup,
        )
        self.button_create.pack(side="top", pady=2)
        self.button_create._ctkmaker_min = 32
        self.button_create._ctkmaker_fixed = True

        self.create_cont_v.bind("<Configure>", lambda _e, _c=self.create_cont_v: ctk.balance_pack(_c, 'height'))

        self.main_cont_v.bind("<Configure>", lambda _e, _c=self.main_cont_v: ctk.balance_pack(_c, 'height'))

    def _close_dialog(self):
        self.username_data = None
        self.password_data = None
        self.remember_username_data = None
        self.destroy()

    def request_signup(self):
        self.request_signup_flag = True
        self.destroy()

    def _toggle_password(self):
        current = self.field_password.cget("show")
        new_show = "" if current == "•" else "•"
        self.field_password.configure(show=new_show)
        self.show_hide_password.configure(
            image=self.eye_off_img if new_show == "" else self.eye_img,
            text="Hide Password" if new_show == "" else "Show Password",
        )

    def submit_login(self):
        username = self.field_username.get().strip()
        password = self.field_password.get()

        if not username or not password:
            show_toast(self, "Please enter both a username and password.", type="error")
            return

        self.username_data = username
        self.password_data = password
        self.remember_username_data = self.remember_username.get()

        if callable(self.on_submit):
            if self.on_submit(username, password, self.remember_username_data):
                self.destroy()
                return

        self.field_password.delete(0, "end")
        self.field_password.focus_set()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    app = Login(root)
    root.mainloop()
