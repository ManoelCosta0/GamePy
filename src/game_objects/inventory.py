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
        if self.is_on_inventory(item) and item.stack_limit > 1:
            self.slot_items[self.find_item_index(item)].stack += 1
            print(f"Adicionou mais uma unidade de {item.name}. Total: {self.slot_items[self.find_item_index(item)].stack}")
        else:
            self.slot_items.append(item)
            inventory_view.add_item_on_display(item, len(self.slot_items) - 1)

    def remove_item(self, inventory_view: InventoryView, index: int):
        """Remove um item do inventário."""
        self.slot_items.pop(index)
        inventory_view.restructure_slots()

    def is_on_inventory(self, item: Item) -> bool:
        """Verifica se um item está no inventário."""
        for items in self.slot_items:
            if items.name == item.name:
                return True 
        return False

    def find_item_index(self, item: Item) -> int:
        for index, current_item in enumerate(self.slot_items):
            if current_item.name == item.name:
                return index
        return -1

    def equip_item(self, inventory_view: InventoryView, item: Item, index: int):
        """Equipa um item do inventário."""
        if item in self.slot_items:
            self.equipped_items.append(item)
            self.remove_item(inventory_view, index)
            print(f"{item.name} equipado!")
        else:
            print(f"{item.name} não está no inventário!")
    
    def unequip_item(self, inventory_view: InventoryView, item: Item):
        """Desequipa um item."""
        if item in self.equipped_items:
            self.equipped_items.remove(item)
            self.add_item(inventory_view, item)
            print(f"{item.name} desequipado!")
        else:
            print(f"{item.name} não está equipado!")