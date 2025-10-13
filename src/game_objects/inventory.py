import arcade
from src.game_objects.item import Item

class Inventory():
    """Classe para gerenciar o inventário do jogador."""
    def __init__(self):
        self.items = []
        self.inventory_view = arcade.get_window().inventory_view

    def add_item(self, item: Item):
        """Adiciona um item ao inventário."""
        if item.stack_limit > 1 and self.find_item(item.name) is not None:
            self.items[self.find_item(item.name)].stack += 1
        else:
            self.items.append(item)
            self.inventory_view.add_item_to_grid(item)

    def remove_item(self, item: Item):
        """Remove um item do inventário."""
        self.items.remove(item)

    def find_item(self, name: str) -> int:
        """Verifica se um item está no inventário."""
        for item in self.items:
            if item.name == name:
                return item 
        return None
    
    def get_items(self):
        return self.items

    def load_inventory(self, items_data: list):
        """Carrega o inventário a partir de uma lista de dados de itens."""
        self.items = [Item(item) for item in items_data]