from blessed import Terminal
from config.config import VERSION
from util.util import get_colors

class Menu:
    OPAQUE_BLOCKS = {'█', '▌', '▀', '▄'}
    TRANSLUCENT_BLOCKS = {'▓', '▒', '░'}
    
    def __init__(self, term: Terminal):
        self.term = term
        self.window_width = self.term.width
        self.window_height = self.term.height
    
    def display_title(self, title, version=True):
        opaque_color, translucent_color = get_colors(self.term)
        print(self.term.home + self.term.clear)
        
        for line in title.splitlines():
            print(self.term.center(''.join(
                f"{opaque_color}{char}{self.term.normal}" if char in self.OPAQUE_BLOCKS else
                f"{translucent_color}{char}{self.term.normal}" if char in self.TRANSLUCENT_BLOCKS else
                char for char in line
            )))
        
        if version:
            self.display_version()
    
    def display_version(self):
        version_text = f"v{VERSION}"
        
        with self.term.location(self.term.width - len(version_text) - 1, self.term.height - 1):
            print(version_text)
    
    def clear_menu(self, menu_start_y, menu_height):
        for i in range(menu_height + 3):
            with self.term.location(0, (menu_start_y - 2) + i):
                print(' ' * self.term.width, end='')
    
    def window_resized(self):
        if self.term.width != self.window_width or self.term.height != self.window_height:
            self.window_width, self.window_height = self.term.width, self.term.height
            return True
        return False