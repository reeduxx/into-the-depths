from blessed import Terminal
from client.scene_manager import SceneManager

def main():
    term = Terminal()
    print(term.home + term.clear)
    scene_manager = SceneManager(term)
    scene_manager.run()
    print(term.home + term.clear)

if __name__ == '__main__':
    main()