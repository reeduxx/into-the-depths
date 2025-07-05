import random

class StatsGenerator:
    stat_names = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    
    def __init__(self, class_data, base_stat_range=(3, 8)):
        self.class_data = class_data
        self.base_stat_range = base_stat_range
    
    def generate(self, class_index):
        stats = [
            random.randint(*self.base_stat_range),
            random.randint(*self.base_stat_range),
            random.randint(*self.base_stat_range),
            random.randint(*self.base_stat_range),
            random.randint(*self.base_stat_range),
            random.randint(*self.base_stat_range)
        ]
        
        for i, stat_name in enumerate(self.stat_names):
            if stat_name in self.class_data[class_index]["stats"]:
                stats[i] += random.randint(*self.class_data[class_index]["stats"][stat_name])
        
        return stats