import tkinter as tk
import keyboard
import string
import pyautogui
import threading

class OverlayApp:
    def __init__(self):
        self.root = None
        self.canvas = None
        self.grid_positions = {}  # Dictionary to store square positions by label
        self.square_width = None
        self.square_height = None

    def show_overlay(self):
        """Displays the overlay with a fixed 26x26 grid of indexed squares."""
        self.root = tk.Tk()
        self.root.title("Grid Overlay")
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="white")  # Use white for transparency
        self.root.attributes("-transparentcolor", "white")
        self.root.attributes("-alpha", 0.4)

        # Create the canvas
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Fixed grid dimensions
        num_columns = 26
        num_rows = 26

        # Calculate square size
        self.square_width = screen_width / num_columns
        self.square_height = screen_height / num_rows

        # Generate the grid
        self.draw_grid(num_columns, num_rows)

        # Start listening for key presses in a separate thread
        threading.Thread(target=self.listen_for_key_presses, daemon=True).start()

        # Start the Tkinter event loop
        self.root.mainloop()

    def draw_grid(self, num_columns, num_rows):
        alphabet = string.ascii_uppercase

        for row in range(num_rows):
            for col in range(num_columns):
                # Generate the indexed text
                row_letter = alphabet[row]
                col_letter = alphabet[col]
                text = f"{col_letter}{row_letter}"

                # Calculate square position
                x1 = col * self.square_width
                y1 = row * self.square_height
                x2 = x1 + self.square_width
                y2 = y1 + self.square_height

                # Store grid position for mouse movement
                self.grid_positions[text] = (x1 + self.square_width / 2, y1 + self.square_height / 2)

                # Draw the square
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="lightgray", outline="black"
                )

                # Draw the text inside the square
                self.canvas.create_text(
                    x1 + self.square_width / 2,
                    y1 + self.square_height / 2,
                    text=text,
                    font=("Consolas", 12, "bold"),
                    fill="black"
                )

    def listen_for_key_presses(self):
        """Listen for key presses to toggle or interact with the overlay."""

        alphabet = string.ascii_uppercase

        # Detect the first character
        first_character = None
        while not first_character:
            event = keyboard.read_event(suppress=True)

            if not event.event_type == "down":
                continue

            if event.name == "esc":
                self.root.quit()
                return

            if event.name.upper() in alphabet:
                first_character = event.name.upper()

        # Detect the second character
        second_character = None
        while not second_character:
            event = keyboard.read_event(suppress=True)

            if not event.event_type == "down":
                continue

            if event.name == "esc":
                self.root.quit()
                return

            if event.name.upper() in alphabet:
                second_character = event.name.upper()

        # Draw a subgrid for fine precision inside the selected square
        label = f"{first_character}{second_character}"
        if label in self.grid_positions:

            self.canvas.delete("all")

            # Calculate the new top-left corner of the subgrid
            center_x, center_y = self.grid_positions[label]
            x = center_x - self.square_width / 2
            y = center_y - self.square_height / 2

            self.draw_subgrid(x, y)
        else:
            self.root.quit()
            return

        # Listen for the third character
        third_character = None
        while not third_character:
            event = keyboard.read_event(suppress=True)

            if not event.event_type == "down":
                continue

            if event.name == "esc":
                self.root.quit()
                return

            if not event.name.upper() in self.grid_positions:
                continue

            third_character = event.name.upper()

        # Clear the canvas so that the mouse can click through the overlay
        self.canvas.delete("all")

        # Perform the mouse click
        x, y = self.grid_positions[third_character]
        pyautogui.moveTo(x, y)
        pyautogui.click(x, y)

        self.root.quit()

    def draw_subgrid(self, x, y):
        """Draws a new 6x3 grid inside the selected square."""

        alphabet = string.ascii_uppercase

        # Fixed grid dimensions
        num_columns = 6
        num_rows = 3

        # Square dimensions
        sub_square_width = self.square_width / num_columns
        sub_square_height = self.square_height / num_rows

        i = 0
        for row in range(num_rows):
            for col in range(num_columns):
                letter = alphabet[i]

                # Calculate positions based on both row and column
                x1 = x + col * sub_square_width
                y1 = y + row * sub_square_height
                x2 = x1 + sub_square_width
                y2 = y1 + sub_square_height

                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="lightgray", outline="black"
                )

                self.canvas.create_text(
                    x1 + sub_square_width / 2,
                    y1 + sub_square_height / 2,
                    text=letter,
                    font=("Consolas", 12, "bold"),
                    fill="black"
                )

                self.grid_positions[letter] = (x1 + sub_square_width / 2, y1 + sub_square_height / 2)
                i += 1



if __name__ == "__main__":
    app = OverlayApp()
    app.show_overlay()
