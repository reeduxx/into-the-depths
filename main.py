from blessed import Terminal
from menu import MainMenu
from player import Player

def main():
    term = Terminal()
    menu = MainMenu(term)
    option = menu.get_selection()

if __name__ == '__main__':
	main()