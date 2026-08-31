import customtkinter as ctk

app = ctk.CTk()
app.geometry("300x200")
app.title("Simple Dropdown Example")

def option_callback(choice):
    if choice == "Create Account":
        global combobox
        combobox.set("No Accounts Found!")
        print("Create Account option selected.")

# Create the dropdown (combobox)
combobox = ctk.CTkComboBox(
    master=app,
    values=["Create Account"],
    command=option_callback
)
combobox.pack(pady=40, fill="x", padx=20)

# Set default value
combobox.set("No Accounts Found!")

app.mainloop()
