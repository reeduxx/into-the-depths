class Innate:
    def __init__(self, name, description, modifier):
        self.name = name
        self.description = description
        self.modifier = modifier
    
    def __str__(self):
        return f"- {self.name}: {self.description}"