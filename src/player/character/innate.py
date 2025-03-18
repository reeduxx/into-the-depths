class Innate:
    def __init__(self, name, description, effect):
        self.name = name
        self.description = description
        self.modifier = effect
    
    def __str__(self):
        return f"- {self.name}: {self.description}"