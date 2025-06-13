from dataclasses import dataclass, field
from characterclass import CharacterClass
from species import Species
from inventory.item import Item
from inventory.inventoryslot import InventorySlot
from inventory.inventory import Inventory
from inventory.itemtype import ItemType
from inventory.weapontype import WeaponType
import pickle
from typing import Dict

@dataclass
class Character:
    """Represents a player character with persistent attributes"""
    
    name: str
    character_class: CharacterClass
    character_species: Species
    level: int = 1
    
    # Core stats
    strength: int = 10
    dexterity: int = 10
    intelligence: int = 10
    constitution: int = 10
    wisdom: int = 10
    
    # Derived stats (calculated from core stats + equipment)
    max_health: int = field(init=False)
    current_health: int = field(init=False)
    base_armor_class: int = field(init=False)
    
    # Inventory system
    inventory: Inventory = field(default_factory=lambda: Inventory(20))
    
    # Skills - dictionary mapping skill names to levels
    skills: Dict[str, int] = field(default_factory=lambda: {
        'melee_combat': 1,
        'ranged_combat': 1,
        'magic': 1,
        'stealth': 1,
        'lockpicking': 1
    })
    
    # Character appearance/flavor
    description: str = ""
    
    def __post_init__(self):
        """Calculate derived stats after initialization"""
        self._calculate_base_stats()
        self._give_starting_equipment()
    
    def _calculate_base_stats(self):
        """Calculate base stats without equipment bonuses"""
        # Base health calculation
        self.max_health = 20 + (self.constitution * 2) + (self.level * 5)
        self.current_health = self.max_health
        
        # Base armor class calculation
        self.base_armor_class = 10 + (self.dexterity // 2)
        
        #attribute bonuses
        """
        Berserker (Strength focused)
        Ranger (Dexterity focused)
        Paladin (Constitution focused)
        Warlock (Intelligence focused)
        Rogue (Wisdom focused)
        Merchant (Charisma focused)
        """
        # Apply class bonuses
        if self.character_class == CharacterClass.BERSERKER:
            self.strength += 5
            self.base_armor_class += 2

        elif self.character_class == CharacterClass.RANGER:
            self.dexterity += 7

        elif self.character_class == CharacterClass.PALADIN:
            self.constitution += 7

        elif self.character_class == CharacterClass.WARLOCK:
            self.max_health -= 5
            self.intelligence += 10
    
        elif self.character_class == CharacterClass.ROGUE:
            self.base_armor_class += 1
            self.wisdom += 5

    #TODO implement species bonuses here. need some discussion about those.
    
    def _give_starting_equipment(self):
        """Give character starting equipment based on class"""
        starting_items = []
        
        if self.character_class == CharacterClass.BERSERKER:
            starting_items = [
                Item("Rusted Axe", ItemType.WEAPON, "A sturdy, rusty axe", 
                     damage=8, weapon_type=WeaponType.SWORD),
                Item("Chain Mail", ItemType.ARMOR, "Flexible metal armor", 
                     armor_bonus=5, constitution_bonus=2),
                Item("Health Potion", ItemType.CONSUMABLE, "Restores 25 HP", 
                     stackable=True, max_stack=10,
                     consumable_effect={'heal': 25})
            ]
        elif self.character_class == CharacterClass.ROGUE:
            starting_items = [
                Item("Steel Dagger", ItemType.WEAPON, "A sharp, quick blade", 
                     damage=6, dexterity_bonus=2, weapon_type=WeaponType.DAGGER),
                Item("Leather Armor", ItemType.ARMOR, "Light, flexible armor", 
                     armor_bonus=3, dexterity_bonus=1),
                Item("Lockpick Set", ItemType.CONSUMABLE, "Tools for opening locks", 
                     stackable=True, max_stack=5)
            ]
        elif self.character_class == CharacterClass.WARLOCK:
            starting_items = [
                Item("Wooden Staff", ItemType.WEAPON, "A simple magic staff", 
                     damage=4, intelligence_bonus=3, weapon_type=WeaponType.STAFF),
                Item("Mage Robes", ItemType.ARMOR, "Robes that enhance magic", 
                     armor_bonus=2, intelligence_bonus=2),
                Item("Mana Potion", ItemType.CONSUMABLE, "Restores magic energy", 
                     stackable=True, max_stack=10,
                     consumable_effect={'mana': 20})
            ]
        elif self.character_class == CharacterClass.PALADIN:
            starting_items = [
                Item("Holy Mace", ItemType.WEAPON, "A blessed weapon", 
                     damage=7, constitution_bonus=1, weapon_type=WeaponType.AXE),
                Item("Blessed Robes", ItemType.ARMOR, "Robes blessed by the gods", 
                     armor_bonus=4, constitution_bonus=1),
                Item("Healing Herb", ItemType.CONSUMABLE, "Natural healing", 
                     stackable=True, max_stack=15,
                     consumable_effect={'heal': 15})
            ]
        elif self.character_class == CharacterClass.RANGER:
            starting_items = [
                Item("Rough hewn bow", ItemType.WEAPON, "A poorly made bow", 
                     damage=4, dexterity_bonus=2, weapon_type=WeaponType.BOW),
                Item("Leather Armour", ItemType.ARMOR, "Robes clad in leather and armour", 
                     armor_bonus=2, constitution_bonus=1),
                Item("", ItemType.CONSUMABLE, "Natural healing", 
                     stackable=True, max_stack=15,
                     consumable_effect={'heal': 15})
            ]

        elif self.character_class == CharacterClass.MERCHANT:
            starting_items = [
                Item("Gem dagger", ItemType.WEAPON, "A mysterious dagger", 
                     damage=6, dexterity_bonus=1, weapon_type=WeaponType.DAGGER),
                Item("Pompous Garb", ItemType.ARMOR, "A decadent red and gold robe", 
                     armor_bonus=2, constitution_bonus=1),
                Item("Healing Herb", ItemType.CONSUMABLE, "Natural healing", 
                     stackable=True, max_stack=15,
                     consumable_effect={'heal': 15})
            ]
        
        # Add starting items to inventory
        for item in starting_items:
            if item.item_type in [ItemType.WEAPON, ItemType.ARMOR]:
                # Add to inventory first, then auto-equip
                self.inventory.add_item(item, 1)
                # Find the slot we just added it to and equip it
                for i, slot in enumerate(self.inventory.slots):
                    if slot.item is not None and not slot.is_empty() and slot.item.name == item.name:
                        self.inventory.equip_item(i)
                        break
            else:
                # Just add consumables and misc items
                quantity = 3 if item.stackable else 1
                self.inventory.add_item(item, quantity)
    
    def get_current_stats(self) -> Dict[str, int]:
        """Get current stats including equipment bonuses"""
        equipment_stats = self.inventory.get_equipped_stats()
        
        return {
            'strength': self.strength + equipment_stats['strength'],
            'dexterity': self.dexterity + equipment_stats['dexterity'],
            'intelligence': self.intelligence + equipment_stats['intelligence'],
            'constitution': self.constitution + equipment_stats['constitution'],
            'armor_class': self.base_armor_class + equipment_stats['armor'],
            'damage': equipment_stats['damage'],
            'max_health': self.max_health,
            'current_health': self.current_health
        }
    
    def get_skill_level(self, skill_name: str) -> int:
        """Get the level of a specific skill"""
        return self.skills.get(skill_name, 0)
    
    def pickup_item(self, item: Item, quantity: int = 1) -> bool:
        """Try to pick up an item from the world"""
        added = self.inventory.add_item(item, quantity)
        return added > 0
    
    def use_consumable(self, item_name: str) -> bool:
        """Use a consumable item"""
        if not self.inventory.has_item(item_name, 1):
            return False
        
        # Find the item to get its effects
        item = None
        for slot in self.inventory.slots:
            if slot.item is not None and not slot.is_empty() and slot.item.name == item_name:
                item = slot.item
                break
        
        if item and item.item_type == ItemType.CONSUMABLE:
            # Apply effects
            effects = item.consumable_effect
            if 'heal' in effects:
                self.current_health = min(self.max_health, 
                                        self.current_health + effects['heal'])
            
            # Remove the item
            self.inventory.remove_item(item_name, 1)
            return True
        
        return False
    
    def serialize(self) -> bytes:
        """Serialize character data for network transmission"""
        return pickle.dumps(self.__dict__)
    
    @classmethod
    def deserialize(cls, data: bytes) -> 'Character':
        """Deserialize character data from network"""
        char_dict = pickle.loads(data)
        char = cls.__new__(cls)
        char.__dict__.update(char_dict)
        return char
    
    def save_to_file(self, filename: str):
        """Save character to file"""
        with open(filename, 'wb') as f:
            pickle.dump(self.__dict__, f)
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'Character':
        """Load character from file"""
        with open(filename, 'rb') as f:
            char_dict = pickle.load(f)
        char = cls.__new__(cls)
        char.__dict__.update(char_dict)
        return char
