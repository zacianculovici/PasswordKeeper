import customtkinter as ctk
from PIL import Image
import account
from helperFiles.dataManager import DataManager
from helperFiles.objects import User, NoAccountError
from helperFiles.secureFileManager import SecureDataManager
from helperFiles.scrollable_dropdown import ScrollableDropdown
from helperFiles.toast import show_toast
import login
import signup
import tkinter as tk
from pathlib import Path
import helperFiles.loadingPleaseWait as loadingPleaseWait
from helperFiles.customDialog import CustomButtonDialog
import webbrowser
import builtins
import datetime
from helperFiles.localDataManager import *
import traceback
from helperFiles.objects import DangerousButton

global original_print
original_print = builtins.print
def custom_print(*args, **kwargs):
    original_print(f"DEBUG@{datetime.datetime.now()}:", *args, **kwargs)

builtins.print = custom_print

print(f"========= Password Keeper: Running from: \"{__file__}\" =========")

global debug_mode, show_loading_window, theme_names, orig_pack, orig_grid, orig_place
debug_mode = "off"  # Set to minimal, medium, verbose, or off for different levels of debug output. Minimal will print only essential information, medium will print more detailed information, verbose will print everything, and off will disable debug output entirely.
show_loading_window = False  # Set to True to show the loading window, or False to disable it.

# Get names without extensions for all files in the assets/themes folder
theme_names = [f.stem for f in Path("assets/themes").iterdir() if f.is_file()]

# Save original geometry manager methods
orig_pack = ctk.CTkBaseClass.pack
orig_grid = ctk.CTkBaseClass.grid
orig_place = ctk.CTkBaseClass.place

def on_widget_added(widget, loading_window):
    loading_window.update_progress()
    widget.master.update()  # Ensure the parent window updates immediately

# Override pack
def custom_pack(self, loading_window=None, *args, **kwargs):
    orig_pack(self, *args, **kwargs)
    on_widget_added(self, loading_window)

# Override grid
def custom_grid(self, loading_window=None, *args, **kwargs):
    orig_grid(self, *args, **kwargs)
    on_widget_added(self, loading_window)

# Override place
def custom_place(self, loading_window=None, *args, **kwargs):
    orig_place(self, *args, **kwargs)
    on_widget_added(self, loading_window)

