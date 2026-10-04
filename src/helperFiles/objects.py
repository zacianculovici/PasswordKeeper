import hashlib
import os
from customtkinter import CTkButton
import customtkinter

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.hashed_username = hashlib.sha256(username.encode()).hexdigest()
        self.hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.hashed_credentials = self.get_hashed_credentials(username, password)

    @staticmethod
    def get_hashed_credentials(username, password):
        credentials = hashlib.sha256(username.encode()).hexdigest() + hashlib.sha256(password.encode()).hexdigest()
        return hashlib.sha256(credentials.encode()).hexdigest()

class NoAccountError(Exception):
    """Exception raised when a user account does not exist."""
    def __init__(self, message="User account does not exist. Please create a new account."):
        self.message = message
        super().__init__(self.message)

class DangerousButton(CTkButton):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            fg_color="transparent",
            hover=False,
            text_color="white",
            border_color="red",
            border_width=2,
            corner_radius=8,
        )
        self.bind("<Enter>", lambda event: self.configure(fg_color="red"))
        self.bind("<Leave>", lambda event: self.configure(fg_color="transparent"))

def safeDelete(file_path):
    """Safely delete a file if it exists."""
    try:
        if file_path.exists():
            with open(file_path, 'w') as file:  # Extra precaution
                file.write("0x00")
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        else:
            print(f"File does not exist: {file_path}")
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")

if __name__ == "__main__":
    app = customtkinter.CTk()
    button = DangerousButton(app, text="Dangerous Action")
    button.pack(pady=20, padx=20)
    app.mainloop()
