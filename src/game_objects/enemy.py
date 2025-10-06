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
        self.drops = info["loot_table"]

    def on_die(self) -> Item:
        self.remove_from_sprite_lists()
        for item in self.drops:
            item = Item(item)
            drop_chance = item.get_drop_chance()
            if random.random() <= drop_chance:
                return item