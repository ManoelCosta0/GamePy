import arcade
import json

item_json = {}
with open("data/items.json") as f:
            item_json = json.load(f)

class Item(arcade.Sprite):
    """Classe base para itens no jogo."""

    def __init__(self, name: str):
        
        self.name = name
        self.image_file = item_json[name]["sprite_path"]
        self.scale = item_json[name]["scale"]
        super().__init__(self.image_file, self.scale)

        self.description = item_json[name]["description"]
        self.type = item_json[name]["type"]
        self.stack_limit = item_json[name]["stack_limit"]

        self.stack = 1

        
