import time
import customtkinter as ctk
from PIL import Image
from pathlib import Path
from helperFiles.toast import show_toast
from helperFiles.center_window_on_screen import center_window_on_screen
from helperFiles.paths import resource_path

class Signup(ctk.CTkToplevel):
    def __init__(self, parent=None, on_submit=None):
        super().__init__(parent)
        ctk.register_project_fonts(self, Path(__file__).resolve().parent / "assets" / "fonts")
        self.title("Sign Up")
        self.geometry("520x500")
        self.minsize(400, 460)
        self.grab_set()
        time.sleep(0.1)  # Allow the window to be created before centering
        center_window_on_screen(self, 520, 500)  # Center the window after it has been created

        # ====== Initialize variables ======
        self.username_data = None
        self.password_data = None
        self.confirm_password_data = None
        self.remember_username_data = None
        self.request_signin_flag = False
        self.on_submit = on_submit

        # ====== Build the UI ======
        self._build_ui()

        self.bind("<Return>", lambda event: self.submit_signup())
        self.bind("<Escape>", lambda event: self._close_dialog())
        self.after(100, self.field_username.focus_set)

    def _build_ui(self):
        # Preload images so they are not garbage-collected
        self.eye_img = ctk.CTkImage(light_image=Image.open(resource_path('assets', 'images', 'eye.png')), dark_image=Image.open(resource_path('assets', 'images', 'eye.png')), size=(20, 20))
        self.eye_off_img = ctk.CTkImage(light_image=Image.open(resource_path('assets', 'images', 'eye-off.png')), dark_image=Image.open(resource_path('assets', 'images', 'eye-off.png')), size=(20, 20))

        self.protocol("WM_DELETE_WINDOW", self._close_dialog)

        self.main_cont_v = ctk.CTkFrame(
            self,
            width=520,
            height=440,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='#2b2b2b',
        )
        self.main_cont_v.place(relwidth=1.0, relheight=1.0, x=0, y=0)

        self.main_cont_v.pack_propagate(False)
        self.main_cont_v.grid_propagate(False)

        self.signup_title = ctk.CTkLabel(
            self.main_cont_v,
            width=500,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=0,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text='SIGN UP',
            font_wrap=True,
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
            font=ctk.CTkFont(family='Ravie', size=50, weight="normal", slant="roman"),
        )
        self.signup_title.pack(side="top", fill="both", expand=True, pady=2)
        self.signup_title._ctkmaker_min = 16

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
            width=190,
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
            width=190,
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
        self.show_hide_password._ctkmaker_min = 36
        self.show_hide_password._ctkmaker_fixed = True

        self.password.bind("<Configure>", lambda _e, _c=self.password: ctk.balance_pack(_c, 'width'))

        self.confirm_password = ctk.CTkFrame(
            self.main_cont_v,
            width=520,
            height=50,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.confirm_password.pack(side="top", pady=2)
        self.confirm_password._ctkmaker_min = 20
        self.confirm_password._ctkmaker_fixed = True

        self.confirm_password.pack_propagate(False)
        self.confirm_password.grid_propagate(False)

        self.label_confirm_password = ctk.CTkLabel(
            self.confirm_password,
            width=190,
            height=50,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=10,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text='Confirm Password',
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
        self.label_confirm_password.pack(side="left", padx=2)
        self.label_confirm_password._ctkmaker_min = 228
        self.label_confirm_password._ctkmaker_fixed = True

        self.field_confirm_password = ctk.CTkEntry(
            self.confirm_password,
            height=40,
            corner_radius=10,
            border_width=2,
            border_color='#565b5e',
            placeholder_text='Confirm password…',
            fg_color='#343638',
            text_color='#dce4ee',
            placeholder_text_color='#9ea0a2',
            justify='left',
            show="•",
        )
        self.field_confirm_password.pack(side="left", fill="both", expand=True, padx=2)
        self.field_confirm_password._ctkmaker_min = 50

        self.button_show_confirm_password = ctk.CTkButton(
            self.confirm_password,
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
            command=self._toggle_confirm_password,
        )
        self.button_show_confirm_password.pack(side="left", padx=2)
        self.button_show_confirm_password._ctkmaker_min = 36
        self.button_show_confirm_password._ctkmaker_fixed = True

        self.confirm_password.bind("<Configure>", lambda _e, _c=self.confirm_password: ctk.balance_pack(_c, 'width'))

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

        self.signup = ctk.CTkButton(
            self.main_cont_v,
            height=32,
            corner_radius=6,
            border_width=0,
            border_color='#efefef',
            text='Sign Up',
            text_color='#ffffff',
            full_circle=True,
            command=self.submit_signup,
        )
        self.signup.pack(side="top", pady=2)
        self.signup._ctkmaker_min = 32
        self.signup._ctkmaker_fixed = True

        self.signin = ctk.CTkFrame(
            self.main_cont_v,
            width=240,
            height=180,
            corner_radius=6,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.signin.pack(side="top", fill="both", expand=True, pady=2)
        self.signin._ctkmaker_min = 20

        self.signin.pack_propagate(False)
        self.signin.grid_propagate(False)

        self.label_signin = ctk.CTkLabel(
            self.signin,
            width=365,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=0,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text='Already Have an Account?',
            font_wrap=True,
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
            font=ctk.CTkFont(size=30, weight="normal", slant="roman"),
        )
        self.label_signin.pack(side="top", pady=2)
        self.label_signin._ctkmaker_min = 16
        self.label_signin._ctkmaker_fixed = True

        self.button_signin = ctk.CTkButton(
            self.signin,
            width=185,
            height=52,
            corner_radius=6,
            border_width=0,
            border_color='#efefef',
            text='Sign In',
            text_color='#ffffff',
            full_circle=True,
            font=ctk.CTkFont(size=30, weight="normal", slant="roman"),
            command=self.request_signin
        )
        self.button_signin.pack(side="top", pady=2)
        self.button_signin._ctkmaker_min = 32
        self.button_signin._ctkmaker_fixed = True

        self.signin.bind("<Configure>", lambda _e, _c=self.signin: ctk.balance_pack(_c, 'height'))

        self.main_cont_v.bind("<Configure>", lambda _e, _c=self.main_cont_v: ctk.balance_pack(_c, 'height'))

    def _close_dialog(self):
        self.username_data = None
        self.password_data = None
        self.confirm_password_data = None
        self.remember_username_data = None
        self.destroy()

    def request_signin(self):
        self.request_signin_flag = True
        self.destroy()

    def _toggle_password(self):
        current = self.field_password.cget("show")
        new_show = "" if current == "•" else "•"
        self.field_password.configure(show=new_show)
        self.show_hide_password.configure(
            image=self.eye_off_img if new_show == "" else self.eye_img,
            text="Hide Password" if new_show == "" else "Show Password",
        )

    def _toggle_confirm_password(self):
        current = self.field_confirm_password.cget("show")
        new_show = "" if current == "•" else "•"
        self.field_confirm_password.configure(show=new_show)
        self.button_show_confirm_password.configure(
            image=self.eye_off_img if new_show == "" else self.eye_img,
            text="Hide Password" if new_show == "" else "Show Password",
        )

    def submit_signup(self):
        username = self.field_username.get().strip()
        password = self.field_password.get()
        confirm_password = self.field_confirm_password.get()

        if not username or not password or not confirm_password:
            show_toast(self, "Please fill out all sign-up fields.", type="error")
            return

        if password != confirm_password:
            show_toast(self, "Error! Passwords don't match!", type="error")
            print("Error! Passwords don't match!")
            return

        self.username_data = username
        self.password_data = password
        self.confirm_password_data = confirm_password
        self.remember_username_data = self.remember_username.get()

        if callable(self.on_submit):
            if self.on_submit(username, password, confirm_password, self.remember_username_data):
                self.destroy()
                return

        self.field_password.delete(0, "end")
        self.field_confirm_password.delete(0, "end")
        self.field_username.focus_set()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    app = Signup(root)
    root.mainloop()
