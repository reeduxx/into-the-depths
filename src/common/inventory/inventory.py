from typing import Tuple, Optional, Dict, List
from item import Item
from itemtype import ItemType
from inventoryslot import InventorySlot

class Inventory:
    #Manages character inventory with flexible slot system
    
    def __init__(self, size: int = 20):
        self.slots: List[InventorySlot] = [InventorySlot() for _ in range(size)]
        self.size = size
        
        # Equipment slots - separate from main inventory
        self.equipped: Dict[str, Optional[Item]] = {
            'weapon': None,
            'armor': None,
            'shield': None,
            'accessory': None
        }
    
    def add_item(self, item: Item, quantity: int = 1) -> int:
       # Add item to inventory, returns amount actually added
        remaining = quantity
        
        # First, try to add to existing stacks
        if item.stackable:
            for slot in self.slots:
                if slot.item is not None and not slot.is_empty() and slot.item.name == item.name:
                    added = slot.add_item(item, remaining)
                    remaining -= added
                    if remaining == 0:
                        return quantity
        
        # Then try empty slots
        for slot in self.slots:
            if slot.is_empty():
                added = slot.add_item(item, remaining)
                remaining -= added
                if remaining == 0:
                    return quantity
        
        return quantity - remaining  # Return how much we actually added
    
    def remove_item(self, item_name: str, quantity: int = 1) -> int:
        #Remove items by name, returns amount actually removed
        removed = 0
        for slot in self.slots:
            if slot.item is not None and not slot.is_empty() and slot.item.name == item_name:
                _, amount = slot.remove_item(min(quantity - removed, slot.quantity))
                removed += amount
                if removed >= quantity:
                    break
        return removed
    
    def has_item(self, item_name: str, quantity: int = 1) -> bool:
        #Check if inventory contains enough of an item
        total = 0
        for slot in self.slots:
            if slot.item is not None and not slot.is_empty() and slot.item.name == item_name:
                total += slot.quantity
                if total >= quantity:
                    return True
        return False
    
    def get_item_quantity(self, item_name: str) -> int:
        #Get total quantity of an item in inventory
        total = 0
        for slot in self.slots:
            if slot.item is not None and not slot.is_empty() and slot.item.name == item_name:
                total += slot.quantity
        return total
    
    def equip_item(self, slot_index: int) -> bool:
        #Equip item from inventory slot
        if slot_index >= len(self.slots) or self.slots[slot_index].is_empty():
            return False
        
        item = self.slots[slot_index].item
        if item is None:
            return False  # No item to equip
        
        # Determine equipment slot
        equip_slot = None
        if item.item_type == ItemType.WEAPON:
            equip_slot = 'weapon'
        elif item.item_type == ItemType.ARMOR:
            equip_slot = 'armor'
        elif item.item_type == ItemType.SHIELD:
            equip_slot = 'shield'
        elif item.item_type == ItemType.CONSUMABLE:
            equip_slot = 'consumable'
        elif item.item_type == ItemType.KEY:
            equip_slot = 'key'
        else:
            return False  # Can't equip this item type
        
        # Unequip current item if any
        if self.equipped[equip_slot] is not None:
            equipped_item = self.equipped[equip_slot]
            if equipped_item is not None and not self.add_item(equipped_item, 1):
                return False  # No room to unequip
        
        # Equip new item
        self.equipped[equip_slot] = item
        self.slots[slot_index].remove_item(1)
        return True
    
    def unequip_item(self, equip_slot: str) -> bool:
        #Unequip item to inventory
        if equip_slot not in self.equipped or self.equipped[equip_slot] is None:
            return False
        
        item = self.equipped[equip_slot]
        if item is not None and self.add_item(item, 1) > 0:
            self.equipped[equip_slot] = None
            return True
        return False  # No room in inventory
    
    def get_equipped_stats(self) -> Dict[str, int]:
        #Get total stat bonuses from all equipped items
        total_stats = {
            'damage': 0, 'armor': 0, 'strength': 0, 
            'dexterity': 0, 'intelligence': 0, 'constitution': 0
        }
        
        for item in self.equipped.values():
            if item is not None:
                item_stats = item.get_total_stats()
                for stat, value in item_stats.items():
                    total_stats[stat] += value
        
        return total_stats
    
    def list_items(self) -> List[Tuple[str, int, int]]:
        #List all items as (name, quantity, slot_index)
        items = []
        for i, slot in enumerate(self.slots):
            if not slot.is_empty() and slot.item is not None:
                items.append((slot.item.name, slot.quantity, i))
        return items
    
    def get_equipped_items(self) -> Dict[str, Optional[str]]:
        #Get names of equipped items
        return {slot: item.name if item else None for slot, item in self.equipped.items()}