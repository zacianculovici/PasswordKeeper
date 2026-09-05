import time
import customtkinter as ctk
from PIL import Image
from helperFiles.scrollable_dropdown import ScrollableDropdown
from pathlib import Path
from helperFiles.toast import show_toast
from helperFiles.center_window_on_screen import center_window_on_screen
from helperFiles.localDataManager import rememberUsername
from helperFiles.objects import DangerousButton
from helperFiles.customDialog import CustomButtonDialog
from helperFiles.paths import resource_path

class Account(ctk.CTkToplevel):
    def __init__(self, parent=None, current_user=None, theme_names=None, current_theme=None):
        super().__init__(parent)
        ctk.register_project_fonts(self, Path(__file__).resolve().parent / "assets" / "fonts")
        self.title("Account Settings")
        self.geometry("660x400")
        self.minsize(400, 300)
        self.grab_set()
        time.sleep(0.1)  # Allow the window to be created before centering
        center_window_on_screen(self, 660, 400)
        self.after(250, lambda: self.iconbitmap(str(resource_path("assets", "icons", "user-round-cog.ico"))))

        # ===== Initialize variables ======
        self.current_user = current_user
        self.theme_names = theme_names
        self.current_theme = current_theme
        self.parent = parent

        # ====== Build UI ======
        self._build_ui()

    def _build_ui(self):
        # Preload images so they are not garbage-collected
        self.img_log_out = ctk.CTkImage(light_image=Image.open(resource_path('assets', 'images', 'log-out.png')), dark_image=Image.open(resource_path('assets', 'images', 'log-out.png')), size=(20, 20))
        self.img_trash_2 = ctk.CTkImage(light_image=Image.open(resource_path('assets', 'images', 'trash-2.png')), dark_image=Image.open(resource_path('assets', 'images', 'trash-2.png')), size=(20, 20))
        self.img_eye = ctk.CTkImage(light_image=Image.open(resource_path('assets', 'images', 'eye.png')), dark_image=Image.open(resource_path('assets', 'images', 'eye.png')), size=(20, 20))
        self.img_eye_off = ctk.CTkImage(light_image=Image.open(resource_path('assets', 'images', 'eye-off.png')), dark_image=Image.open(resource_path('assets', 'images', 'eye-off.png')), size=(20, 20))

        self.body_1 = ctk.CTkFrame(
            self,
            width=660,
            height=400,
            corner_radius=6,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.body_1.place(relwidth=1.0, relheight=1.0, x=0, y=0)

        self.body_1.pack_propagate(False)
        self.body_1.grid_propagate(False)

        self.header_1 = ctk.CTkFrame(
            self.body_1,
            width=800,
            height=50,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='#000000',
        )
        self.header_1.pack(side="top", fill="x")
        self.header_1._ctkmaker_min = 20
        self.header_1._ctkmaker_fixed = True

        self.header_1.pack_propagate(False)
        self.header_1.grid_propagate(False)

        self.title_1 = ctk.CTkLabel(
            self.header_1,
            width=100,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=10,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text='Account Settings',
            font_wrap=True,
            anchor='w',
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
            font=ctk.CTkFont(size=20, weight="bold", slant="roman"),
        )
        self.title_1.pack(side="left", fill="both", expand=True)
        self.title_1._ctkmaker_min = 233

        self.log_out_button_1 = ctk.CTkButton(
            self.header_1,
            width=90,
            height=50,
            corner_radius=0,
            border_width=0,
            border_color='#efefef',
            border_spacing=0,
            text='Logout',
            text_color='#ffffff',
            full_circle=True,
            image=self.img_log_out,
            command=lambda: self.parent.logout(),
        )
        self.log_out_button_1.pack(side="left")
        self.log_out_button_1._ctkmaker_min = 91
        self.log_out_button_1._ctkmaker_fixed = True

        self.header_1.bind("<Configure>", lambda _e, _c=self.header_1: ctk.balance_pack(_c, 'width'))

        self.main_1 = ctk.CTkFrame(
            self.body_1,
            width=320,
            height=60,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='#2b2b2b',
        )
        self.main_1.pack(side="top", fill="both", expand=True)
        self.main_1._ctkmaker_min = 20

        self.main_1.pack_propagate(False)
        self.main_1.grid_propagate(False)

        # Add a frame with a horizontal layout for the user label and the "Signed in as:" text

        self.user_1 = ctk.CTkFrame(
            self.main_1,
            width=300,
            height=40,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.user_1.pack(side="top", fill="x", pady=2)
        self.user_1._ctkmaker_min = 20
        self.user_1.bind("<Configure>", lambda _e, _c=self.user_1: ctk.balance_pack(_c, 'width'))

        self.label_user_1 = ctk.CTkLabel(
            self.user_1,
            width=100,
            height=40,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=0,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text=f'Signed in as:',
            font_wrap=True,
            justify='right',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
        )
        self.label_user_1.pack(side="left", pady=2)
        self.label_user_1._ctkmaker_min = 16
        self.label_user_1._ctkmaker_fixed = True

        self.entry_user_1 = ctk.CTkEntry(
            self.user_1,
            width=100,
            height=40,
            border_color='#565b5e',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
        )
        self.entry_user_1.pack(side="left", fill="x", pady=2)
        self.entry_user_1._ctkmaker_min = 16

        self.entry_user_1.insert(0, self.current_user)

        self.button_save_username_1 = ctk.CTkButton(
            self.user_1,
            width=100,
            height=40,
            text="Save",
            command=lambda: self.parent.save_username(self.entry_user_1.get().strip(), self.checkbox_remember_1.get())
        )
        self.button_save_username_1.pack(side="left", padx=5, pady=2)
        self.button_save_username_1._ctkmaker_min = 16
        self.button_save_username_1._ctkmaker_fixed = True

        self.separator_rect_1 = ctk.CTkFrame(
            self.main_1,
            width=780,
            height=2,
            corner_radius=1,
            border_width=0,
            border_color='#565b5e',
            fg_color='#4e4e4e',
        )
        self.separator_rect_1.pack(side="top", fill="x", pady=2, padx=5)
        self.separator_rect_1._ctkmaker_min = 20
        self.separator_rect_1._ctkmaker_fixed = True

        self.checkbox_remember_1 = ctk.CTkCheckBox(
            self.main_1,
            width=20,
            height=10,
            corner_radius=6,
            border_width=3,
            border_color='#949A9F',
            checkmark_color='#e5e5e5',
            text='Remember my username',
            text_color='#dce4ee',
            text_color_disabled='#737373',
            command=lambda: (rememberUsername(self.current_user if self.checkbox_remember_1.get() else None))
        )
        self.checkbox_remember_1.pack(side="top", pady=2)
        self.checkbox_remember_1._ctkmaker_min = 28
        self.checkbox_remember_1._ctkmaker_fixed = True
        self.checkbox_remember_1.set(bool(rememberUsername() == self.current_user))

        self.checkbox_start_maximized_1 = ctk.CTkCheckBox(
            self.main_1,
            width=20,
            height=10,
            corner_radius=6,
            border_width=3,
            border_color='#949A9F',
            checkmark_color='#e5e5e5',
            text='Start maximized',
            text_color='#dce4ee',
            text_color_disabled='#737373',
            command=lambda: (self.parent.data_manager.start_maximised(bool(self.checkbox_start_maximized_1.get())))
        )
        self.checkbox_start_maximized_1.pack(side="top", pady=2)
        self.checkbox_start_maximized_1._ctkmaker_min = 28
        self.checkbox_start_maximized_1._ctkmaker_fixed = True

        self.theme_dropdown_1 = ctk.CTkFrame(
            self.main_1,
            width=500,
            height=40,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.theme_dropdown_1.pack(side="top", pady=2)
        self.theme_dropdown_1._ctkmaker_min = 20
        self.theme_dropdown_1._ctkmaker_fixed = True

        self.theme_dropdown_1.pack_propagate(False)
        self.theme_dropdown_1.grid_propagate(False)

        self.label_theme_dropdown_1 = ctk.CTkLabel(
            self.theme_dropdown_1,
            width=100,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=10,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text='Theme',
            font_wrap=True,
            anchor='w',
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
        )
        self.label_theme_dropdown_1.pack(side="left", padx=2)
        self.label_theme_dropdown_1._ctkmaker_min = 57
        self.label_theme_dropdown_1._ctkmaker_fixed = True

        self.optionmenu_theme_dropdown_1 = ctk.CTkOptionMenu(
            self.theme_dropdown_1,
            corner_radius=6,
            values=[theme.capitalize() for theme in self.theme_names],
            command=lambda value: (self._change_color_theme(self.parent, value), show_toast(self, f"Theme changed to {value}")),
            fg_color='#565b5e',
            button_color='#2f3133',
            button_hover_color='#203a4f',
            dropdown_fg_color='#2b2b2b',
            dropdown_hover_color='#3a3a3a',
            dropdown_text_color='#dce4ee',
            text_color='#dce4ee',
            text_color_disabled='#737373',
            dynamic_resizing=False,
        )
        self.optionmenu_theme_dropdown_1.pack(side="left", fill="x", padx=5, pady=5)
        self.optionmenu_theme_dropdown_1._ctkmaker_min = 60
        self.optionmenu_theme_dropdown_1.set(self.current_theme.capitalize() if self.current_theme else "blue".capitalize())
        self.optionmenu_theme_dropdown_1._scrollable_dropdown = ScrollableDropdown(
            self.optionmenu_theme_dropdown_1,
            font=self.optionmenu_theme_dropdown_1.cget("font"),
            fg_color='#2b2b2b',
            text_color='#dce4ee',
            hover_color='#3a3a3a',
            offset=4,
            button_align='center',
            max_visible=8,
            border_width=1,
            border_color='#3c3c3c',
            corner_radius=6,
        )

        self.theme_dropdown_1.bind("<Configure>", lambda _e, _c=self.theme_dropdown_1: ctk.balance_pack(_c, 'width'))

        # Cloud storage is not available yet
        # self.card_connection_token_1 = ctk.CTkFrame(
        #     self.main_1,
        #     width=500,
        #     height=28,
        #     corner_radius=0,
        #     border_width=0,
        #     fg_color='transparent',
        # )
        # self.card_connection_token_1.pack(side="top", pady=2)
        # self.card_connection_token_1._ctkmaker_min = 20
        # self.card_connection_token_1._ctkmaker_fixed = True

        # self.card_connection_token_1.pack_propagate(False)
        # self.card_connection_token_1.grid_propagate(False)

        # self.label_connection_token_1 = ctk.CTkLabel(
        #     self.card_connection_token_1,
        #     width=200,
        #     corner_radius=0,
        #     border_width=0,
        #     border_color='#565b5e',
        #     padx=10,
        #     pady=0,
        #     cursor='',
        #     takefocus=False,
        #     fg_color='transparent',
        #     text='Connection token',
        #     font_wrap=True,
        #     anchor='w',
        #     justify='center',
        #     text_color='#ffffff',
        #     text_color_disabled='#a0a0a0',
        #     compound='left',
        #     full_circle=True,
        #     unified_bind=True,
        # )
        # self.label_connection_token_1.pack(side="left", padx=2)
        # self.label_connection_token_1._ctkmaker_min = 135
        # self.label_connection_token_1._ctkmaker_fixed = True

        # self.field_connection_token_1 = ctk.CTkEntry(
        #     self.card_connection_token_1,
        #     width=400,
        #     corner_radius=6,
        #     border_width=2,
        #     border_color='#565b5e',
        #     placeholder_text='Enter connection token...',
        #     fg_color='#343638',
        #     text_color='#dce4ee',
        #     placeholder_text_color='#9ea0a2',
        #     justify='left',
        # )
        # self.field_connection_token_1.pack(side="left", fill="both", expand=True, padx=2)
        # self.field_connection_token_1._ctkmaker_min = 50

        # self.card_connection_token_1.bind("<Configure>", lambda _e, _c=self.card_connection_token_1: ctk.balance_pack(_c, 'width'))

        self.separator_rect_2 = ctk.CTkFrame(
            self.main_1,
            width=780,
            height=2,
            corner_radius=1,
            border_width=0,
            border_color='#565b5e',
            fg_color='#4e4e4e',
        )
        self.separator_rect_2.pack(side="top", fill="x", pady=2, padx=5)
        self.separator_rect_2._ctkmaker_min = 20
        self.separator_rect_2._ctkmaker_fixed = True

        self.change_password_1 = ctk.CTkFrame(
            self.main_1,
            width=500,
            height=28,
            corner_radius=0,
            border_width=0,
            fg_color='transparent',
        )
        self.change_password_1.pack(side="top", pady=2)
        self.change_password_1._ctkmaker_min = 20
        self.change_password_1._ctkmaker_fixed = True

        self.label_change_password_1 = ctk.CTkLabel(
            self.change_password_1,
            width=200,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=0,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text='Change Password',
            font_wrap=True,
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
            anchor='w',
        )
        self.label_change_password_1.pack(side="left", padx=2)
        self.label_change_password_1._ctkmaker_min = 135
        self.label_change_password_1._ctkmaker_fixed = True

        self.field_change_password_1 = ctk.CTkEntry(
            self.change_password_1,
            width=300,
            corner_radius=6,
            border_width=2,
            border_color='#565b5e',
            placeholder_text='Enter new password...',
            fg_color='#343638',
            text_color='#dce4ee',
            placeholder_text_color='#9ea0a2',
            justify='left',
            show='•'
        )
        self.field_change_password_1.pack(side="left", fill="both", expand=True, padx=2)
        self.field_change_password_1._ctkmaker_min = 50

        self.show_hide_password_button_1 = ctk.CTkButton(
            self.change_password_1,
            width=30,
            height=30,
            text='',
            image=self.img_eye,
            command=self._toggle_password_visibility
        )
        self.show_hide_password_button_1.pack(side="right", padx=2)
        self.show_hide_password_button_1._ctkmaker_min = 30
        self.show_hide_password_button_1._ctkmaker_fixed = True

        self.change_password_confirm_1 = ctk.CTkFrame(
            self.main_1,
            width=500,
            height=28,
            corner_radius=0,
            border_width=0,
            fg_color='transparent',
        )
        self.change_password_confirm_1.pack(side="top", pady=2)
        self.change_password_confirm_1._ctkmaker_min = 20
        self.change_password_confirm_1._ctkmaker_fixed = True

        self.label_change_password_confirm_1 = ctk.CTkLabel(
            self.change_password_confirm_1,
            width=200,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=0,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text='Confirm Password',
            font_wrap=True,
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
            anchor='w',
        )
        self.label_change_password_confirm_1.pack(side="left", padx=2)
        self.label_change_password_confirm_1._ctkmaker_min = 135
        self.label_change_password_confirm_1._ctkmaker_fixed = True

        self.field_change_password_confirm_1 = ctk.CTkEntry(
            self.change_password_confirm_1,
            width=300,
            corner_radius=6,
            border_width=2,
            border_color='#565b5e',
            placeholder_text='Confirm new password...',
            fg_color='#343638',
            text_color='#dce4ee',
            placeholder_text_color='#9ea0a2',
            justify='left',
            show='•'
        )
        self.field_change_password_confirm_1.pack(side="left", fill="both", expand=True, padx=2)
        self.field_change_password_confirm_1._ctkmaker_min = 50

        self.show_hide_confirm_password_button_1 = ctk.CTkButton(
            self.change_password_confirm_1,
            width=30,
            height=30,
            text='',
            image=self.img_eye,
            command=self._toggle_confirm_password_visibility
        )
        self.show_hide_confirm_password_button_1.pack(side="right", padx=2)
        self.show_hide_confirm_password_button_1._ctkmaker_min = 30
        self.show_hide_confirm_password_button_1._ctkmaker_fixed = True

        self.button_change_password_1 = ctk.CTkButton(
            self.main_1,
            width=200,
            height=32,
            text='Change Password',
            full_circle=True,
            command=self.change_password
        )
        self.button_change_password_1.pack(side="top", pady=2)
        self.button_change_password_1._ctkmaker_min = 32
        self.button_change_password_1._ctkmaker_fixed = True

        self.separator_rect_3 = ctk.CTkFrame(
            self.main_1,
            width=780,
            height=2,
            corner_radius=1,
            border_width=0,
            border_color='#565b5e',
            fg_color='#4e4e4e',
        )
        self.separator_rect_3.pack(side="top", fill="x", pady=2, padx=5)
        self.separator_rect_3._ctkmaker_min = 20
        self.separator_rect_3._ctkmaker_fixed = True

        self.button_permanently_delete_1 = DangerousButton(
            self.main_1,
            width=200,
            height=32,
            text='Permanently Delete Account',
            full_circle=True,
            image=self.img_trash_2,
            command=self.permanently_delete_account
        )
        self.button_permanently_delete_1.pack(side="top", pady=2)
        self.button_permanently_delete_1._ctkmaker_min = 32
        self.button_permanently_delete_1._ctkmaker_fixed = True

        self.main_1.bind("<Configure>", lambda _e, _c=self.main_1: ctk.balance_pack(_c, 'height'))

        self.body_1.bind("<Configure>", lambda _e, _c=self.body_1: ctk.balance_pack(_c, 'height'))

        maximize = self.parent.data_manager.start_maximised()
        print(f"Setting 'Start maximized' checkbox for user '{self.parent.current_user}' to: {maximize}")
        self.checkbox_start_maximized_1.set(bool(maximize))

    def _change_color_theme(self, parent, new_theme):
        print(f"Changing color theme to: {new_theme}")
        for widget in self.winfo_children():
            if not isinstance(widget, ctk.CTkToplevel):
                widget.destroy()
            else:
                print(f"Skipping destruction of Toplevel widget with name: '{widget.winfo_name()}'")
        for widget in parent.winfo_children():
            if not isinstance(widget, ctk.CTkToplevel):
                widget.destroy()
            else:
                print(f"Skipping destruction of Toplevel widget with name: '{widget.winfo_name()}'")
        ctk.set_default_color_theme(str(resource_path("assets", "themes", new_theme.lower() + ".json")))
        parent.current_theme = new_theme.lower()
        self.current_theme = new_theme.lower()
        parent.data_manager.theme(new_theme.lower())
        self._build_ui()
        parent._build_ui()

    def permanently_delete_account(self):
        answer = CustomButtonDialog(self, "Are you sure you want to permanently delete your account?", "This action cannot be undone.", {"Yes": "#E01E1E", "No": "#2A2A2A"}, icon_path=str(resource_path('assets', 'icons', 'circle-alert.ico'))).result.lower()
        if answer == "yes":
            self.parent.delete_account()
        else:
            self.grab_set()  # Re-grab focus to the dialog if the user cancels the deletion

    def change_password(self):
        new_password = self.field_change_password_1.get()
        confirm_password = self.field_change_password_confirm_1.get()

        if new_password != confirm_password:
            show_toast(self, "Passwords do not match.", "error")
            return

        if not new_password:
            show_toast(self, "Password cannot be empty.", "error")
            return

        self.parent.data_manager.change_password(new_password)
        show_toast(self, "Password changed successfully.", "success")

    def _toggle_password_visibility(self):
        if self.field_change_password_1.cget("show") == "":
            self.field_change_password_1.configure(show='•')
            self.show_hide_password_button_1.configure(image=self.img_eye)
        else:
            self.field_change_password_1.configure(show="")
            self.show_hide_password_button_1.configure(image=self.img_eye_off)

    def _toggle_confirm_password_visibility(self):
        if self.field_change_password_confirm_1.cget("show") == "":
            self.field_change_password_confirm_1.configure(show='•')
            self.show_hide_confirm_password_button_1.configure(image=self.img_eye)
        else:
            self.field_change_password_confirm_1.configure(show="")
            self.show_hide_confirm_password_button_1.configure(image=self.img_eye_off)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = Account()
    app.mainloop()
