import random

class BSPNode:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.left = None
        self.right = None
        self.room = None
    
    def split(self, min_size):
        if self.left or self.right:
            return False
        
        horizontal = random.choice([True, False])
        
        if horizontal:
            if self.height < min_size * 2:
                return False
            
            split = random.randint(min_size, self.height - min_size)
            self.left = BSPNode(self.x, self.y, self.width, split)
            self.right = BSPNode(self.x, self.y + split, self.width, self.height - split)
        else:
            if self.width < min_size * 2:
                return False
            
            split = random.randint(min_size, self.width - min_size)
            self.left = BSPNode(self.x, self.y, split, self.height)
            self.right = BSPNode(self.x + split, self.y, self.width - split, self.height)
    
        return True

def generate_bsp(root, min_size):
    nodes = [root]
    
    while nodes:
        node = nodes.pop()
        
        if node.split(min_size):
            nodes.append(node.left)
            nodes.append(node.right)

def create_rooms(root, dungeon):
    if root.left or root.right:
        if root.left:
            create_rooms(root.left, dungeon)
        if root.right:
            create_rooms(root.right, dungeon)
    else:
        room_x = root.x + random.randint(1, root.width // 4)
        room_y = root.y + random.randint(1, root.width // 4)
        room_w = root.width - (room_x - root.x)
        room_h = root.height - (room_y - root.y)
        
        for y in range(room_y, room_y + room_h):
            for x in range(room_x, room_x + room_w):
                dungeon.grid[y][x] = 0
        
        root.room = (room_x, room_y, room_w, room_h)

def connect_rooms(root, dungeon):
    if root.left and root.right:
        left_room = root.left.room
        right_room = root.right.room
        
        if left_room and right_room:
            lx, ly = left_room[0] + left_room[2] // 2, left_room[1] + left_room[3] // 2
            rx, ry = right_room[0] + right_room[2] // 2, right_room[1] + right_room[3] // 2
            
            while lx != rx:
                dungeon.grid[ly][lx] = 0
                lx += 1 if lx < rx else -1
            
            while ly != ry:
                dungeon.grid[ly][lx] = 0
                ly += 1 if ly < ry else -1
        
        connect_rooms(root.left, dungeon)
        connect_rooms(root.right, dungeon)