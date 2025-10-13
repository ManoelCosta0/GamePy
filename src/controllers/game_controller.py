import arcade
#from src.game_objects.player import Player
#from src.views.game_view import GameView
from src.views.inventory_view import InventoryView

class Controller():
    """Usado para conectar a lógica do jogo com as views."""
    def __init__(self):
        self.inventory_view = None
    
    def add_item_to_inventory(self, item):
        """Adiciona um item ao inventário e atualiza a view."""
        print(self.inventory_view)
        if self.inventory_view:
            self.inventory_view.add_item_to_grid(item)
        