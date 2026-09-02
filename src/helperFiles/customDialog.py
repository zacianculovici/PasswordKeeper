import customtkinter as ctk

class CustomButtonDialog(ctk.CTkToplevel):
    def __init__(self, parent, title="Dialog", message="This is a custom dialog.", options=None, icon_path=None, wrap_number=3):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.grab_set()  # Make the dialog modal
        self.lift()  # Bring the dialog to the front
        self.result = None
        if icon_path:
            self.after(250, lambda: self.iconbitmap(icon_path))

        # Create a label for the message
        self.message_label = ctk.CTkLabel(self, text=message, wraplength=350)
        self.message_label.pack(pady=20)

        # Create a frame for the buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10)

        # Create buttons based on the provided options
        if options:
            # If there are more than wrap_number options, wrap them to the next line
            for i in range(0, len(options.items()), wrap_number):
                row_frame = ctk.CTkFrame(self.button_frame, fg_color="transparent")
                row_frame.pack(pady=5)
                for option_text, option_color in list(options.items())[i:i+wrap_number]:
                    button = ctk.CTkButton(row_frame, text=option_text, command=lambda opt=option_text: self.on_button_click(opt), fg_color=option_color)
                    button.pack(side="left", padx=10)

        self.protocol("WM_DELETE_WINDOW", lambda: self.on_button_click("Cancel"))  # Handle window close button

        parent.wait_window(self)

    def on_button_click(self, option):
        self.result = option
        self.destroy()

if __name__ == "__main__":
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()  # Hide the main window

    dialog = CustomButtonDialog(root, options={"Yes": "#1d681f", "No": "#E01E1E", "Cancel": "#2A2A2A"}, icon_path="assets/icons/favicon.ico")

    print(f"User selected: {dialog.result}")
