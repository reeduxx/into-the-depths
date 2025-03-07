from blessed import Terminal
from menu import MainMenu
from player import Player


def main():
    term = Terminal()
    menu = MainMenu(term)
    option = menu.get_selection()
    
    match option:
        case 0:
            print("Continue")
        case 1:
            print("New Game")
        case 2:
            print("Credits")
        case 3:
            print("Exit")
    
    print(term.clear)

if __name__ == '__main__':
	main()