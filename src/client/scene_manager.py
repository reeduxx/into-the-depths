from client.menu.character_creation_menu import CharacterCreationMenu
from client.menu.main_menu import MainMenu

class SceneManager:
    def __init__(self, term, config):
        self.term = term
        self.config = config
    
    def run(self):
        while True:
            menu = MainMenu(self.term, self.config)
            result = menu.run()

            if result == "new_game":
                scene = CharacterCreationMenu(self.term, self.config)
                character = scene.run()
                break
            elif result == "exit":
                break