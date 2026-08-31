import customtkinter as ctk

def center_window_on_screen(window, width, height, debug_mode="off"):
    """
    Centers a given window on the screen.

    Args:
        window: The window to be centered.
        width: The width of the window.
        height: The height of the window.
    """

    window.after(100)

    if debug_mode == "verbose":
        print(f"Centering window of size {width}x{height} on screen...")

    window.lift() # Bring the window to the front
    window.update_idletasks() # Update "requested size" from geometry manager

    scaling_factor = ctk.ScalingTracker.get_window_scaling(window)
    if debug_mode == "verbose":
        print(f"Scaling factor detected: {scaling_factor*100:.2f}%")

    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Scale the screen dimensions based on the scaling factor
    scaled_screen_width = int(screen_width * scaling_factor)
    scaled_screen_height = int(screen_height * scaling_factor)

    # Calculate the x and y coordinates to center the window
    x = (scaled_screen_width - width) // 2
    y = (scaled_screen_height - height) // 2

    # Set the geometry of the window to center it
    window.geometry(f"{width}x{height}+{x}+{y}")

    if debug_mode == "verbose":
        print(f"Window centered at: {x}, {y} (Screen: {scaled_screen_width}x{scaled_screen_height}, Window: {width}x{height}, Scaling factor: {scaling_factor*100:.2f}%)")

if __name__ == "__main__":
    # Example usage
    app = ctk.CTk()
    center_window_on_screen(app, 800, 600, debug_mode="verbose")  # Example usage with a CTk window of size 800x600
    app.mainloop()
