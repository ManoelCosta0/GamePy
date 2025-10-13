import arcade
import json
import random
from src.game_objects.entity import Entity
from src.game_objects.item import Item

enemy_json = {}
with open("data/enemies.json") as f:
    enemy_json = json.load(f)

class Enemy(Entity):
    """
    Classe para inimigos no jogo.
    """
    def __init__(self, name: str, x: float, y: float):
        info  = enemy_json[name]
        super().__init__(info["image_path"], x, y, max_hp=info["max_hp"], scale=info["scale"])
        self.name = name
        self.speed = info["speed"]
        self.drops = info["loot_table"]
        self.attack = info["attack"]
        
        self.state = "idle"
        self.direction = "left"
        self.len_anim = {"idle": 6, "walk": 8, "attack": 10, "run": 8, "hurt": 3}
        self.target = (None, None)
    
    def update(self, delta_time = 1 / 60, *args, **kwargs):
        if self.target[0] is not None and self.target != (self.center_x, self.center_y): # Se não tiver chegado ao objetivo
            print("Moving to", self.target)
            if self.target[0] - self.center_x > 0:
                self.direction = "right"
                self.change_x = self.speed
            elif self.target[0] - self.center_x < 0:
                self.direction = "left"
                self.change_x = -self.speed

            if self.target[1] - self.center_y > 0:
                self.change_y = self.speed
            elif self.target[1] - self.center_y < 0:
                self.change_y = -self.speed

    def move_to(self, target_x: float, target_y: float):
        self.target = (target_x, target_y)

    def on_die(self) -> Item:
        self.remove_from_sprite_lists()
        for item in self.drops:
            item = Item(item)
            drop_chance = item.get_drop_chance()
            if random.random() <= drop_chance:
                return item