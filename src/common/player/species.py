"""
Drakari (Similar to DND Dragonborn or MTG Viashino)
Dwarf
High Elf
Gnome
Half-Giant
Hellkin (Similar to DND Tiefling)
Human
Myconid (Mushroom person)
Night Elf
Orc
Revenant (Zombie)
Voidborn
Wood Elf
"""

from enum import Enum

class Species(Enum):
    DWARF = 'dwarf'
    HIGHELF = 'highelf'
    GNOME = 'gnome'
    HALFGIANT = 'halfgiant'
    HELLKIN = 'hellkin'
    HUMAN = 'human'
    MYCONID = 'myconid'
    NIGHTELF = 'nightelf'
    ORC = 'orc'
    REVENANT = 'revenant'
    VOIDBORN = 'voidborn'
    WOODELF = 'woodelf'