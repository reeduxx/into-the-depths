from dataclasses import dataclass,field
from inventory.itemtype import ItemType
from inventory.weapontype import WeaponType
from player.characterclass import CharacterClass
from typing import Optional, Dict, Any

@dataclass
class Item:
    
    #Represents any findable or equippable item.
    name: str
    item_type: ItemType
    description: str = ""

    #stats that this item provides
    damage: int = 0
    armor_bonus: int = 0
    strength_bonus: int = 0
    dexterity_bonus: int = 0
    intelligence_bonus: int = 0
    constitution_bonus: int = 0

    #Item properties
    stackable: bool = False
    max_stack: int = 1
    value: int = 0
    rarity: str = "common"

    #if its a weapon set the weapon type
    weapon_type: Optional[WeaponType] = None

    #if its a consumable
    consumable_effect: Dict[str, Any] = field(default_factory=dict)

    def can_equip(self, character_class: CharacterClass) ->  bool:

        #check if item you are trying to equip is equppable by your class.
        if self.weapon_type == WeaponType.STAFF and character_class not in [CharacterClass.WARLOCK, CharacterClass.PALADIN]:
            return False
        
        if self.weapon_type == WeaponType.AXE and character_class not in [CharacterClass.BERSERKER, CharacterClass.PALADIN]:
            return False
        
        if self.weapon_type == WeaponType.BOW and character_class not in [CharacterClass.RANGER, CharacterClass.ROGUE]:
            return False
        
        if self.weapon_type == WeaponType.DAGGER and character_class not in [CharacterClass.MERCHANT, CharacterClass.ROGUE]:
            return False
        
        if self.weapon_type == WeaponType.SWORD and character_class not in [CharacterClass.WARLOCK, CharacterClass.BERSERKER, CharacterClass.MERCHANT]:
            return False
        
        return True
    
    def get_total_stats(self) -> Dict[str,int]:
        #get all stat bonuses
        return {
            'damage': self.damage,
            'armor': self.armor_bonus,
            'strength': self.strength_bonus,
            'dexterity': self.dexterity_bonus,
            'intelligence': self.intelligence_bonus,
            'constitution': self.constitution_bonus
        }