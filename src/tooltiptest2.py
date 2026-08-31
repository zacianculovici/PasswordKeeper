import customtkinter
from CTkToolTip import CTkToolTip
from PIL import Image

root = customtkinter.CTk()
root.geometry("300x200")

# 1. Load your icon using CTkImage
# (Ensure you have an image file named 'info_icon.png' in your project folder)
icon_image = customtkinter.CTkImage(
    light_image=Image.open("assets/images/eye.png"),  # Path to your icon for light mode
    dark_image=Image.open("assets/images/eye.png"),   # Path to your icon for dark mode
    size=(30, 30) # Adjust icon size here
)

button = customtkinter.CTkButton(root, 
                                 text="Hover for Info",
                                 bg_color="#3c3c3c",
                                 fg_color="#3c3c3c",
                                 hover=False,
                                 )
button.pack(pady=50)

# 2. Pass the icon into the CTkToolTip
CTkToolTip(
    button, 
    message="This tooltip includes an icon!",
    image=icon_image,
    compound="left", # Places the icon to the 'left', 'right', 'top', or 'bottom' of the text
    font=("Arial", 20, "bold"),
)

root.mainloop()
