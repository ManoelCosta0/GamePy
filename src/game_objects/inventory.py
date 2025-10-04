import arcade
from src.game_objects.item import Item

class Inventory():
    """Classe para gerenciar o inventário do jogador."""
    def __init__(self):
        self.slot_items = []
        self.equipped_items = []

    def add_item(self, item: Item):
        """Adiciona um item ao inventário."""
        if self.is_on_inventory(item) and item.stack_limit > 1:
            self.slot_items[self.find_item_index(item)].stack += 1
            print(f"Adicionou mais uma unidade de {item.name}. Total: {self.slot_items[self.find_item_index(item)].stack}")
        else:
            self.slot_items.append(item)

    def remove_item(self, index: int):
        """Remove um item do inventário."""
        self.slot_items.pop(index)

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

    def equip_item(self, item: Item, index: int):
        """Equipa um item do inventário."""
        if item in self.slot_items:
            self.equipped_items.append(item)
            self.remove_item(index)
        else:
            print(f"{item.name} não está no inventário!")

    def unequip_item(self, item: Item):
        """Desequipa um item."""
        if item in self.equipped_items:
            self.equipped_items.remove(item)
            self.add_item(item)
        else:
            print(f"{item.name} não está equipado!")