class SpeciesGenerator:
    def __init__(self, species_data):
        self.species_data = species_data
    
    def generate(self, species_index):
        species_info = self.species_data[species_index]
        innate = self.generate_innate(species_info["innates"])
        
        return Species(species_info, innate)
    
    def generate_innate(self):
        return 0