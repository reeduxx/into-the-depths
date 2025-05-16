from blessed import Terminal
import numpy as np
import random
from dungeon.bsp import *
from dungeon.drunken_walk import drunken_walk

class Dungeon:
    def __init__(self, width, height, term=Terminal):
        self.width = width
        self.height = height
        self.term = term
        self.grid = np.ones((height, width), dtype=int)
    
    def print_dungeon(self):
        for row in self.grid:
            print(''.join(['#' if cell else '.' for cell in row]))

def generate_dungeon(width, height, min_size, drunken_walk_steps):
    dungeon = Dungeon(width, height)
    root = BSPNode(0, 0, width, height)
    generate_bsp(root, min_size)
    create_rooms(root, dungeon)
    connect_rooms(root, dungeon)
    '''
    for _ in range(5):
        start_x, start_y = random.randint(0, width - 1), random.randint(0, height - 1)
        drunken_walk(dungeon, start_x, start_y, drunken_walk_steps)
    '''
    return dungeon
    