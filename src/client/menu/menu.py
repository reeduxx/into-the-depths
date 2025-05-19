from abc import ABC, abstractmethod

class Menu(ABC):
    """
    Abstract base class for the game menus.

    Provides utility methods for tracking resize events, clearing the 
    screen, centering text, and rendering menu borders.
    All derived menus must implement the 'run()' method.

    Attributes:
        term (blessed.Terminal): The terminal instance used for input and display.
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
        Clears the terminal and moves the cursor to the top-left corner.
        """
        print(self.term.home + self.term.clear)
    
    def center_text(self, y: int, text: str):
        """
        Prints centered text at a given y-coordinate.

        Args:
            y (int): The y-coordinate (row) to print the text on.
            text (str): The text to center and print.
        """
        with self.term.location(0, y):
            print(self.term.center(text))
    
    def draw_box(self, x: int, y: int, width: int, height: int):
        """
        Draws a box using Unicode line characters at the given location.

        Args:
            x (int): The x-coordinate (column) of the top-left corner of the box.
            y (int): The y-coordinate (row) of the top of the box.
            width (int): The total width of the box.
            height (int): The total height of the box.
        """
        print(self.term.move_xy(x, y) + f"╒{'═' * (width - 2)}╕")

        for i in range(1, height):
            print(self.term.move_xy(x, y + i) + f"│{' ' * (width - 2)}│")
        
        print(self.term.move_xy(x, y + height) + f"╘{'═' * (width - 2)}╛")
    
    @abstractmethod
    def run(self):
        """
        Runs the menu loop.

        Must be implemented by subclasses to define menu functionality.
        """
        pass