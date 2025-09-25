import arcade
from src.game_objects.item import Item

class Inventory():
    """Classe para gerenciar o inventário do jogador."""
    def __init__(self):
        self.items = []

    def add_item(self, item: Item):
        """Adiciona um item ao inventário."""
        self.items.append(item)

    def remove_item(self, item: Item):
        """Remove um item do inventário."""
        if item in self.items:
            self.items.remove(item)
    
    def remove_item(self, item: Item, length: int):
        """Remove um item empilhado do inventário."""
        if item in self.items:
            item.length -= length
            if item.length <= 0:
                self.items.remove(item)

    def is_on_inventory(self, item: Item) -> bool:
        """Verifica se um item está no inventário."""
        return item in self.items