from blessed import Terminal
from client.scene_manager import SceneManager
from client.util import load_config
from time import sleep

def main():
    term = Terminal()
    config = load_config("config/config.toml")
    print(term.home + term.clear)
    scene_manager = SceneManager(term, config)
    scene_manager.run()
    print(term.home + term.clear)

if __name__ == '__main__':
    main()