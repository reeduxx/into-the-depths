import textwrap

class Species:
    def __init__(self, species_data, innate):
        self.name = species_data["name"]
        self.description = species_data["description"]
        self.innate = innate
    
    def __str__(self, wrap_width):
        wrapped_description = '\n'.join(textwrap.fill(self.description, width=wrap_width).split('\n'))
        return f"{self.name}\n{wrapped_description}\n{self.innate}"