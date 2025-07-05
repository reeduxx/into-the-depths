from abc import ABC, abstractmethod
from client.constants import BLOCK_SHADING
from client.screen_buffer import ScreenBuffer

class Menu(ABC):
    """
    Abstract base class for the game menus.

    Provides utility methods for tracking resize events, clearing the 
    screen, centering text, and rendering menu borders.
    All derived menus must implement the 'run()' method.

    Attributes:
        term (blessed.Terminal): The terminal instance used for input and display.
        buffer (ScreenBuffer): The screen buffer used for optimized terminal rendering.
        _prev_width (int): Cached terminal width.
        _prev_height (int): Cached terminal height.
    """
    def __init__(self, term):
        """
        Initializes the menu with a terminal instance.

        Args:
            term (blessed.Terminal): The terminal instance used for input and display.
        """
        self.term = term
        self.buffer = ScreenBuffer(term)
        self._prev_width = term.width
        self._prev_height = term.height
    
    def window_resized(self) -> bool:
        """
        Checks if the terminal has been resized since the last frame.

        Returns:
            bool: True if the terminal has been resized, else false.
        """
        return self.term.width != self._prev_width or self.term.height != self._prev_height

    def clear_screen(self):
        """
        Clears the entire terminal and resets the cursor to the top-left corner.
        """
        print(self.term.home + self.term.clear)
    
    def center_text(self, y: int, text: str, style: str = ""):
        """
        Prints centered text at a given y-coordinate.

        Args:
            y (int): The y-coordinate (row) to print the text on.
            text (str): The text to center and print.
            style (str, optional): blessed style string to apply (e.g. term.bold, term.reverse).
        """
        x = (self.term.width - len(text)) // 2

        if 0 <= y < self.term.height:
            self.buffer.draw_text(x, y, text, style)
    
    def draw_box(self, x: int, y: int, width: int, height: int):
        """
        Draws a box using Unicode line characters at the given location.

        Args:
            x (int): The x-coordinate (column) of the top-left corner of the box.
            y (int): The y-coordinate (row) of the top of the box.
            width (int): The total width of the box.
            height (int): The total height of the box.
        """
        self.buffer.draw_text(x, y, f"╒{'═' * (width - 2)}╕")

        for i in range(1, height):
            self.buffer.draw_text(x, y + i, f"│{' ' * (width - 2)}│")
        
        self.buffer.draw_text(x, y + height, f"╘{'═' * (width - 2)}╛")
    
    def draw_ascii_art(self, ascii_art: str, top_y: int, opaque_style: str, transparent_style: str):
        for i, line in enumerate(ascii_art.strip('\n').splitlines()):
            y = top_y + i

            if y >= self.term.height:
                break

            for j, char in enumerate(line):
                x = (self.term.width - len(line)) // 2 + j

                if 0 <= x < self.term.width:
                    if char in BLOCK_SHADING["opaque"]:
                        self.buffer.draw_text(x, y, char, opaque_style)
                    elif char in BLOCK_SHADING["transparent"]:
                        self.buffer.draw_text(x, y, char, transparent_style)
                    else:
                        self.buffer.draw_text(x, y, char)

    @abstractmethod
    def run(self):
        """
        Runs the menu loop.

        Must be implemented by subclasses to define menu functionality.
        """
        pass