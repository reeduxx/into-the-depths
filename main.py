from blessed import Terminal
import os
from config import SAVE_DIR
from menu import MainMenu
from player import Player


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
            print("New Game")
        
        if option == 2:
            print("Credits")
        
        if option == 3:
            break
    
    print(term.clear)

if __name__ == '__main__':
	main()