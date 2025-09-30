import arcade
import json
import random
from src.game_objects.entity import Entity
from src.game_objects.item import Item

enemy_json = {}
with open("data/enemies.json") as f:
    enemy_json = json.load(f)

class Enemy(Entity):
    def __init__(self, image_path: str, scale: float, center_x: float, center_y: float, max_hp: int, name: str):
        super().__init__(image_path, scale, center_x, center_y, max_hp)
        self.name = name
        self.drops = enemy_json[name]["loot_table"]

    def on_die(self) -> Item:
        for item in self.drops:
            item = Item(item)
            drop_chance = item.get_drop_chance()
            if random.random() <= drop_chance:
                print(f"{self.name} dropou {item.name}!")
                return item