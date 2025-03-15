import random
from player.character.innate import Innate
from util.json_loader import load_json

class Species:
    def __init__(self, data):
        self.name = data["name"]
        self.description = data["description"]
        self.innate = self.generate_innate(data["innates"])
    
    def generate_innate(self, innates):
        return Innate(random.choice(innates), "TODO")
    
    def __str__(self):
        return f"{self.name}\n{self.description}\n{self.innate}"