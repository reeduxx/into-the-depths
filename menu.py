from blessed import Terminal
from art import TITLE_ASCII
from config import VERSION
from util import get_colors

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
                print("  " * self.term.width, end='') # Clears the menu item before reprinting to prevent duplication bug
                
                with self.term.location(0, cursor_y):
                    if i == self.selected_index:
                        print(self.term.center(self.term.reverse + option + self.term.normal), end='')
                    else:
                        print(self.term.center(option), end='')
    
    def get_selection(self):
        with self.term.cbreak(), self.term.hidden_cursor():
            self.display_title()
            
            while True:
                self.display_menu()
                key = self.term.inkey(0.1)
                
                if key.code == self.term.KEY_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.MENU_OPTIONS)
                elif key.code == self.term.KEY_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.MENU_OPTIONS)
                elif key.code == self.term.KEY_ENTER:
                    return self.selected_index
    