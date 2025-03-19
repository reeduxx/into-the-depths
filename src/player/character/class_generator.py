import random
from player.character.player_class import Class

class ClassGenerator:
    def __init__(self, class_data):
        self.class_data = class_data
    
    def generate(self, class_index):
        cls = self.class_data[class_index]
        
        return Class(cls)