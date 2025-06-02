from client.menu.menu import Menu
from client.util import load_ascii_art
from common import __version__

class MainMenu(Menu):
    """
    Class for the game's main menu.

    Attributes:
        theme (str): The theme of the menu (dark or light).
        selected_index (int): The index of the menu item the user has selected.
        ascii_art (str): The ASCII art to display at the top of the menu.
        menu_width (int): The total width of the menu.
        menu_height (int): The total height of the menu.
    """
    MENU_OPTIONS = ["Continue", "New Game", "Multiplayer", "Credits", "Exit"]

    def __init__(self, term, config):
        """
        Initializes the MainMenu with a terminal instance.

        args:
            term (blessed.Terminal): The terminal instance used for input and display.
            config (dict): The game configuration.
        """
        super().__init__(term)
        self.config = config
        self.theme = self.config.get("theme", "auto")
        self.selected_index = 0
        self.ascii_art = load_ascii_art("assets/title.txt")
        self.menu_width = max(len(opt) for opt in self.MENU_OPTIONS) + 6
        self.menu_height = len(self.MENU_OPTIONS) * 2 + 2
    
    def run(self) -> str:
        """
        Executes the main loop for the menu.

        Handles window resizing, rendering, input listening, and selection logic.

        Returns:
            str: The selected menu option (lowercase, spaces replaced with underscores).
        """
        with self.term.cbreak(), self.term.hidden_cursor():
            self.buffer.clear()

            while True:
                if self.window_resized():
                    self._prev_width, self._prev_height = self.term.width, self.term.height
                    self.buffer.resize()
                    self.buffer.clear()
                
                self.display_menu()
                self.buffer.render()
                
                key = self.term.inkey(timeout=0.1)
                key_map = self.get_key_map()

                if key.code in key_map:
                    key_map[key.code]()
                    self._menu_dirty = True
                elif key.code == self.term.KEY_ENTER:
                    return self.MENU_OPTIONS[self.selected_index].lower().replace(' ', '_')
    
    def display_menu(self):
        """
        Renders the menu options using the double buffer.

        Draws a border surrounding the options, the options themselves, and 
        highlights the selected option.
        """
        x = (self.term.width - self.menu_width) // 2
        y = max(12, (self.term.height - self.menu_height) // 2)
        opaque_color = self.term.white if self.theme == "dark" or self.theme == "auto" else self.term.black
        transparent_color = self.term.red if self.theme == "dark" or self.theme == "auto" else self.term.green
        self.draw_ascii_art(self.ascii_art, 1, opaque_color, transparent_color)
        self.draw_box(x, y, self.menu_width, self.menu_height)

        for i, option in enumerate(self.MENU_OPTIONS):
            line_y = y + 2 + (i * 2)
            pad_left = (self.menu_width - len(option) - 2) // 2
            pad_right = self.menu_width - len(option) - 2 - pad_left
            style = self.term.reverse if i == self.selected_index else ''
            self.buffer.draw_text(x + 1, line_y, ' ' * pad_left)

            if i == self.selected_index:
                self.buffer.draw_text(x + 1 + pad_left, line_y, option, style=self.term.reverse)
            else:
                self.buffer.draw_text(x + 1 + pad_left, line_y, option)
            
            self.buffer.draw_text(x + 1 + pad_left + len(option), line_y, ' ' * pad_right)
            self.buffer.draw_text(self.term.width - len(__version__), self.term.height - 1, __version__)

    def get_key_map(self) -> dict:
        """
        Returns a dictionary mapping directional key codes to menu navigation logic.

        Returns:
            dict: A mapping of terminal key codes to lambda functions that move the selection.
        """
        return {
            self.term.KEY_UP: lambda: self._move_selection(-1),
            self.term.KEY_DOWN: lambda: self._move_selection(1)
        }

    def _move_selection(self, delta):
        """
        Moves the selection up or down in the menu.

        Args:
            delta (int): The direction to move (-1 is up, 1 is down).
        """
        self.selected_index = (self.selected_index + delta) % len(self.MENU_OPTIONS)