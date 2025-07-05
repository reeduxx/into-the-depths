from client.menu.character_creation_menu import CharacterCreationMenu
from client.menu.main_menu import MainMenu
from client.menu.multiplayer_menu import MultiplayerMenu
from client.menu.join_menu import JoinMenu

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

            if result == "multiplayer":
                scene = MultiplayerMenu(self.term, self.config)
                choice = scene.run()
                if choice == "join":
                    scene = JoinMenu(self.term, self.config)
                    scene.run()
                if choice == "host":
                    pass

            if result == "exit":
                break