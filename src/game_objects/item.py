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
        super().__init__(self.image_file, item_json[name]["scale"])

        self.description = item_json[name]["description"]
        self.type = item_json[name]["type"]
        self.stack_limit = item_json[name]["stack_limit"]

        self.stack = 1

    def get_damage(self):
        """Retorna o dano do item, se aplicável."""
        if self.type == "Sword":
            return item_json[self.name]["stats"]["damage"]
        return 0
    
    def get_drop_chance(self):
        """Retorna a chance de drop do item, se aplicável."""
        if "drop_chance" in item_json[self.name]:
            return item_json[self.name]["drop_chance"]
        return 0

        
