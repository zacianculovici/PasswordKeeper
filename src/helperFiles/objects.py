import hashlib
from customtkinter import CTkButton
import customtkinter

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.hashed_credentials = self.get_hashed_credentials(username, password)

    @staticmethod
    def get_hashed_credentials(username, password):
        credentials = username + password
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

if __name__ == "__main__":
    app = customtkinter.CTk()
    button = DangerousButton(app, text="Dangerous Action")
    button.pack(pady=20, padx=20)
    app.mainloop()