# Helper to reset geometry managers to their original methods
def reset_geometry_managers():
    ctk.CTkBaseClass.grid = orig_grid
    ctk.CTkBaseClass.pack = orig_pack
    ctk.CTkBaseClass.place = orig_place

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Password Keeper")
        self.geometry("800x600")
        self.minsize(width=700, height=300)

        # ====== Initialize variables ======
        self.signedin = False
        self.signin_or_signup = None

        self.current_user = None

        self.selected_category = "All"
        self.selected_password = ""

        self.category_buttons = []
        self.password_buttons = []

        self.current_main_frame = "none"  # Track the current main frame: "password", "category", or "none"

        self.all_category = True

        # ====== Build the UI ======
        self.requestAccount()
        if not getattr(self, "data_manager", None):
            print("Data manager not initialized. Exiting application.")
            self.destroy()
        self.current_theme = self.data_manager.user_data.get("theme", "blue")
        ctk.set_default_color_theme("assets/themes/" + self.current_theme + ".json")  # Set default theme based on user preference
        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _build_ui(self):
        # Preload images so they are not garbage-collected
        self.img_brain_cog = ctk.CTkImage(light_image=Image.open('assets/images/brain-cog.png'), dark_image=Image.open('assets/images/brain-cog.png'), size=(20, 20))
        self.img_user_round_cog = ctk.CTkImage(light_image=Image.open('assets/images/user-round-cog.png'), dark_image=Image.open('assets/images/user-round-cog.png'), size=(20, 20))
        self.img_plus = ctk.CTkImage(light_image=Image.open('assets/images/plus.png'), dark_image=Image.open('assets/images/plus.png'), size=(20, 20))
        self.img_trash_2 = ctk.CTkImage(light_image=Image.open('assets/images/trash-2.png'), dark_image=Image.open('assets/images/trash-2.png'), size=(20, 20))
        self.img_x = ctk.CTkImage(light_image=Image.open('assets/images/x.png'), dark_image=Image.open('assets/images/x.png'), size=(20, 20))
        self.img_eye = ctk.CTkImage(light_image=Image.open('assets/images/eye.png'), dark_image=Image.open('assets/images/eye.png'), size=(20, 20))
        self.img_eye_off = ctk.CTkImage(light_image=Image.open('assets/images/eye-off.png'), dark_image=Image.open('assets/images/eye-off.png'), size=(20, 20))
        self.img_copy = ctk.CTkImage(light_image=Image.open('assets/images/copy.png'), dark_image=Image.open('assets/images/copy.png'), size=(20, 20))
        self.img_check = ctk.CTkImage(light_image=Image.open('assets/images/check.png'), dark_image=Image.open('assets/images/check.png'), size=(20, 20))

        if show_loading_window:
            self.loadtk = loadingPleaseWait.LoadingWindow(self, text="Loading theme: <X%>\nplease wait...\n", total_amount=75, delay=0, debug=debug_mode)
            ctk.CTkBaseClass.grid = lambda myself, *args, **kwargs: custom_grid(myself, self.loadtk, *args, **kwargs)
            ctk.CTkBaseClass.pack = lambda myself, *args, **kwargs: custom_pack(myself, self.loadtk, *args, **kwargs)
            ctk.CTkBaseClass.place = lambda myself, *args, **kwargs: custom_place(myself, self.loadtk, *args, **kwargs)

        self.body_v_1 = ctk.CTkFrame(
            self,
            width=800,
            height=600,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.body_v_1.place(relwidth=1.0, relheight=1.0, x=0, y=0)

        self.body_v_1.pack_propagate(False)
        self.body_v_1.grid_propagate(False)

        self.header_h_1 = ctk.CTkFrame(
            self.body_v_1,
            width=800,
            height=50,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='#000000',
        )
        self.header_h_1.pack(fill="x", side="top")
        self.header_h_1._ctkmaker_min = 20
        self.header_h_1._ctkmaker_fixed = True

        self.header_h_1.pack_propagate(False)
        self.header_h_1.grid_propagate(False)

        self.title_l_1 = ctk.CTkLabel(
            self.header_h_1,
            width=100,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=10,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text='Password Keeper',
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
        self.title_l_1.pack(side="left", fill="both", expand=True)
        self.title_l_1._ctkmaker_min = 238

        # self.theme_dropdown = ctk.CTkOptionMenu(
        #     self.header_h_1,
        #     values=[theme.capitalize() for theme in theme_names],
        #     fg_color='#565b5e',
        #     button_color='#2f3133',
        #     button_hover_color='#203a4f',
        #     dropdown_fg_color='#2b2b2b',
        #     dropdown_hover_color='#3a3a3a',
        #     dropdown_text_color='#dce4ee',
        #     text_color='#dce4ee',
        #     text_color_disabled='#737373',
        #     dynamic_resizing=False,
        # )
        # self.theme_dropdown.pack(side="left", padx=5, pady=5)
        # self.theme_dropdown._ctkmaker_min = 60
        # self.theme_dropdown._ctkmaker_fixed = True
        # self.theme_dropdown.set(self.current_theme.capitalize())  # Set the initial theme
        # self.theme_dropdown = ScrollableDropdown(
        #     self.header_h_1,
        #     font=self.theme_dropdown.cget("font"),
        #     fg_color='#2b2b2b',
        #     text_color='#dce4ee',
        #     hover_color='#3a3a3a',
        #     offset=4,
        #     button_align='center',
        #     max_visible=8,
        #     border_width=1,
        #     border_color='#3c3c3c',
        #     corner_radius=6,
        # )

        # TODO: Add functionality for generating passwords

        # self.gen_btn_1 = ctk.CTkButton(
        #     self.header_h_1,
        #     width=50,
        #     height=50,
        #     corner_radius=0,
        #     border_width=0,
        #     border_color='#efefef',
        #     border_spacing=0,
        #     text='',
        #     text_color='#ffffff',
        #     compound='right',
        #     full_circle=True,
        #     image=self.img_brain_cog,
        # )
        # self.gen_btn_1.pack(side="left")
        # self.gen_btn_1._ctkmaker_min = 36
        # self.gen_btn_1._ctkmaker_fixed = True

        self.account_btn_1 = ctk.CTkButton(
            self.header_h_1,
            width=50,
            height=50,
            corner_radius=0,
            border_width=0,
            border_color='#efefef',
            border_spacing=0,
            text='',
            text_color='#ffffff',
            compound='right',
            full_circle=True,
            image=self.img_user_round_cog,
            command=lambda: self.open_account_settings()
        )
        self.account_btn_1.pack(side="left")
        self.account_btn_1._ctkmaker_min = 36
        self.account_btn_1._ctkmaker_fixed = True

        self.header_h_1.bind("<Configure>", lambda _e, _c=self.header_h_1: ctk.balance_pack(_c, 'width'))

        self.main_h_1 = ctk.CTkFrame(
            self.body_v_1,
            width=320,
            height=60,
            corner_radius=6,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.main_h_1.pack(side="top", fill="both", expand=True)
        self.main_h_1._ctkmaker_min = 20

        self.main_h_1.pack_propagate(False)
        self.main_h_1.grid_propagate(False)

        self.categories_v_1 = ctk.CTkFrame(
            self.main_h_1,
            width=175,
            height=550,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='#000000',
        )
        self.categories_v_1.pack(fill="y", side="left")
        self.categories_v_1._ctkmaker_min = 20
        self.categories_v_1._ctkmaker_fixed = True

        self.categories_v_1.pack_propagate(False)
        self.categories_v_1.grid_propagate(False)

        self.search_categories_field = ctk.CTkEntry(
            self.categories_v_1,
            width=200,
            height=30,
            corner_radius=0,
            border_width=2,
            border_color='#565b5e',
            placeholder_text='Search Categories...',
            fg_color='#343638',
            text_color='#dce4ee',
            placeholder_text_color='#9ea0a2',
            justify='left',
        )
        self.search_categories_field.pack(side="top")
        self.search_categories_field._ctkmaker_min = 50
        self.search_categories_field._ctkmaker_fixed = True
        self.search_categories_field.bind("<KeyRelease>", lambda event: self.update_category_list())

        self.category_list_sf_1 = ctk.CTkScrollableFrame(
            self.categories_v_1,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            label_fg_color='#3a3a3a',
            label_text_color='#dce4ee',
            scrollbar_fg_color='transparent',
            scrollbar_button_color='#3a3a3a',
            scrollbar_button_hover_color='#4a4a4a',
            fg_color='#2b2b2b',
        )
        self.category_list_sf_1.pack(side="top", fill="both", expand=True)
        self.category_list_sf_1._ctkmaker_min = 40
        self.category_list_sf_1._parent_frame.configure(width=200, height=200)
        self.category_list_sf_1._parent_frame.grid_propagate(False)

        self.update_category_list()

        self.categories_v_1.bind("<Configure>", lambda _e, _c=self.categories_v_1: ctk.balance_pack(_c, 'height'))

        self.passwords_v_1 = ctk.CTkFrame(
            self.main_h_1,
            width=175,
            height=550,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='#000000',
        )
        self.passwords_v_1.pack(fill="y", side="left")
        self.passwords_v_1._ctkmaker_min = 20
        self.passwords_v_1._ctkmaker_fixed = True

        self.passwords_v_1.pack_propagate(False)
        self.passwords_v_1.grid_propagate(False)

        self.search_passwords_field = ctk.CTkEntry(
            self.passwords_v_1,
            width=200,
            height=30,
            corner_radius=0,
            border_width=2,
            border_color='#565b5e',
            placeholder_text='Search Passwords...',
            fg_color='#343638',
            text_color='#dce4ee',
            placeholder_text_color='#9ea0a2',
            justify='left',
        )
        self.search_passwords_field.pack(side="top")
        self.search_passwords_field._ctkmaker_min = 50
        self.search_passwords_field._ctkmaker_fixed = True
        self.search_passwords_field.bind("<KeyRelease>", lambda event: self.update_password_list())

        self.password_list_sf_1 = ctk.CTkScrollableFrame(
            self.passwords_v_1,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            label_fg_color='#3a3a3a',
            label_text_color='#dce4ee',
            scrollbar_fg_color='transparent',
            scrollbar_button_color='#3a3a3a',
            scrollbar_button_hover_color='#4a4a4a',
            fg_color='#2b2b2b',
        )
        self.password_list_sf_1.pack(side="top", fill="both", expand=True)
        self.password_list_sf_1._ctkmaker_min = 40
        self.password_list_sf_1._parent_frame.configure(width=200, height=200)
        self.password_list_sf_1._parent_frame.grid_propagate(False)

        self.update_password_list("All")

        self.passwords_v_1.bind("<Configure>", lambda _e, _c=self.passwords_v_1: ctk.balance_pack(_c, 'height'))

        self.main_frame_container = ctk.CTkFrame(
            self.main_h_1,
            width=320,
            height=240,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.main_frame_container.pack(side="left", fill="both", expand=True)
        self.main_frame_container._ctkmaker_min = 20

        self.main_frame_container.pack_propagate(False)
        self.main_frame_container.grid_propagate(False)
        self.main_frame_container.grid_rowconfigure(0, weight=1)
        self.main_frame_container.grid_columnconfigure(0, weight=1)

        self.main_frame_pass = ctk.CTkFrame(
            self.main_frame_container,
            width=321,
            height=330,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.main_frame_pass.grid(row=0, column=0, sticky="nsew")

        self.main_frame_pass.pack_propagate(False)
        self.main_frame_pass.grid_propagate(False)

        self.header_pass = ctk.CTkFrame(
            self.main_frame_pass,
            width=450,
            height=50,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='#2b2b2b',
        )
        self.header_pass.pack(fill="x", side="top")
        self.header_pass._ctkmaker_min = 20
        self.header_pass._ctkmaker_fixed = True

        self.header_pass.pack_propagate(False)
        self.header_pass.grid_propagate(False)

        self.password_name_field = ctk.CTkEntry(
            self.header_pass,
            corner_radius=0,
            border_width=2,
            border_color='#565b5e',
            placeholder_text='Enter Password Name...',
            fg_color='#343638',
            text_color='#dce4ee',
            placeholder_text_color='#9ea0a2',
            justify='left',
        )
        self.password_name_field.pack(side="left", fill="both", expand=True)
        self.password_name_field._ctkmaker_min = 50

        self.delete_password_button = DangerousButton(
            self.header_pass,
            width=80,
            height=50,
            text='Delete!',
            full_circle=True,
            image=self.img_trash_2,
            command=self.delete_password
        )
        self.delete_password_button.pack(side="left", padx=5, pady=5)
        self.delete_password_button._ctkmaker_min = 93
        self.delete_password_button._ctkmaker_fixed = True

        self.btn_close_pass = ctk.CTkButton(
            self.header_pass,
            width=80,
            height=50,
            corner_radius=6,
            border_width=0,
            border_color='#efefef',
            compound='right',
            text='Close',
            text_color='#ffffff',
            full_circle=True,
            fg_color='#565b5e',
            pressed_color="#929394",
            image=self.img_x,
        )
        self.btn_close_pass.pack(side="left", padx=5, pady=5)
        self.btn_close_pass._ctkmaker_min = 93
        self.btn_close_pass._ctkmaker_fixed = True

        self.header_pass.bind("<Configure>", lambda _e, _c=self.header_pass: ctk.balance_pack(_c, 'width'))

        self.password_edit_form = ctk.CTkScrollableFrame(
            self.main_frame_pass,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            label_fg_color='#3a3a3a',
            label_text_color='#dce4ee',
            scrollbar_fg_color='transparent',
            scrollbar_button_color='#3a3a3a',
            scrollbar_button_hover_color='#4a4a4a',
            fg_color='#2b2b2b',
        )
        self.password_edit_form.pack(side="top", fill="both", expand=True)
        self.password_edit_form._ctkmaker_min = 40
        self.password_edit_form._parent_frame.configure(width=200, height=200)
        self.password_edit_form._parent_frame.grid_propagate(False)

        self.description_password = ctk.CTkFrame(
            self.password_edit_form,
            width=400,
            height=40,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.description_password.pack(fill="x", side="top", pady=2)
        self.description_password._ctkmaker_min = 20
        self.description_password._ctkmaker_fixed = True

        self.description_password.pack_propagate(False)
        self.description_password.grid_propagate(False)

        self.label_desc_pass = ctk.CTkLabel(
            self.description_password,
            width=100,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=10,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text='Description',
            font_wrap=True,
            anchor='w',
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
        )
        self.label_desc_pass.pack(side="left", padx=2)
        self.label_desc_pass._ctkmaker_min = 91
        self.label_desc_pass._ctkmaker_fixed = True

        self.field_desc_pass = ctk.CTkEntry(
            self.description_password,
            corner_radius=6,
            border_width=2,
            border_color='#565b5e',
            placeholder_text='Enter description…',
            fg_color='#343638',
            text_color='#dce4ee',
            placeholder_text_color='#9ea0a2',
            justify='left',
        )
        self.field_desc_pass.pack(side="left", fill="both", expand=True, padx=2)
        self.field_desc_pass._ctkmaker_min = 50

        self.description_password.bind("<Configure>", lambda _e, _c=self.description_password: ctk.balance_pack(_c, 'width'))

        self.username = ctk.CTkFrame(
            self.password_edit_form,
            width=400,
            height=40,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.username.pack(fill="x", side="top", pady=2)
        self.username._ctkmaker_min = 20
        self.username._ctkmaker_fixed = True

        self.username.pack_propagate(False)
        self.username.grid_propagate(False)

        self.label_user = ctk.CTkLabel(
            self.username,
            width=100,
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
        )
        self.label_user.pack(side="left", padx=2)
        self.label_user._ctkmaker_min = 82
        self.label_user._ctkmaker_fixed = True

        self.field_user = ctk.CTkEntry(
            self.username,
            corner_radius=6,
            border_width=2,
            border_color='#565b5e',
            placeholder_text='Enter username…',
            fg_color='#343638',
            text_color='#dce4ee',
            placeholder_text_color='#9ea0a2',
            justify='left',
        )
        self.field_user.pack(side="left", fill="both", expand=True, padx=2)
        self.field_user._ctkmaker_min = 50

        self.username.bind("<Configure>", lambda _e, _c=self.username: ctk.balance_pack(_c, 'width'))

        self.password = ctk.CTkFrame(
            self.password_edit_form,
            width=400,
            height=40,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.password.pack(fill="x", side="top", pady=2)
        self.password._ctkmaker_min = 20
        self.password._ctkmaker_fixed = True

        self.password.pack_propagate(False)
        self.password.grid_propagate(False)

        self.label_pass = ctk.CTkLabel(
            self.password,
            width=100,
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
        )
        self.label_pass.pack(side="left", padx=2)
        self.label_pass._ctkmaker_min = 79
        self.label_pass._ctkmaker_fixed = True

        self.field_password = ctk.CTkEntry(
            self.password,
            corner_radius=6,
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

        self.copy_password_button = ctk.CTkButton(
            self.password,
            width=150,
            height=40,
            corner_radius=6,
            border_width=0,
            border_color='#efefef',
            text='Copy Password',
            text_color='#ffffff',
            full_circle=True,
            fg_color='transparent',
            pressed_color='#2b2b2b',
            image=self.img_copy,
            command=self.copy_password_to_clipboard,
        )
        self.copy_password_button.pack(side="left", padx=2)
        self.copy_password_button._ctkmaker_min = 40
        self.copy_password_button._ctkmaker_fixed = True

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
            image=self.img_eye,
            command=self._toggle_password,
        )
        self.show_hide_password.pack(side="left", padx=2)
        self.show_hide_password._ctkmaker_min = 40
        self.show_hide_password._ctkmaker_fixed = True

        self.password.bind("<Configure>", lambda _e, _c=self.password: ctk.balance_pack(_c, 'width'))

        # TODO: Add functionality for generating passwords

        # self.generate = ctk.CTkFrame(
        #     self.password_edit_form,
        #     width=400,
        #     height=40,
        #     corner_radius=0,
        #     border_width=0,
        #     border_color='#565b5e',
        #     fg_color='transparent',
        # )
        # self.generate.pack(fill="x", side="top", pady=2)
        # self.generate._ctkmaker_min = 20
        # self.generate._ctkmaker_fixed = True

        # self.generate.pack_propagate(False)
        # self.generate.grid_propagate(False)

        # self.generate_button_edit_pass = ctk.CTkButton(
        #     self.generate,
        #     height=32,
        #     corner_radius=6,
        #     border_width=0,
        #     border_color='#efefef',
        #     text='Generate Password',
        #     text_color='#ffffff',
        #     full_circle=True,
        # )
        # self.generate_button_edit_pass.pack(side="left", fill="both", expand=True, padx=2)
        # self.generate_button_edit_pass._ctkmaker_min = 159

        # self.generate.bind("<Configure>", lambda _e, _c=self.generate: ctk.balance_pack(_c, 'width'))

        self.category = ctk.CTkFrame(
            self.password_edit_form,
            width=400,
            height=40,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.category.pack(fill="x", side="top", pady=2)
        self.category._ctkmaker_min = 20
        self.category._ctkmaker_fixed = True

        self.category.pack_propagate(False)
        self.category.grid_propagate(False)

        self.label_category = ctk.CTkLabel(
            self.category,
            width=100,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=10,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text='Category',
            font_wrap=True,
            anchor='w',
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
        )
        self.label_category.pack(side="left", padx=2)
        self.label_category._ctkmaker_min = 75
        self.label_category._ctkmaker_fixed = True

        mytempvalues = list(self.data_manager.user_data["categories"] if self.data_manager.user_data["categories"] else ['No Categories!'])

        self.field_category = ctk.CTkOptionMenu(
            self.category,
            corner_radius=6,
            command=self.add_category_from_dropdown,
            values=mytempvalues,
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
        self.field_category.pack(side="left", fill="both", expand=True, padx=2)
        self.field_category._ctkmaker_min = 60
        self.field_category.set(list(self.data_manager.user_data["categories"])[0] if self.data_manager.user_data["categories"] else "No Categories!")
        self.field_category._scrollable_dropdown = ScrollableDropdown(
            self.field_category,
            font=self.field_category.cget("font"),
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

        self.category.bind("<Configure>", lambda _e, _c=self.category: ctk.balance_pack(_c, 'width'))

        self.website = ctk.CTkFrame(
            self.password_edit_form,
            width=400,
            height=40,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.website.pack(fill="x", side="top", pady=2)
        self.website._ctkmaker_min = 20
        self.website._ctkmaker_fixed = True

        self.website.pack_propagate(False)
        self.website.grid_propagate(False)

        self.label_website = ctk.CTkLabel(
            self.website,
            width=100,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=10,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text='Website',
            font_wrap=True,
            anchor='w',
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
        )
        self.label_website.pack(side="left", padx=2)
        self.label_website._ctkmaker_min = 68
        self.label_website._ctkmaker_fixed = True

        self.field_website = ctk.CTkEntry(
            self.website,
            corner_radius=6,
            border_width=2,
            border_color='#565b5e',
            placeholder_text='Enter url…',
            fg_color='#343638',
            text_color='#dce4ee',
            placeholder_text_color='#9ea0a2',
            justify='left',
        )
        self.field_website.pack(side="left", fill="both", expand=True, padx=2)
        self.field_website._ctkmaker_min = 50
        self.field_website.insert(0, 'https://')

        self.button_open_website = ctk.CTkButton(
            self.website,
            width=150,
            height=40,
            corner_radius=6,
            border_width=0,
            border_color='#efefef',
            text='Open Website',
            text_color='#ffffff',
            full_circle=True,
            fg_color='transparent',
            pressed_color='#2b2b2b',
            image=self.img_plus,
            command=self.open_website_in_browser,
        )
        self.button_open_website.pack(side="left", padx=2)
        self.button_open_website._ctkmaker_min = 40
        self.button_open_website._ctkmaker_fixed = True

        self.website.bind("<Configure>", lambda _e, _c=self.website: ctk.balance_pack(_c, 'width'))

        self.password_edit_form.bind("<Configure>", lambda _e, _c=self.password_edit_form: ctk.balance_pack(_c, 'height'), add="+")

        self.footer_pass = ctk.CTkFrame(
            self.main_frame_pass,
            width=400,
            height=40,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.footer_pass.pack(fill="x", side="top")
        self.footer_pass._ctkmaker_min = 20
        self.footer_pass._ctkmaker_fixed = True

        self.footer_pass.pack_propagate(False)
        self.footer_pass.grid_propagate(False)

        self.label_status_pass = ctk.CTkLabel(
            self.footer_pass,
            width=100,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=10,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text='Status:',
            font_wrap=True,
            anchor='w',
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
        )
        self.label_status_pass.pack(side="left", padx=2)
        self.label_status_pass._ctkmaker_min = 58
        self.label_status_pass._ctkmaker_fixed = True

        self.field_status_pass = ctk.CTkOptionMenu(
            self.footer_pass,
            corner_radius=6,
            values=['Active', 'Inactive'],
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
        self.field_status_pass.pack(side="left", padx=2)
        self.field_status_pass._ctkmaker_min = 60
        self.field_status_pass._ctkmaker_fixed = True
        self.field_status_pass.set('Active')
        self.field_status_pass._scrollable_dropdown = ScrollableDropdown(
            self.field_status_pass,
            font=self.field_status_pass.cget("font"),
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

        self.button_save_pass = ctk.CTkButton(
            self.footer_pass,
            height=32,
            corner_radius=6,
            border_width=0,
            border_color='#efefef',
            text='Save',
            text_color='#ffffff',
            full_circle=True,
            command=self.save_password
        )
        self.button_save_pass.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.button_save_pass._ctkmaker_min = 52

        self.footer_pass.bind("<Configure>", lambda _e, _c=self.footer_pass: ctk.balance_pack(_c, 'width'))

        self.main_frame_pass.bind("<Configure>", lambda _e, _c=self.main_frame_pass: ctk.balance_pack(_c, 'height'))

        self.main_frame_cat = ctk.CTkFrame(
            self.main_frame_container,
            width=321,
            height=330,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.main_frame_cat.grid(row=0, column=0, sticky="nsew")

        self.main_frame_cat.pack_propagate(False)
        self.main_frame_cat.grid_propagate(False)

        self.header_cat = ctk.CTkFrame(
            self.main_frame_cat,
            width=450,
            height=50,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='#2b2b2b',
        )
        self.header_cat.pack(fill="x", side="top")
        self.header_cat._ctkmaker_min = 20
        self.header_cat._ctkmaker_fixed = True

        self.header_cat.pack_propagate(False)
        self.header_cat.grid_propagate(False)

        self.category_name_field = ctk.CTkEntry(
            self.header_cat,
            corner_radius=0,
            border_width=2,
            border_color='#565b5e',
            placeholder_text='Enter Category Name...',
            fg_color='#343638',
            text_color='#dce4ee',
            placeholder_text_color='#9ea0a2',
            justify='left',
        )
        self.category_name_field.pack(side="left", fill="both", expand=True)
        self.category_name_field._ctkmaker_min = 50

        self.delete_category_button = DangerousButton(
            self.header_cat,
            width=80,
            height=50,
            text='Delete!',
            full_circle=True,
            image=self.img_trash_2,
            command=self.delete_category
        )
        self.delete_category_button.pack(side="left", padx=5, pady=5)
        self.delete_category_button._ctkmaker_min = 93
        self.delete_category_button._ctkmaker_fixed = True

        self.btn_close_cat = ctk.CTkButton(
            self.header_cat,
            width=80,
            height=50,
            corner_radius=6,
            border_width=0,
            border_color='#efefef',
            compound='right',
            text='Close',
            text_color='#ffffff',
            full_circle=True,
            fg_color='#565b5e',
            pressed_color="#929394",
            image=self.img_x,
        )
        self.btn_close_cat.pack(side="left", padx=5, pady=5)
        self.btn_close_cat._ctkmaker_min = 93
        self.btn_close_cat._ctkmaker_fixed = True

        self.header_cat.bind("<Configure>", lambda _e, _c=self.header_cat: ctk.balance_pack(_c, 'width'))

        self.category_edit_form = ctk.CTkScrollableFrame(
            self.main_frame_cat,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            label_fg_color='#3a3a3a',
            label_text_color='#dce4ee',
            scrollbar_fg_color='transparent',
            scrollbar_button_color='#3a3a3a',
            scrollbar_button_hover_color='#4a4a4a',
            fg_color='#2b2b2b',
        )
        self.category_edit_form.pack(side="top", fill="both", expand=True)
        self.category_edit_form._ctkmaker_min = 40
        self.category_edit_form._parent_frame.configure(width=200, height=200)
        self.category_edit_form._parent_frame.grid_propagate(False)

        self.description_category = ctk.CTkFrame(
            self.category_edit_form,
            width=400,
            height=40,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.description_category.pack(fill="x", side="top", pady=2)
        self.description_category._ctkmaker_min = 20
        self.description_category._ctkmaker_fixed = True

        self.description_category.pack_propagate(False)
        self.description_category.grid_propagate(False)

        self.label_desc_cat = ctk.CTkLabel(
            self.description_category,
            width=100,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=10,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text='Description',
            font_wrap=True,
            anchor='w',
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
        )
        self.label_desc_cat.pack(side="left", padx=2)
        self.label_desc_cat._ctkmaker_min = 91
        self.label_desc_cat._ctkmaker_fixed = True

        self.field_desc_cat = ctk.CTkEntry(
            self.description_category,
            corner_radius=6,
            border_width=2,
            border_color='#565b5e',
            placeholder_text='Enter description…',
            fg_color='#343638',
            text_color='#dce4ee',
            placeholder_text_color='#9ea0a2',
            justify='left',
        )
        self.field_desc_cat.pack(side="left", fill="both", expand=True, padx=2)
        self.field_desc_cat._ctkmaker_min = 50

        self.description_category.bind("<Configure>", lambda _e, _c=self.description_category: ctk.balance_pack(_c, 'width'))

        self.type = ctk.CTkFrame(
            self.category_edit_form,
            width=400,
            height=40,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.type.pack(fill="x", side="top", pady=2)
        self.type._ctkmaker_min = 20
        self.type._ctkmaker_fixed = True

        self.type.pack_propagate(False)
        self.type.grid_propagate(False)

        self.label_type = ctk.CTkLabel(
            self.type,
            width=100,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=10,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text='Type',
            font_wrap=True,
            anchor='w',
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
        )
        self.label_type.pack(side="left", padx=2)
        self.label_type._ctkmaker_min = 75
        self.label_type._ctkmaker_fixed = True

        self.field_type = ctk.CTkOptionMenu(
            self.type,
            corner_radius=6,
            values=['Digital', 'Physical'],
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
        self.field_type.pack(side="left", fill="both", expand=True, padx=2)
        self.field_type._ctkmaker_min = 60
        self.field_type.set('Digital')
        self.field_type._scrollable_dropdown = ScrollableDropdown(
            self.field_type,
            font=self.field_type.cget("font"),
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

        self.type.bind("<Configure>", lambda _e, _c=self.type: ctk.balance_pack(_c, 'width'))

        self.category_edit_form.bind("<Configure>", lambda _e, _c=self.category_edit_form: ctk.balance_pack(_c, 'height'), add="+")

        self.footer_cat = ctk.CTkFrame(
            self.main_frame_cat,
            width=400,
            height=40,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.footer_cat.pack(fill="x", side="top")
        self.footer_cat._ctkmaker_min = 20
        self.footer_cat._ctkmaker_fixed = True

        self.footer_cat.pack_propagate(False)
        self.footer_cat.grid_propagate(False)

        self.button_save_cat = ctk.CTkButton(
            self.footer_cat,
            height=32,
            corner_radius=6,
            border_width=0,
            border_color='#efefef',
            text='Save',
            text_color='#ffffff',
            full_circle=True,
            command=self.save_category
        )
        self.button_save_cat.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.button_save_cat._ctkmaker_min = 52

        self.footer_cat.bind("<Configure>", lambda _e, _c=self.footer_cat: ctk.balance_pack(_c, 'width'))

        self.main_frame_cat.bind("<Configure>", lambda _e, _c=self.main_frame_cat: ctk.balance_pack(_c, 'height'))

        self.main_frame_none = ctk.CTkFrame(
            self.main_frame_container,
            width=240,
            height=180,
            corner_radius=6,
            border_width=0,
            border_color='#565b5e',
            fg_color='transparent',
        )
        self.main_frame_none.grid(row=0, column=0, sticky="nsew")

        self.main_frame_none.pack_propagate(False)
        self.main_frame_none.grid_propagate(False)

        self.label_please_select = ctk.CTkLabel(
            self.main_frame_none,
            width=100,
            corner_radius=0,
            border_width=0,
            border_color='#565b5e',
            padx=0,
            pady=0,
            cursor='',
            takefocus=False,
            fg_color='transparent',
            text='No category or password selected.\nTo view and edit please select or create one. ',
            font_wrap=True,
            justify='center',
            text_color='#ffffff',
            text_color_disabled='#a0a0a0',
            compound='left',
            full_circle=True,
            unified_bind=True,
        )
        self.label_please_select.pack(side="top", fill="both", expand=True, pady=2)
        self.label_please_select._ctkmaker_min = 16

        self.set_main_frame(self.main_frame_none)
        self.update_password_list("All")

        self.btn_close_pass.configure(command=lambda: self.set_main_frame(self.main_frame_none))
        self.btn_close_cat.configure(command=lambda: self.set_main_frame(self.main_frame_none))

        self.bind("<Control-s>", lambda _e: self.save_current_item())
        self.bind("<Control-w>", lambda _e: self.set_main_frame(self.main_frame_none))
        self.bind("<Alt-a>", lambda _e: self.open_account_settings())
        self.bind_all("<Key>", self.update_unsaved)
        self.bind_all("<Button-1>", self.update_unsaved)

        if show_loading_window:
            self.loadtk.update_progress()
        reset_geometry_managers()

    def set_main_frame(self, frame):
        self.update_unsaved()
        if self.check_for_unsaved_changes():
            match self.prompt_save_changes().lower():
                case "save":
                    self.save_current_item()
                    frame.tkraise()
                case "discard":
                    frame.tkraise()
                case "cancel":
                    print("User canceled the action. Staying on the current frame.")
                    return False
        else:
            frame.tkraise()
        self.update_password_list()
        self.update_category_list()
        match frame:
            case self.main_frame_pass:
                self.current_main_frame = "password"
            case self.main_frame_cat:
                self.current_main_frame = "category"
            case self.main_frame_none:
                self.current_main_frame = "none"
            case _:
                self.current_main_frame = "none"
        return True

    def handle_login_submission(self, username, password, remember_username):
        username = (username or "").strip()
        if not username or not password:
            return False

        if SecureDataManager.verify_credentials(username, password):
            if debug_mode == "verbose":
                print(f"Credentials: Username: {username}, Password: {password}, Remember: {bool(remember_username)}")
            self.current_user = username
            self.signedin = True
            self.data_manager = SecureDataManager(username, password)
            if debug_mode == "verbose":
                print(f"User data loaded for {username}: {self.data_manager.user_data}")
            if self.data_manager.start_maximised():
                self.after(300, lambda: self.state('zoomed'))
            if remember_username:
                rememberUsername(self.current_user)
            return True

        target = self.loginDialog if getattr(self, "loginDialog", None) and self.loginDialog.winfo_exists() else self
        show_toast(target, "Invalid username or password.", "error")
        return False

    def handle_signup_submission(self, username, password, confirm_password, remember_username):
        username = (username or "").strip()
        if not username or not password or not confirm_password:
            return False

        if password != confirm_password:
            target = self.signupDialog if getattr(self, "signupDialog", None) and self.signupDialog.winfo_exists() else self
            show_toast(target, "Passwords do not match.", "error")
            return False

        if SecureDataManager.username_exists(username):
            target = self.signupDialog if getattr(self, "signupDialog", None) and self.signupDialog.winfo_exists() else self
            show_toast(target, f"The username '{username}' is already taken.", "error")
            return False

        try:
            if debug_mode == "verbose":
                print(f"Credentials (signup): Username: {username}, Password: {password}, Remember: {bool(remember_username)}")
            self.data_manager = SecureDataManager(username, password, create=True)
            self.current_user = username
            self.signedin = True
            if self.data_manager.start_maximised():
                self.after(300, lambda: self.state('zoomed'))
            if remember_username:
                rememberUsername(self.current_user)
            return True
        except:
            target = self.signupDialog if getattr(self, "signupDialog", None) and self.signupDialog.winfo_exists() else self
            show_toast(target, "Failed to create account. Please try again.", "error")
            return False

    def openLoginDialog(self):
        self.loginDialog = login.Login(self, on_submit=self.handle_login_submission)
        self.wait_window(self.loginDialog)

        if self.loginDialog.request_signup_flag:
            return "signup"

        if self.loginDialog.username_data is None and self.loginDialog.password_data is None:
            return "quit"

        if self.signedin:
            return "signedin"

        return "signin"

    def openSignupDialog(self):
        self.signupDialog = signup.Signup(self, on_submit=self.handle_signup_submission)
        self.wait_window(self.signupDialog)

        if self.signupDialog.request_signin_flag:
            return "signin"

        if self.signupDialog.username_data is None and self.signupDialog.password_data is None and self.signupDialog.confirm_password_data is None:
            return "quit"

        if self.signedin:
            return "signedin"

        return "signup"

    def requestAccount(self):
        self.signin_or_signup = "signin"
        while not self.signedin and self.winfo_exists():
            if self.signin_or_signup == "signup":
                self.signin_or_signup = self.openSignupDialog()
            else:
                self.signin_or_signup = self.openLoginDialog()
            if self.signin_or_signup == "quit":
                self.destroy()
                break

    def update_category_list(self, unsaved_category=None):
        for child in self.category_list_sf_1.winfo_children():
            child.destroy()
        self.category_buttons = []

        self.all_btn_category = ctk.CTkButton(
            self.category_list_sf_1,
            height=32,
            corner_radius=6,
            border_width=0,
            border_color='#efefef',
            text='All',
            text_color='#ffffff',
            full_circle=True,
            command=lambda: self.select_category("All") and setattr(self, "selected_category", "All")
        )
        self.all_btn_category.pack(side="top", pady=2)
        self.all_btn_category._ctkmaker_min = 32
        self.all_btn_category._ctkmaker_fixed = True

        for category in self.data_manager.user_data["categories"]:
            if debug_mode == "verbose":
                print(f"Creating button for category: {category}")
            category_button = ctk.CTkButton(
                self.category_list_sf_1,
                height=32,
                corner_radius=6,
                border_width=0,
                border_color='#efefef',
                text='•' + unsaved_category if category == unsaved_category else category,
                text_color='#ffffff',
                full_circle=True,
                command=lambda c=category: self.select_category(c)
            )
            category_button.pack(side="top", pady=2)
            category_button._ctkmaker_min = 32
            category_button._ctkmaker_fixed = True
            self.category_buttons.append(category_button)

        if len(self.category_buttons) == 0:
            self.no_categories_label = ctk.CTkLabel(
                self.category_list_sf_1,
                text="No categories available.\nPlease create one first.",
                text_color="#ffffff",
            )
            self.no_categories_label.pack(side="top", fill="x", pady=2)

        self.plus_category_btn_1 = ctk.CTkButton(
            self.category_list_sf_1,
            width=32,
            height=32,
            corner_radius=6,
            border_width=0,
            border_color='#efefef',
            text='',
            text_color='#ffffff',
            full_circle=True,
            image=self.img_plus,
            command=self.add_category
        )
        self.plus_category_btn_1.pack(side="top", pady=2)
        self.plus_category_btn_1._ctkmaker_min = 32
        self.plus_category_btn_1._ctkmaker_fixed = True

    def update_password_list(self, unsaved_password=None):
        if debug_mode == "verbose":
            print(f"Traceback[update_password_list()]@{datetime.datetime.now()}: {'\n'.join(traceback.format_stack())}")
        for child in self.password_list_sf_1.winfo_children():
            child.destroy()
        self.password_buttons = []

        if debug_mode == "verbose":
            print(f"Password data: {self.data_manager.user_data['passwords']}")

        for password, data in self.data_manager.user_data["passwords"].items():
            if self.selected_category.lower() == "all" or data.get("category") == self.selected_category or self.selected_category is None:
                if debug_mode == "verbose":
                    print(f"Creating button for password: {password}")
                password_button = ctk.CTkButton(
                    self.password_list_sf_1,
                    height=32,
                    corner_radius=6,
                    border_width=0,
                    border_color='#efefef',
                    text='•' + unsaved_password if password==unsaved_password else password,
                    text_color='#ffffff',
                    full_circle=True,
                    command=lambda p=password: (self.select_password(p))
                )
                password_button.pack(side="top", pady=2)
                password_button._ctkmaker_min = 32
                password_button._ctkmaker_fixed = True
                self.password_buttons.append(password_button)
                if debug_mode == "verbose":
                    print(f"Added password button for: {password}")

        if len(self.password_buttons) == 0:
            if debug_mode == "verbose":
                print("No passwords available to display.")
            self.no_passwords_label = ctk.CTkLabel(
                self.password_list_sf_1,
                text="No passwords available.\nPlease create one first.",
                text_color="#ffffff",
            )
            self.no_passwords_label.pack(side="top", fill="x", pady=2)

        self.plus_password_btn_1 = ctk.CTkButton(
            self.password_list_sf_1,
            width=32,
            height=32,
            corner_radius=6,
            border_width=0,
            border_color='#efefef',
            text='',
            text_color='#ffffff',
            full_circle=True,
            image=self.img_plus,
            command=self.add_password
        )
        self.plus_password_btn_1.pack(side="top", pady=2)
        self.plus_password_btn_1._ctkmaker_min = 32
        self.plus_password_btn_1._ctkmaker_fixed = True

    def _toggle_password(self):
        if debug_mode == "verbose":
            print("Toggling password visibility")
        current = self.field_password.cget("show")
        new_show = "" if current == "•" else "•"
        self.field_password.configure(show=new_show)
        self.show_hide_password.configure(
            image=self.img_eye_off if new_show == "" else self.img_eye,
            text="Hide Password" if new_show == "" else "Show Password",
        )

    def select_category(self, category_name):
        if debug_mode == "verbose":
            print(f"Selecting category: {category_name}")
        if not category_name:
            return

        if category_name.lower() == "all":
            print("All categories selected. Updating password list to show all passwords.")
            self.selected_category = "All"
            self.update_password_list("All")
            self.set_main_frame(self.main_frame_none)
            return

        self.set_main_frame(self.main_frame_cat)
        self.selected_category = category_name
        self.category_name_field.delete(0, tk.END)
        self.category_name_field.insert(0, category_name)

        category_data = self.data_manager.user_data["categories"].get(category_name)
        if category_data:
            self.field_desc_cat.delete(0, tk.END)
            self.field_desc_cat.insert(0, category_data["description"])
            self.field_type.set(category_data.get("type", "Digital"))

        self.update_category_list()
        self.update_password_list()

    def select_password(self, password_name):
        if debug_mode == "verbose":
            print(f"Selecting password: {password_name}")
        if not password_name:
            return

        password_data = self.data_manager.user_data["passwords"].get(password_name)

        self.set_main_frame(self.main_frame_pass)
        self.selected_password = password_name

        if password_data:
            self.password_name_field.delete(0, tk.END)
            self.password_name_field.insert(0, password_name)
            self.field_desc_pass.delete(0, tk.END)
            self.field_desc_pass.insert(0, password_data.get("description", ""))
            if password_data.get("description", "") == "":
                self.field_desc_pass._activate_placeholder()
            self.field_user.delete(0, tk.END)
            self.field_user.insert(0, password_data.get("username", ""))
            if password_data.get("username", "") == "":
                self.field_user._activate_placeholder()
            password_show = self.field_password.cget("show")
            self.field_password.delete(0, tk.END)
            self.field_password.insert(0, password_data.get("password", ""))
            if password_data.get("password", "") == "":
                self.field_password._activate_placeholder()
            self.field_password.configure(show=password_show)
            self.field_category.set(password_data.get("category", "Could not find category!"))
            self.field_website.delete(0, tk.END)
            self.field_website.insert(0, password_data.get("website", "https://"))
            if password_data.get("website", "") == "":
                self.field_website._activate_placeholder()
            self.field_status_pass.set(password_data.get("status", "Active"))

        self.update_category_list()
        self.update_password_list()

    def open_account_settings(self):
        self.account_settings_dialog = account.Account(self, current_user=self.current_user, theme_names=theme_names, current_theme=self.current_theme)
        self.wait_window(self.account_settings_dialog)

    def add_category(self):
        if self.set_main_frame(self.main_frame_cat):
            self.selected_category = None
            self.category_name_field.delete(0, tk.END)
            self.field_desc_cat.delete(0, tk.END)
            self.field_type.set("Digital")
            self.category_name_field.focus_set()
            self.category_name_field._activate_placeholder()
            self.field_desc_cat._activate_placeholder()

    def add_category_from_dropdown(self, selected_category):
        if selected_category == "Add New Category...":
            self.add_category()

    def add_password(self):
        if self.set_main_frame(self.main_frame_pass):
            self.selected_password = None
            self.password_name_field.delete(0, tk.END)
            self.field_desc_pass.delete(0, tk.END)
            self.field_user.delete(0, tk.END)
            self.field_password.delete(0, tk.END)
            self.field_category.configure(values=list(self.data_manager.user_data["categories"].keys()) if len(self.data_manager.user_data["categories"]) > 0 else ["Add New Category..."])
            self.field_category.set(list(self.data_manager.user_data["categories"].keys())[0] if len(self.data_manager.user_data["categories"]) > 0 else "No Categories!")
            self.field_website.delete(0, tk.END)
            self.field_status_pass.set("Active")
            self.password_name_field._activate_placeholder()
            self.field_desc_pass._activate_placeholder()
            self.field_user._activate_placeholder()
            self.field_password._activate_placeholder()
            self.field_password.configure(show="•")
            self.field_website._activate_placeholder()
            self.password_name_field.focus_set()

    def logout(self):
        if self.account_settings_dialog.winfo_exists():
            self.account_settings_dialog.destroy()
        self.withdraw()
        self.current_user = None
        self.signedin = False
        self.selected_category = None
        self.selected_password = None
        self.requestAccount()
        self.deiconify()
        for child in self.winfo_children():
            child.destroy()
        self._build_ui()

    def save_category(self):
        category_name = self.category_name_field.get().strip()
        description = self.field_desc_cat.get().strip()
        category_type = self.field_type.get()

        if not category_name:
            show_toast(self, "Category name cannot be empty.", "error")
            return

        user_data = self.data_manager.user_data
        if "categories" not in user_data:
            user_data["categories"] = {}
            print(f"Initialized 'categories' for user {self.current_user}")

        user_data["categories"][category_name] = {
            "description": description,
            "type": category_type
        }

        if category_name != self.selected_category and self.selected_category is not None:
            # Run recursive function to update all passwords that belong to the old category name
            self.recursive_rename_category(self.selected_category, category_name)
            user_data["categories"][category_name] = user_data["categories"].pop(self.selected_category)

        self.selected_category = category_name

        self.data_manager.user_data = user_data
        self.data_manager.save_user_data()
        show_toast(self, f"Category '{category_name}' saved successfully.", "success")
        self.update_category_list()

    def recursive_rename_category(self, old_category_name, new_category_name):
        user_data = self.data_manager.user_data
        if "passwords" in user_data:
            for password_name, password_data in list(user_data["passwords"].items()):
                if password_data.get("category") == old_category_name:
                    password_data["category"] = new_category_name
                    print(f"Updated category for password '{password_name}' to '{new_category_name}'")
        self.data_manager.user_data = user_data
        self.data_manager.save_user_data()

    def save_password(self):
        print("Saving password...")
        password_name = self.password_name_field.get().strip()

        if self.field_category.get() == "No Categories!" or self.field_category.get() == "Add New Category...":
            show_toast(self, "Please create a category first.", "error")
            return

        user_data = self.data_manager.user_data
        if "passwords" not in user_data:
            user_data["passwords"] = {}
            print(f"Initialized 'passwords' for user {self.current_user}")

        user_data["passwords"][password_name] = {
            "description": self.field_desc_pass.get().strip(),
            "category": self.field_category.get(),
            "username": self.field_user.get().strip(),
            "password": self.field_password.get().strip(),
            "website": self.field_website.get().strip(),
            "status": self.field_status_pass.get()
        }

        if password_name != self.selected_password and self.selected_password is not None and self.selected_password in user_data["passwords"] and self.selected_password != "":
            user_data["passwords"][password_name] = user_data["passwords"].pop(self.selected_password)

        self.selected_password = password_name

        self.data_manager.user_data = user_data
        self.data_manager.save_user_data()
        show_toast(self, f"Password '{password_name}' saved successfully.", "success")
        print(f"Password saved successfully: {password_name}")
        self.update_password_list()

    def delete_category(self):
        category_name = self.category_name_field.get().strip()
        if not category_name:
            self.set_main_frame(self.main_frame_none)
            return
        dependencies = []
        if "passwords" in self.data_manager.user_data:
            for password_name, password_data in list(self.data_manager.user_data["passwords"].items()):
                if password_data.get("category") == category_name:
                    dependencies.append(password_name)
        answer = CustomButtonDialog(self, title="Delete Category", message=f"Are you sure you want to delete the category '{category_name}'?\n\nThis will also delete {len(dependencies)} associated password(s):\n{', '.join(dependencies) if dependencies else 'None'}", options={"Delete": "#E01E1E", "Cancel": "#2A2A2A"}, icon_path='assets/icons/circle-exclamation-mark.ico').result
        if answer.lower() == "delete":
            self.data_manager.user_data["categories"].pop(category_name, None)
            for password_name in dependencies:
                self.data_manager.user_data["passwords"].pop(password_name, None)
            self.data_manager.save_user_data()
            show_toast(self, f"Category '{category_name}' deleted successfully.", "success")
            self.selected_category = None
            self.update_category_list()
            self.update_password_list()
            self.set_main_frame(self.main_frame_none)
        else:
            print("User canceled the delete action. Staying on the current frame.")

    def delete_password(self):
        password_name = self.password_name_field.get().strip()
        if not password_name:
            self.set_main_frame(self.main_frame_none)
            return
        self.data_manager.user_data["passwords"].pop(password_name, None)
        self.data_manager.save_user_data()
        show_toast(self, f"Password '{password_name}' deleted successfully.", "success")
        self.selected_password = None
        self.update_password_list()
        self.set_main_frame(self.main_frame_none)

    def save_current_item(self):
        if self.current_main_frame == "password":
            self.save_password()
        elif self.current_main_frame == "category":
            self.save_category()

    def copy_password_to_clipboard(self):
        password = self.field_password.get()
        if password:
            self.clipboard_clear()
            self.clipboard_append(password)
            show_toast(self, "Password copied to clipboard.", "success")
            self.copy_password_button.configure(text="Copied!", fg_color="#1d681f", hover_color="#1a5a1a", image=self.img_check)
            self.after(2000, lambda: self.copy_password_button.configure(text="Copy Password", fg_color="transparent", hover_color=ctk.ThemeManager.theme["CTkButton"]["hover_color"], image=self.img_copy))
        else:
            show_toast(self, "No password to copy.", "error")

    def check_for_unsaved_changes(self):
        if self.current_main_frame == "password":
            password_name = self.password_name_field.get().strip()
            if password_name in self.data_manager.user_data["passwords"] or self.selected_password in self.data_manager.user_data["passwords"]:
                saved_data = self.data_manager.user_data["passwords"][self.selected_password] if self.selected_password in self.data_manager.user_data["passwords"] else password_name
                current_data = {
                    "description": self.field_desc_pass.get().strip(),
                    "category": self.field_category.get(),
                    "username": self.field_user.get().strip(),
                    "password": self.field_password.get().strip(),
                    "website": self.field_website.get().strip(),
                    "status": self.field_status_pass.get()
                }
                if debug_mode == "verbose":
                    print(f"Saved data: '{password_name}': {saved_data}")
                    print(f"Current data: '{self.selected_password}': {current_data}")
                if self.selected_password == "All":
                    return False
                return saved_data != current_data or password_name != self.selected_password
        elif self.current_main_frame == "category":
            category_name = self.category_name_field.get().strip()
            if category_name in self.data_manager.user_data["categories"] or self.selected_category in self.data_manager.user_data["categories"]:
                saved_data = self.data_manager.user_data["categories"][self.selected_category] if self.selected_category in self.data_manager.user_data["categories"] else category_name
                current_data = {
                    "description": self.field_desc_cat.get().strip(),
                    "type": self.field_type.get()
                }
                if debug_mode == "verbose":
                    print(f"Saved data: '{category_name}': {saved_data}")
                    print(f"Current data: '{self.selected_category}': {current_data}")
                if self.selected_category == "All":
                    return False
                return saved_data != current_data or category_name != self.selected_category
        return False

    def prompt_save_changes(self):
        dialog = CustomButtonDialog(self, title="Unsaved Changes", message="You have unsaved changes. What would you like to do?", options={"Save": "#1d681f", "Discard": "#E01E1E", "Cancel": "#2A2A2A"}, icon_path='assets/icons/circle-question-mark.ico')
        return dialog.result

    def on_close(self):
        if self.check_for_unsaved_changes():
            match self.prompt_save_changes().lower():
                case "save":
                    self.save_current_item()
                    self.destroy()
                case "discard":
                    self.destroy()
                case "cancel":
                    print("User canceled the close action. Staying on the current frame.")
                    return
        else:
            self.destroy()

    def open_website_in_browser(self):
        website_url = self.field_website.get().strip()
        if website_url and website_url != "https://":
            if not website_url.startswith("http://") and not website_url.startswith("https://"):
                website_url = "https://" + website_url
            try:
                webbrowser.open(website_url)
            except Exception as e:
                show_toast(self, f"Failed to open the website: {e}", "error")
        else:
            show_toast(self, "No valid website URL provided.", "error")

    def update_unsaved(self, event=None):
        if debug_mode == "verbose":
            print(f"Traceback[update_unsaved()]@{datetime.datetime.now()}: {'\n'.join(traceback.format_stack())}")
        unsaved = self.check_for_unsaved_changes()
        if unsaved:
            match self.current_main_frame:
                case "password":
                    self.update_password_list(unsaved_password=self.selected_password)
                case "category":
                    self.update_category_list(unsaved_category=self.selected_category)
        else:
            self.update_password_list()
            self.update_category_list()

    def save_username(self, username, remember_username):
        if debug_mode == "verbose":
            print(f"Saving username: {username}")
        if remember_username:
            rememberUsername(username)
        self.current_user = username
        self.data_manager.change_username(username)
        show_toast(self, f"Username '{username}' saved successfully.", "success")

    def delete_account(self):
        self.data_manager.delete_account()
        show_toast(self, f"Account '{self.current_user}' deleted successfully.", "success")
        self.account_settings_dialog.destroy()
        self.logout()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = MainWindow()
    try:
        if app.winfo_exists():
            app.mainloop()
    except tk.TclError:
        pass
