class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.exp = 0
        self.curr_hp = self.max_hp = 100
	
    def __str__(self):
        return f"[{self.level}] {self.name}"