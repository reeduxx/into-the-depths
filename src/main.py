from blessed import Terminal
from client.menu.main_menu import MainMenu

def main():
    term = Terminal()
    print(term.clear)
    main_menu = MainMenu(term)
    main_menu.run()

if __name__ == '__main__':
    main()