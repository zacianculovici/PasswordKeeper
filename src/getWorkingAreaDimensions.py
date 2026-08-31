import tkinter as tk

root = tk.Tk()
# Hide the window immediately so the user doesn't see it flash
root.withdraw() 

# Force the window to maximize (respects the taskbar/dock bounds)
root.state('zoomed')
root.update()

# Extract the maximized dimensions
working_width = root.winfo_width()
working_height = root.winfo_height()

print(f"Working Width: {working_width}")
print(f"Working Height: {working_height}")

root.destroy()
