import arcade
from src.game_objects.entity import Entity
from src.game_objects.inventory import Inventory
from src import constants as const

class Player(Entity):
    """
    Classe para o jogador no jogo.
    """
    def __init__(self):
        super().__init__("assets/sprites/player/player.png", scale=2, center_x=const.PLAYER_INITIAL_X, center_y=const.PLAYER_INITIAL_Y, max_hp=100)
        self.speed = 5
        self.move_state_x = 0
        self.move_state_y = 0
        self.equipped_weapon = None  # Arma equipada
        self.inventory = Inventory()
        
        self.animation_state = -1
        self.direction = "right"
        self.LENGTH_WALK_ANIMATION = 5
        self.load_animations()

    def update(self, delta_time: float = 1/60):
        """ Atualiza a lógica do jogador. """
        self.move_player()
        self.update_anim()
        self.update_weapon_position()
    
    def update_weapon_position(self):
        if self.equipped_weapon:
            self.equipped_weapon.center_x = self.center_x
            self.equipped_weapon.center_y = self.center_y
    
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

    def equip_weapon(self, weapon, index: int):
        self.equipped_weapon = weapon
        self.inventory.equip_item(weapon, index)
        self.attack_damage = weapon.get_damage()
        weapon.center_x = self.center_x
        weapon.center_y = self.center_y
    
    def unequip_weapon(self):
        if self.equipped_weapon:
            self.inventory.unequip_item(self.equipped_weapon)
            self.equipped_weapon = None
            self.attack_damage = 0
        else:
            print("Nenhuma arma equipada para desequipar.")
    
    def attack(self, target):
        if self.equipped_weapon:
            target.take_damage(self.attack_damage)
    
    def get_items(self):
        return self.inventory.slot_items
    
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