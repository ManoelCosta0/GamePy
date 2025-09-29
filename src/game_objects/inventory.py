import arcade
from src.game_objects.item import Item
from src.views.inventory_view import InventoryView

class Inventory():
    """Classe para gerenciar o inventário do jogador."""
    def __init__(self):
        self.slot_items = []
        self.equipped_items = []

    def add_item(self, inventory_view: InventoryView, item: Item):
        """Adiciona um item ao inventário."""
        self.slot_items.append(item)
        inventory_view.add_item_on_display(item, len(self.slot_items) - 1)

    def remove_item(self, inventory_view: InventoryView, index: int):
        """Remove um item do inventário."""
        self.slot_items.pop(index)
        inventory_view.remove_item_from_display(index)

    def is_on_inventory(self, item: Item) -> bool:
        """Verifica se um item está no inventário."""
        return item in self.slot_items

    def equip_item(self, inventory_view: InventoryView, item: Item):
        """Equipa um item do inventário."""
        if item in self.slot_items:
            self.equipped_items.append(item)
            self.remove_item(inventory_view, item)
            print(f"{item.name} equipado!")
        else:
            print(f"{item.name} não está no inventário!")