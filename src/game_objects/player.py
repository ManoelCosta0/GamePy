# src/game_objects/player.py
from src.game_objects.entity import Entity
import arcade

class Player(Entity):
    def __init__(self, image_path: str, scale: float, center_x: float, center_y: float):
        super().__init__(image_path, scale, center_x, center_y, max_hp=100)