import unittest
from .inventory import Inventory
from .item import Item
from .itemtype import ItemType

class InventoryTests(unittest.TestCase):

    def setUp(self):
        self.health_potion = Item(name="Banana of truth", item_type=ItemType.CONSUMABLE, stackable=True, max_stack=5)
        self.sword = Item(name="Iron Sword", item_type=ItemType.WEAPON, stackable=True, max_stack=1)
        self.inv = Inventory(size=7)

    def test_add_item(self):
        self.assertEqual(self.inv.get_total_items(), 0)
        self.inv.add_item(self.health_potion)
        self.assertEqual(self.inv.get_total_items(), 1)
        self.inv.add_item(self.sword)
        self.assertEqual(self.inv.get_total_items(), 2)

    def test_remove_item(self):
        self.inv.add_item(self.health_potion)
        self.inv.add_item(self.sword)
        self.assertEqual(self.inv.get_total_items(), 2)
        self.inv.remove_item("Iron Sword")
        self.assertEqual(self.inv.get_total_items(), 1)

    def test_has_item(self):
        self.inv.add_item(self.health_potion)
        self.assertTrue(self.inv.has_item("Banana of truth"))
        self.assertFalse(self.inv.has_item("Iron Sword"))

    def test_get_item_quantity(self):
        self.inv.add_item(self.health_potion, 2)
        self.assertEqual(self.inv.get_item_quantity("Banana of truth"), 2)
        self.assertEqual(self.inv.get_item_quantity("Iron Sword"), 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
