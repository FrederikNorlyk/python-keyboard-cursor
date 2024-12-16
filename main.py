import tkinter as tk
import keyboard
import threading
import string
import pyautogui

class OverlayApp:
    def __init__(self):
        self.root = None
        self.canvas = None
        self.running = False
        self.grid_positions = {}  # Dictionary to store square positions by label

    def show_overlay(self):
        """Displays the overlay with a fixed 26x26 grid of indexed squares."""
        if self.running:
            return

        self.running = True
        self.root = tk.Tk()
        self.root.title("Grid Overlay")
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="white")  # Use white for transparency
        self.root.attributes("-transparentcolor", "white")

        # Create the canvas
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Screen dimensions
        screen_width = 300 # self.root.winfo_screenwidth()
        screen_height = 300 # self.root.winfo_screenheight()

        # Fixed grid dimensions
        num_columns = 4 # 26
        num_rows = 4 # 26

        # Calculate square size
        square_width = screen_width // num_columns
        square_height = screen_height // num_rows

        # Generate the grid
        alphabet = string.ascii_uppercase
        for row in range(num_rows):
            for col in range(num_columns):
                # Generate the indexed text
                row_letter = alphabet[row % len(alphabet)]
                col_letter = alphabet[col % len(alphabet)]
                text = f"{col_letter}{row_letter}"

                # Calculate square position
                x1 = col * square_width
                y1 = row * square_height
                x2 = x1 + square_width
                y2 = y1 + square_height

                # Store grid position for mouse movement
                self.grid_positions[text] = (x1 + square_width // 2, y1 + square_height // 2)

                # Draw the square
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="lightgray", outline="black"
                )

                # Draw the text inside the square
                self.canvas.create_text(
                    x1 + square_width // 2,
                    y1 + square_height // 2,
                    text=text,
                    font=("Helvetica", 12),
                    fill="black"
                )

        # Handle closing the overlay
        self.root.protocol("WM_DELETE_WINDOW", self.hide_overlay)
        self.root.mainloop()

    def hide_overlay(self):
        """Hides the overlay safely."""
        if self.root:
            try:
                self.root.quit()  # Stop the mainloop
                self.root.update()  # Process any remaining events
                self.root.destroy()  # Destroy the Tk instance
            except Exception as e:
                print(f"Error while hiding overlay: {e}")
            finally:
                self.root = None
                self.canvas = None
                self.grid_positions = {}
                self.running = False


def listen_for_hotkey(app):
    """Listen for key presses to toggle or interact with the overlay."""
    while True:
        if not app.running:
            # Wait for the hotkey to toggle the overlay
            keyboard.wait("shift+alt+o")
            threading.Thread(target=app.show_overlay).start()
        else:
            # Listen for two key presses for navigation
            first_key = None
            while not first_key:
                event = keyboard.read_event(suppress=True)
                if event.event_type == "down" and event.name.isalpha():
                    first_key = event.name.upper()

            second_key = None
            while not second_key:
                event = keyboard.read_event(suppress=True)
                if event.event_type == "down" and event.name.isalpha():
                    second_key = event.name.upper()

            # Construct the label and move the mouse if valid
            label = f"{first_key}{second_key}"
            if label in app.grid_positions:
                x, y = app.grid_positions[label]
                pyautogui.moveTo(x, y)  # Move the mouse to the corresponding square
            else:
                print(f"Invalid grid position: {label}")

            app.hide_overlay()


if __name__ == "__main__":
    app = OverlayApp()
    listen_for_hotkey(app)
