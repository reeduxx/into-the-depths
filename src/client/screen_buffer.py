class ScreenBuffer:
    """
    A double-buffered terminal rendering system with character and style diffing.

    Tracks the current and previous frames as 2D buffers of characters and styles,
    allowing efficient and flicker-free rendering by only redrawing changed cells.

    Attributes:
        term (blessed.Terminal): The terminal instance used for input and display.
        width (int): The current width of the terminal.
        height (int): The current height of the terminal.
        previous (list[list[dict]]): The previous frame's buffer.
        current (list[list[dict]]): The current frame's buffer.
    """
    def __init__(self, term):
        """
        Initializes the buffer with an empty screen state.

        Args:
            term (blessed.Terminal): The terminal instance used for input and display.
        """
        self.term = term
        self.width = term.width
        self.height = term.height
        self.previous = self._create_buffer()
        self.current = self._create_buffer()
    
    def _create_buffer(self) -> list:
        """
        Creates a 2D buffer initialized with empty characters and styles.

        Returns:
            list[list[dict]]: A 2D list of dicts with 'char' and 'style' keys.
        """
        return [[{'char': '', 'style': ''} for _ in range(self.width)] for _ in range(self.height)]

    def clear(self):
        """
        Clears the entire terminal, resets the cursor to the top-left corner, and empties both buffers. 
        """
        print(self.term.home + self.term.clear, end='')
        self.previous = self._create_buffer()
        self.current = self._create_buffer()
    
    def draw_text(self, x: int, y: int, text: str, style: str = ""):
        """
        Draws stylized text to the current frame buffer at the given position.

        Args:
            x (int): The x-coordinate (column) to print the text on.
            y (int): The y-coordinate (row) to print the text on.
            text (str): The text to print.
            style (str, optional): blessed style string to apply (e.g. term.bold, term.reverse).
        """
        for i, char in enumerate(text):
            if 0 <= x + i < self.width and 0 <= y < self.height:
                self.current[y][x + i] = {'char': char, 'style': style}
    
    def render(self):
        """
        Compares the previous and current frame buffers, printing only the changed cells.

        Optimized to reduce screen flickering and improve performance by skipping redundant redraws.
        """
        output = []

        for y in range(self.height):
            for x in range(self.width):
                curr = self.current[y][x]
                prev = self.previous[y][x]

                if curr != prev:
                    output.append(self.term.move_xy(x, y) + curr['style'] + curr['char'] + self.term.normal)
                    self.previous[y][x] = curr.copy()
        if output:
            print(''.join(output), end='', flush=True)
    
    def resize(self):
        """
        Reinitializes the buffers to match the new terminal dimensions.
        """
        self.width = self.term.width
        self.height = self.term.height
        self.previous = self._create_buffer()
        self.current = self._create_buffer()