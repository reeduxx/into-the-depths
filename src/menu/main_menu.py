from blessed import Terminal
import os
import sys
import time
from art.art import TITLE_ASCII
from config.config import SAVE_DIR, VERSION
from menu.character_creation_menu import CharacterCreationMenu
from menu.menu import Menu
from player.player import Player
from util.util import get_colors

class MainMenu(Menu):
    MENU_OPTIONS = ["Continue", "New Game", "Credits ", "Exit"]
    
    def __init__(self, term):
        super().__init__(term)
        self.selected_index = 0
        self.first_run = True
        self.menu_max_y = 14
        self.menu_width = max(len(option) for option in self.MENU_OPTIONS) + 6
        self.menu_height = len(self.MENU_OPTIONS) * 2 + 2
    
    def run(self):
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))
        
        while True:
            option = self.get_selection(self.first_run)
            self.first_run = False
            
            match option:
                case 0:
                    if not os.listdir(SAVE_DIR):
                        self.display_message("No saves found.")
                    else:
                        print("Continue") # TODO: Implement save loading
                case 1:
                    character_creation_menu = CharacterCreationMenu(self.term)
                    name, species, cls = character_creation_menu.get_input()
                    player = Player(name, species, cls, self.term)
                    self.first_run = True
                case 2:
                    print("Credits") # TODO: Implement credits screen
                case 3:
                    break
    
    def get_menu_y(self):
        box_start_y = (self.term.height - self.menu_height) // 2
        return max(self.menu_max_y, box_start_y)
    
    def display_menu(self):
        box_x = (self.term.width - self.menu_width) // 2
        box_y = self.get_menu_y()

        with self.term.location(box_x, box_y):
            print(f"╒{'═' * (self.menu_width - 2)}╕")
        
        with self.term.location(box_x, box_y + 1):
            print(f"│{' ' * (self.menu_width - 2)}│")

        for i in range(len(self.MENU_OPTIONS) * 2):
            cursor_y = box_y + i + 2
            
            if i % 2 == 1:
                with self.term.location(box_x, cursor_y):
                    print(f"│{' ' * (self.menu_width - 2)}│")
            else:
                option_index = i // 2
                option = self.MENU_OPTIONS[option_index]
                left_padding = (self.menu_width - len(option) - 2) // 2  # Adjust for side borders
                right_padding = self.menu_width - len(option) - 2 - left_padding  # Ensures even spacing

                with self.term.location(box_x, cursor_y):
                    if option_index == self.selected_index:
                        option_text = f"│{' ' * left_padding}{self.term.reverse}{option}{self.term.normal}{' ' * right_padding}│"
                    else:
                        option_text = f"│{' ' * left_padding}{option}{' ' * right_padding}│"

                    print(option_text)

        with self.term.location(box_x, cursor_y + 1):
            print(f"╘{'═' * (self.menu_width - 2)}╛")
    
    def display_message(self, message):
        self.clear_menu(self.get_menu_y(), self.menu_height)
        with self.term.cbreak(), self.term.hidden_cursor():
            while True:
                message_start_y = max(self.menu_max_y, (self.term.height - 3) // 2)
            
                if self.window_resized():
                    self.display_title()
                
                with self.term.location(0, message_start_y):
                    print(self.term.center(message), end='')
                    
                with self.term.location(0, message_start_y + 2):
                    print(self.term.center("Press any key to continue. . ."), end='')
                    
                key = self.term.inkey(timeout=0.1)
                    
                if key:
                    break
                
        self.clear_menu(self.get_menu_y(), self.menu_height)
    
    def get_selection(self, show_title=True):
        with self.term.cbreak(), self.term.hidden_cursor():
            if show_title:
                self.display_title(TITLE_ASCII)
            
            key_map = {
                self.term.KEY_UP: lambda: setattr(self, 'selected_index', (self.selected_index - 1) % len(self.MENU_OPTIONS)),
                self.term.KEY_DOWN: lambda: setattr(self, 'selected_index', (self.selected_index + 1) % len(self.MENU_OPTIONS))
            }
            
            while True:
                if self.window_resized():
                    self.display_title(TITLE_ASCII)
                
                self.display_menu()
                key = self.term.inkey(timeout=0.1)
                
                if key.code in key_map:
                    key_map[key.code]()
                elif key.code == self.term.KEY_ENTER:
                    return self.selected_index
    