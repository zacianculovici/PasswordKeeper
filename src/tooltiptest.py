import customtkinter
from CTkToolTip import CTkToolTip

root = customtkinter.CTk()
root.title("CTkToolTip Customization")
root.geometry("300x200")

# 1. Custom Styled Tooltip
btn_styled = customtkinter.CTkButton(root, text="Styled Button")
btn_styled.pack(pady=20)

label_styled = customtkinter.CTkLabel(root, text="Hover over the button to see the tooltip.")
label_styled.pack(pady=10)

CTkToolTip(
    label_styled,
    message="This is a styled tooltip!",
    bg_color="#34495e",       # Darker blue background
    text_color="#ecf0f1",     # Off-white text
    border_width=1,
    border_color="#2980b9",   # Blue border
    font=("Helvetica", 10, "italic")
)

CTkToolTip(
    btn_styled, 
    message="Custom Style!",
    bg_color="#2c3e50",       # Dark blue background
    text_color="#ecf0f1",     # Off-white text
    border_width=2,
    border_color="#e74c3c",   # Red border
    font=("Arial", 12, "bold")
)

# 2. Dynamic Tooltip
btn_dynamic = customtkinter.CTkButton(root, text="Dynamic Button")
btn_dynamic.pack(pady=20)

# Create the initial tooltip object
dynamic_tip = CTkToolTip(btn_dynamic, message="Original Message")

# Function to change the text dynamically
def update_tooltip():
    dynamic_tip.configure(message="The message has changed!")

# Trigger the update after 3 seconds
root.after(3000, update_tooltip)

root.mainloop()
