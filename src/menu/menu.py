from blessed import Terminal
import time
from art.title import TITLE_ASCII
from config.config import VERSION
from util.util import get_colors

class MainMenu:
    MENU_OPTIONS = ["Continue", "New Game", "Credits", "Exit"]
    OPAQUE_BLOCKS = {'█', '▌', '▀', '▄'}
    TRANSLUCENT_BLOCKS = {'▓', '▒', '░'}
    
    def __init__(self, term):
        self.term = term
        self.selected_index = 0
        self.menu_start_y = 14
    
    def display_title(self):
        opaque_color, translucent_color = get_colors(self.term)
        print(self.term.home + self.term.clear)
        
        for line in TITLE_ASCII.splitlines():
            print(self.term.center(''.join(
                f"{opaque_color}{char}{self.term.normal}" if char in self.OPAQUE_BLOCKS else
                f"{translucent_color}{char}{self.term.normal}" if char in self.TRANSLUCENT_BLOCKS else char
                for char in line
            )))
        
        self.display_version()
    
    def display_version(self):
        version_text = f"v{VERSION}"
        
        with self.term.location(self.term.width - len(version_text) - 1, self.term.height - 1):
            print(version_text)
    
    def display_menu(self):
        print('\n')
        
        for i, option in enumerate(self.MENU_OPTIONS):
            cursor_y = self.menu_start_y + (i * 2)
            
            with self.term.location(0, cursor_y):
                print(' ', end='') # Clears the menu item before reprinting to prevent duplication bug
                
                with self.term.location(0, cursor_y):
                    if i == self.selected_index:
                        print(self.term.center(self.term.reverse + option + self.term.normal), end='')
                    else:
                        print(self.term.center(option), end='')
    
    def display_message(self, message):
        blinking = True
        start_time = time.time()
        
        for i in range(len(self.MENU_OPTIONS) * 2 + 2):
            with self.term.location(0, self.menu_start_y + i):
                print(' ' * self.term.width, end='')
        
        with self.term.location(0, self.menu_start_y + 2):
            print(self.term.center(message), end='')
        
        with self.term.location(0, self.menu_start_y + 4):
            print(self.term.center("Press any key to continue. . ."), end='')
        
        with self.term.cbreak():
            self.term.inkey()
    
    def get_selection(self, show_title=True):
        with self.term.cbreak(), self.term.hidden_cursor():
            prev_width, prev_height = self.term.width, self.term.height
            
            if show_title:
                self.display_title()
            
            key_map = {
                self.term.KEY_UP: lambda: setattr(self, 'selected_index', (self.selected_index - 1) % len(self.MENU_OPTIONS)),
                self.term.KEY_DOWN: lambda: setattr(self, 'selected_index', (self.selected_index + 1) % len(self.MENU_OPTIONS))
            }
            
            while True:
                if self.term.width != prev_width or self.term.height != prev_height:
                    prev_width, prev_height = self.term.width, self.term.height
                    self.display_title()
                
                self.display_menu()
                key = self.term.inkey(timeout=0.1)
                
                if key.code in key_map:
                    key_map[key.code]()
                elif key.code == self.term.KEY_ENTER:
                    return self.selected_index
    