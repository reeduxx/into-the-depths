import random

def drunken_walk(dungeon, start_x, start_y, steps):
    x, y = start_x, start_y
    
    for _ in range(steps):
        dungeon.grid[y][x] = 0
        direction = random.choice([0, 1, 2, 3])
        
        if direction == 0 and y > 1:
            y -= 1
        elif direction == 1 and y < dungeon.height - 2:
            y += 1
        elif direction == 2 and x > 1:
            x -= 1
        elif direction == 3 and x < dungeon.width - 2:
            x += 1