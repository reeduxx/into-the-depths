from blessed import Terminal
from menu.main_menu import MainMenu
from dungeon.dungeon import generate_dungeon

def main():
    term = Terminal()
    menu = MainMenu(term)
    menu.run()
    print(term.clear)
    '''
    dungeon = generate_dungeon(40, 25, min_size=6, drunken_walk_steps=20)
    dungeon.print_dungeon()
    '''

if __name__ == '__main__':
	main()