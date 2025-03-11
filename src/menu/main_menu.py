from blessed import Terminal
import time
from art.art import TITLE_ASCII
from config.config import VERSION
from util.util import get_colors

class MainMenu:
    MENU_OPTIONS = ["Continue", "New Game", "Credits ", "Exit"]
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
                f"{translucent_color}{char}{self.term.normal}" if char in self.TRANSLUCENT_BLOCKS else 
                char for char in line
            )))
        
        self.display_version()
    
    def display_version(self):
        version_text = f"v{VERSION}"
        
        with self.term.location(self.term.width - len(version_text) - 1, self.term.height - 1):
            print(version_text)
    '''
    def display_menu(self):
        menu_width = max(len(option) for option in self.MENU_OPTIONS) + 6
        menu_height = len(self.MENU_OPTIONS) * 2 + 2
        box_x = (self.term.width - menu_width) // 2
        box_y = self.menu_start_y - 2
        
        with self.term.location(box_x, box_y):
            print(f"╒{'═' * (menu_width - 2)}╕")
        
        for i, option in enumerate(self.MENU_OPTIONS):
            cursor_y = self.menu_start_y + (i * 2)
            left_padding = (menu_width - len(option) - 2) // 2
            right_padding = menu_width - len(option) - 2 - left_padding
            
            with self.term.location(0, cursor_y):
                print(' ', end='') # Clears the menu item before reprinting to prevent duplication bug
                
                with self.term.location(0, cursor_y):
                    if i == self.selected_index:
                        print(self.term.center(f"│{' ' * left_padding}{self.term.reverse}{option}{self.term.normal}{' ' * right_padding}│"))
                    else:
                        print(self.term.center(f"│{' ' * left_padding}{option}{' ' * right_padding}│"))
        
        with self.term.location(box_x, cursor_y + 2):
            print(f"╘{'═' * (menu_width - 2)}╛")
    '''
    def display_menu(self):
        menu_width = max(len(option) for option in self.MENU_OPTIONS) + 6  # Adds padding
        menu_height = len(self.MENU_OPTIONS) * 2 + 2  # Calculates required height
        box_x = (self.term.width - menu_width) // 2  # Centers the box horizontally
        box_y = self.menu_start_y - 2  # Positions above first option

    # Draw top border
        with self.term.location(box_x, box_y):
            print(f"╒{'═' * (menu_width - 2)}╕")
        
        with self.term.location(box_x, box_y + 1):
            print(f"│{' ' * (menu_width - 2)}│")

    # Draw menu options with side borders
        for i in range(len(self.MENU_OPTIONS) * 2):
            cursor_y = self.menu_start_y + i
            
            if i % 2 == 1:
                with self.term.location(box_x, cursor_y):
                    print(f"│{' ' * (menu_width - 2)}│")
            else:
                option_index = i // 2
                option = self.MENU_OPTIONS[option_index]
                left_padding = (menu_width - len(option) - 2) // 2  # Adjust for side borders
                right_padding = menu_width - len(option) - 2 - left_padding  # Ensures even spacing

                with self.term.location(box_x, cursor_y):
                    if option_index == self.selected_index:
                        option_text = f"│{' ' * left_padding}{self.term.reverse}{option}{self.term.normal}{' ' * right_padding}│"
                    else:
                        option_text = f"│{' ' * left_padding}{option}{' ' * right_padding}│"

                    print(option_text)

        with self.term.location(box_x, cursor_y + 1):
            print(f"╘{'═' * (menu_width - 2)}╛")

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
    