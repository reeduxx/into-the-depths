from blessed import Terminal

class Player:
    def __init__(self, name, species, passive, term, stats=[]):
        self.term = term
        self.name = name
        self.species = species
        self.passive = passive
        self.level = 1
        self.exp = 0
        self.max_hp = 10
        self.curr_hp = self.max_hp
        self.stats = stats
	
    def __str__(self):
        hp_segments = 10 # HP bar represented by 10 blocks
        hp_ratio = self.curr_hp / self.max_hp
        filled_segments = round(hp_ratio * hp_segments)
        empty_segments = hp_segments - filled_segments
        '''
        HP bar is:
        Green if HP >= 70%
        Yellow if 70% > HP >= 40%
        Orange if 40% > HP >= 20%
        Red if HP < 20%
        '''
        hp_color = self.term.green if hp_ratio >= 0.7 else self.term.yellow if hp_ratio >= 0.4 else self.term.orange if hp_ratio >= 0.2 else self.term.red
        hp_bar = f"[{hp_color}{'█' * filled_segments}{self.term.normal}{'▒' * empty_segments}]"
        hp_text = f"{self.curr_hp}/{self.max_hp}"
        
        return f"[{self.level}] {self.name}\n{hp_bar} {hp_text}"