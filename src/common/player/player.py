class Player:
    def __init__(self, term, name, species, job, stats, curr_hp, level=1, exp=0):
        self.term = term
        self.name = name
        self.species = species
        self.job = job
        self.stats = stats
        self.curr_hp = curr_hp
        self.level = level
        self.exp = exp
        self.max_hp = 10 + stats[2]
    
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
        stats = '\n'.join([str(_) for _ in self.stats])
        
        return f"{self.name}, Lvl {self.level} {self.species.name} {self.cls.name}\n{hp_bar} {hp_text}\n{stats}"