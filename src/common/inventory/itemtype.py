from enum import Enum

#used when creating items from the Item class.
#Designates what type of item it is which tells our inventory how to sort it out.

class ItemType(Enum):
    WEAPON = 'weapon'
    ARMOR = 'armor'
    SHIELD = 'shield'
    CONSUMABLE = 'consumable'
    KEY = 'key'
