class Species:
    def __init__(self, data):
        self.name = data["name"]
        self.description = data["description"]
        self.passives = data["passives"]
    
    def __str__(self):
        return f"{self.name}\n\n{self.description}"