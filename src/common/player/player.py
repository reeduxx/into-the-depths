class Player:
    def __init__(self, name, level=1):
        self.name = name
        self.level = 1
    
    def __str__(self):
        return f"{self.name}\nLvl {self.level}"