import arcade
import math
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
        
        self.len_anim = {"idle": 6, "walk": 8, "attack": 10, "run": 8, "hurt": 3}
        self.textures = {"idle": {}, "walk": {}, "attack": {}, "run": {}, "hurt": {}}
        self.animation_state = 0
        self.timer = 0.0
        self.ANIMATION_COOLDOWN = 0.020
        self.ATTACK_COOLDOWN = 0.1

        self.load_animations()

        self.state = "idle"
        self.direction = "left"
        self.target = {"x": None, "y": None}
        self.range = 35
    
    def update(self, delta_time = 1 / 60, *args, **kwargs):
        if self.state == "walk" or self.state == "run":
            self.move_enemy()
        self.timer += delta_time
        self.update_anim()

    def update_anim(self):
        if self.state == "idle" and self.timer <= self.ANIMATION_COOLDOWN: return
        elif self.state != "idle" and self.timer <= self.ANIMATION_COOLDOWN - 0.015: return
        x = (self.animation_state // self.len_anim[self.state] % self.len_anim[self.state])
        if self.state == "attack" and x == 0 and self.timer <= self.ATTACK_COOLDOWN: return
        self.texture = self.textures[self.state][self.direction][x]
        self.animation_state += 1
        self.timer = 0.0
    
    def move_enemy(self):
        if (self.target["x"] and self.target["y"]) is None: return
        distance = abs(math.dist((self.center_x, self.center_y), (self.target["x"], self.target["y"])))
        if distance < self.range: # Chegou no destino
            self.target["x"], self.target["y"] = None, None
            self.state = "attack"
            self.animation_state = 0
            return
        
        delta_x = self.target["x"] - self.center_x
        delta_y = self.target["y"] - self.center_y

        length = math.hypot(delta_x, delta_y)
        if length != 0: delta_x /= length; delta_y /= length

        self.center_x += delta_x * self.speed
        self.center_y += delta_y * self.speed
        
        new_direction = self.direction
        if abs(delta_x) > abs(delta_y):
            new_direction = "right" if delta_x > 0 else "left"
        elif abs(delta_y) > abs(delta_x):
            new_direction = "up" if delta_y > 0 else "down"
            
        if new_direction != self.direction:
            self.direction = new_direction
            self.animation_state = 0

    def load_animations(self):
        states = ["idle", "walk", "attack", "run", "hurt"]
        directions = ["left", "right", "up", "down"]
        for state in states:
            for direction in directions:
                self.textures[state][direction] = []
                for i in range(1, self.len_anim[state] + 1):
                    path = f"assets/sprites/enemies/{self.name.lower()}/{state}/{self.name.lower()}_{state}_{direction}_{i}.png"
                    texture = arcade.load_texture(path)
                    self.textures[state][direction].append(texture)
    
    def move_to(self, target_x: float, target_y: float):
        self.target = {"x": target_x, "y": target_y}
        self.state = "run"
        self.animation_state = 0

    def on_die(self) -> Item:
        self.remove_from_sprite_lists()
        for item in self.drops:
            item = Item(item)
            drop_chance = item.get_drop_chance()
            if random.random() <= drop_chance:
                return item