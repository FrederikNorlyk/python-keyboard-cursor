import tkinter as tk
import keyboard
import string
import pyautogui
import threading


class Overlay:
    def __init__(self):
        self.grid_positions = {}  # Dictionary to store square positions by label
        self.root = self.setup_root()
        self.canvas = self.setup_canvas()

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

    def setup_root(self):
        root = tk.Tk()
        root.title("Keyboard Cursor")
        root.attributes("-fullscreen", True)
        root.attributes("-topmost", True)
        root.configure(bg="white")
        root.attributes("-transparentcolor", "white")
        root.attributes("-alpha", 0.4)
        return root

    def setup_canvas(self):
        canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        return canvas

    def draw_grid(self, num_columns, num_rows):
        alphabet = string.ascii_uppercase

        for row in range(num_rows):
            for col in range(num_columns):
                # Generate the indexed text
                row_letter = alphabet[row]
                col_letter = alphabet[col]
                text = f"{col_letter}{row_letter}"

                # Calculate the square's position
                x1 = col * self.square_width
                y1 = row * self.square_height
                x2 = x1 + self.square_width
                y2 = y1 + self.square_height

                # Store the center position of each square by label.
                center_x = x1 + self.square_width / 2
                center_y = y1 + self.square_height / 2
                self.grid_positions[text] = (center_x, center_y)

                # Draw the square
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="lightgray", outline="black"
                )

                # Draw the text inside the square
                self.canvas.create_text(
                    center_x,
                    center_y,
                    text=text,
                    font=("Consolas", 12, "bold"),
                    fill="black"
                )

    def listen_for_key_presses(self):
        """Listen for a sequence of key presses to navigate and select within the overlay."""

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

        # Clear the canvas to prepare for drawing the subgrid.
        self.canvas.delete("all")

        # Calculate the new top-left corner of the subgrid
        label = f"{first_character}{second_character}"
        center_x, center_y = self.grid_positions[label]
        x = center_x - self.square_width / 2
        y = center_y - self.square_height / 2

        # Draw a subgrid for fine precision inside the selected square
        self.draw_subgrid(x, y)

        # Listen for the third character
        third_character = None
        shift_key_is_held = False
        while not third_character:
            event = keyboard.read_event(suppress=True)

            if event.event_type == "down":
                if event.name == "esc":
                    self.root.quit()
                    return
                elif event.name == 'skift':
                    shift_key_is_held = True
                    continue

                if not event.name.upper() in self.grid_positions:
                    continue

                third_character = event.name.upper()
            elif event.event_type == 'up' and event.name == 'skift':
                shift_key_is_held = False

        # Clear the canvas so that the mouse can click through the overlay
        self.canvas.delete("all")

        # Perform the mouse click
        x, y = self.grid_positions[third_character]
        pyautogui.moveTo(x, y)

        if shift_key_is_held:
            pyautogui.rightClick(x, y)
        else:
            pyautogui.click(x, y)


        self.root.quit()

    def draw_subgrid(self, x, y):
        """Draw a 6x3 subgrid for finer selection precision inside the selected square."""

        alphabet = string.ascii_uppercase

        # Fixed grid dimensions
        number_of_columns = 6
        number_of_rows = 3

        # Square dimensions
        sub_square_width = self.square_width / number_of_columns
        sub_square_height = self.square_height / number_of_rows

        i = 0
        for row in range(number_of_rows):
            for col in range(number_of_columns):
                letter = alphabet[i]

                # Calculate positions based on both row and column
                x1 = x + col * sub_square_width
                y1 = y + row * sub_square_height
                x2 = x1 + sub_square_width
                y2 = y1 + sub_square_height

                # Store the center position of each square by label.
                center_x = x1 + sub_square_width / 2
                center_y = y1 + sub_square_height / 2
                self.grid_positions[letter] = (center_x, center_y)

                # Draw the square
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="lightgray", outline="black"
                )

                # Draw the text inside the square
                self.canvas.create_text(
                    center_x,
                    center_y,
                    text=letter,
                    font=("Consolas", 12, "bold"),
                    fill="black"
                )

                i += 1


if __name__ == "__main__":
    app = Overlay()
