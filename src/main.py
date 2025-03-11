from blessed import Terminal
import os
import sys
from config.config import SAVE_DIR
from menu.character_creation_menu import CharacterCreationMenu
from menu.main_menu import MainMenu
from player.player import Player

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

def main():
    first_run = True
    term = Terminal()
    menu = MainMenu(term)
    
    while True:
        option = menu.get_selection(first_run)
        first_run = False
        
        if option == 0:
            if not os.listdir(SAVE_DIR):
                menu.display_message("No saves found.")
            else:
                print("Continue")
        
        if option == 1:
            character_creation_menu = CharacterCreationMenu(term)
            name = character_creation_menu.display_menu()
            player = Player(name, term)
            print(player)
            first_run = True
        
        if option == 2:
            print("Credits")
        
        if option == 3:
            break
    
    print(term.clear)

if __name__ == '__main__':
	main()