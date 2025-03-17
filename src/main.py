from blessed import Terminal
from menu.main_menu import MainMenu

def main():
    term = Terminal()
    menu = MainMenu(term)
    menu.run()
    print(term.clear)

if __name__ == '__main__':
	main()