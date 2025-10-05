import arcade
from src.game_objects.entity import Entity
from src.game_objects.inventory import Inventory
from src.game_objects.item import Item

class Player(Entity):
    """
    Classe para o jogador no jogo.
    """
    def __init__(self, class_: str):
        super().__init__("assets/sprites/player/player.png", center_x=400, center_y=1500)
        
        self.speed = 0
        self.move_state_x = 0
        self.move_state_y = 0
        
        self.equipped_weapon = None
        self.class_ = class_
        self.inventory = Inventory()
        self.load_class_configs(class_)
        
        self.animation_state = -1
        self.direction = "right"
        self.LENGTH_WALK_ANIMATION = 5
        self.load_animations()

    def update(self, delta_time: float = 1/60):
        """ Atualiza a lógica do jogador. """
        self.move_player()
        self.update_anim()
    
    def update_anim(self):
       if self.animation_state == -1 and self.idle_textures[self.direction] != self.texture:
           self.texture = self.idle_textures[self.direction]
       elif self.animation_state >= 0:
           self.texture = self.walk_textures[self.direction][self.animation_state // 5 % self.LENGTH_WALK_ANIMATION]
           
    def move_player(self):
        if self.move_state_x > 0:
            self.center_x += self.move_state_x * self.speed
            self.animation_state += 1
            self.direction = "right"
        elif self.move_state_x < 0:
            self.center_x += self.move_state_x * self.speed
            self.animation_state += 1
            self.direction = "left"
        if self.move_state_y > 0:
            self.center_y += self.move_state_y * self.speed
            self.animation_state += 1
            self.direction = "up"
        elif self.move_state_y < 0:
            self.center_y += self.move_state_y * self.speed
            self.animation_state += 1
            self.direction = "down"

    def equip_weapon(self, weapon: Item):
        self.equipped_weapon = weapon
        self.inventory.remove_item(weapon)
        self.attack_damage = weapon.get_damage()
    
    def unequip_weapon(self):
        if self.equipped_weapon:
            self.inventory.add_item(self.equipped_weapon)
            self.equipped_weapon = None
            self.attack_damage = 0
        else:
            print("Nenhuma arma equipada para desequipar.")
    
    def attack(self, target):
        if self.equipped_weapon:
            target.take_damage(self.attack_damage)
    
    def get_items(self):
        return self.inventory.get_items()
    
    def load_class_configs(self, class_: str):
        if class_ == "Warrior":
            self.max_hp = 150
            self.speed = 4
        elif class_ == "Assassin":
            self.max_hp = 80
            self.speed = 6
    
    def load_animations(self):
        self.idle_textures = {
            "right": arcade.load_texture("assets/sprites/player/player.png"),
            "left": arcade.load_texture("assets/sprites/player/player_left.png"),
            "up": arcade.load_texture("assets/sprites/player/player_up.png"),
            "down": arcade.load_texture("assets/sprites/player/player_down.png")}
        self.walk_textures = {"right": [], "left": [], "up": [], "down": []}
    
        for i in range(1, 6):
            right = arcade.load_texture(f"assets/sprites/player/player_walk_right_{i}.png")
            left = arcade.load_texture(f"assets/sprites/player/player_walk_left_{i}.png")
            up = arcade.load_texture(f"assets/sprites/player/player_walk_up_{i}.png")
            down = arcade.load_texture(f"assets/sprites/player/player_walk_down_{i}.png")
            self.walk_textures["right"].append(right)
            self.walk_textures["left"].append(left)
            self.walk_textures["up"].append(up)
            self.walk_textures["down"].append(down)
    
    def load_player(self, inventory_data, equipped_weapon_name, position, max_hp, speed):
        self.inventory.load_inventory(inventory_data)
        if equipped_weapon_name:
            self.equip_weapon(Item(equipped_weapon_name))
        self.center_x, self.center_y = position
        self.max_hp = max_hp
        self.speed = speed