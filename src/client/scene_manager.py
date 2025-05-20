from client.menu.main_menu import MainMenu

class SceneManager:
    def __init__(self, term):
        self.term = term
    
    def run(self):
        while True:
            menu = MainMenu(self.term)
            result = menu.run()

            if result == "new_game":
                """
                scene = ChracterCreationScene(self.term)
                character = scene.run()
                """
                break
            elif result == "exit":
                break