import random
from player.character.innate import Innate
from player.character.species import Species
from util.json_loader import load_json

class SpeciesGenerator:
    def __init__(self, species_data):
        self.species_data = species_data
    
    def generate(self, species_index):
        species_info = self.species_data[species_index]
        innate = self.generate_innate(species_info["innates"])
        return Species(species_info, innate)
    
    def generate_innate(self, innates):
        innate_data = load_json("player", "innates.json")
        innate = random.randint(0, len(innates) - 1)
        return Innate(innate_data[innate]["name"], innate_data[innate]["description"], innate_data[innate]["effect"])