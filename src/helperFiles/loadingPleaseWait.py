import customtkinter as ctk
from tkinter import font as tkfont
from helperFiles.center_window_on_screen import center_window_on_screen

class LoadingWindow(ctk.CTkToplevel):
    def __init__(self, parent, text="Loading assets: <X/X> please wait...", total_amount=100, grab=True, auto_update=False, delay=0, debug="off"):
        super().__init__(parent)
        self.debug = debug

        self.after(100)  # Allow the window to initialize before measuring
        parent.update_idletasks()  # Ensure the parent window is updated

        self.auto_update = auto_update
        self.delay = delay

        self.message_font = tkfont.Font(family='Segoe UI', size=13, weight='bold')
        self.message_width = self.message_font.measure(max(text.split('\n'), key=len)) + 20  # Add padding
        self.message_height = self.message_font.metrics("linespace") * (text.count('\n') + 2) + 20  # Add padding for multiple lines
        if self.debug in ["medium", "verbose"]:
            print(f"Font height: {self.message_font.metrics('linespace')}, Message height: {self.message_height}, Message width: {self.message_width}")

        self.total_amount = total_amount
        self.resolve_text = lambda text, current, total: text.replace("<X/X>", f"{current}/{total}").replace("<X>", f"{current}").replace("<X%>", f"{(current / total) * 100:.0f}%")
        self.text = text
        self.geometry(f"{self.message_width}x{self.message_height}")
        self.title("Please Wait")
        self.attributes("-topmost", True)  # Keeps window on top
        self.overrideredirect(True)
        self.configure(fg_color='red')

        self.after(100, lambda: center_window_on_screen(self, self.message_width, self.message_height))

        self.frame = ctk.CTkFrame(self, fg_color='black', corner_radius=0, border_width=2, border_color='red')

        self.label = ctk.CTkLabel(self.frame, text=f"{self.resolve_text(self.text, 0, self.total_amount)}", text_color='white')
        self.label.pack(expand=True, fill='both', padx=0, pady=0, anchor='center')

        self.frame.pack(expand=True, fill='both', padx=2, pady=2, anchor='center')

        # Make window modal
        if grab:
            self.grab_set()

        # Start the recursive update loop at step 0
        self.current_step = 0
        if auto_update:
            self.update_progress()

    def update_progress(self):
        if self.current_step <= self.total_amount:
            if self.debug in ["verbose"]:
                print(f"Doing work number: {self.current_step}...")
            self.label.configure(text=self.resolve_text(self.text, self.current_step, self.total_amount))
            self.update_idletasks()  # Ensure the label updates immediately

            # Call this same function again after the delay
            self.current_step += 1
            self.after(self.delay)
            if self.auto_update:
                self.after(self.auto_update, lambda: self.update_progress())
        else:
            self.label.configure(text_color='green', text="Done!")
            # Once complete, wait 1s and close the window
            self.after(1000, lambda: self.finish_loading())

    def finish_loading(self):
        # Close loading window and release grab
        self.grab_release()
        self.destroy()

if __name__ == "__main__":
    app = ctk.CTk()
    top = LoadingWindow(app, text=f"Loading assets: <X%>\nplease wait...\n{"LONG <X/X>"*15}", total_amount=32, auto_update=100)
    app.mainloop()
