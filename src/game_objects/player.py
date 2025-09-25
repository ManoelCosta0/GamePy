# src/game_objects/player.py
from src.game_objects.entity import Entity
from src.game_objects.inventory import Inventory

class Player(Entity):
    def __init__(self, image_path: str, scale: float, center_x: float, center_y: float):
        super().__init__(image_path, scale, center_x, center_y, max_hp=100)
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_moving = False
        self.equipped_weapon = None  # Arma equipada
        self.inventory = Inventory()

    def update(self, *args, **kwargs):
        # Lógica de atualização do jogador
        if self.is_moving:
            self.center_x += self.velocity_x
            if self.equipped_weapon:
                self.equipped_weapon.center_x += self.velocity_x
                self.equipped_weapon.center_y += self.velocity_y
            self.center_y += self.velocity_y
        pass