from item import Item
from typing import Optional, Tuple
from dataclasses import dataclass

@dataclass
class InventorySlot:
    #represents a single inventory slot
    item: Optional[Item] = None
    quantity: int = 0

    def is_empty(self) -> bool:
        return self.item is None or self.quantity == 0
    
    def can_add_item(self, item: Item, quantity: int = 1) -> bool:
        if self.is_empty():
            return True
        if self.item is not None and self.item.name == item.name and self.item.stackable:
            return self.quantity + quantity <= self.item.max_stack
        return False
    
    def add_item(self, item: Item, quantity: int = 1) -> int:
        #Add item to slot, returns amount actually added
        if self.is_empty():
            self.item = item
            self.quantity = min(quantity, item.max_stack if item.stackable else 1)
            return self.quantity
        
        if self.item is not None and self.item.name == item.name and self.item.stackable:
            can_add = min(quantity, self.item.max_stack - self.quantity)
            self.quantity += can_add
            return can_add
        
        return 0 
    
    def remove_item(self, quantity: int = 1) -> Tuple:
        if self.is_empty():
            return None, 0
        
        actual_removed = min(quantity, self.quantity)
        removed_item = self.item
        self.quantity -= actual_removed

        if self.quantity == 0:
            self.item = None

        return removed_item, actual_removed
    
    
