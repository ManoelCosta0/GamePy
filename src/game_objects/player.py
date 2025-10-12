import arcade

from src.game_objects.entity import Entity
from src.game_objects.inventory import Inventory
from src.game_objects.item import Item
from src.ui.health_bar import HealthBar

class Player(Entity):
    """
    Classe para o jogador no jogo.
    """
    def __init__(self):
        super().__init__("assets/sprites/player/player.png", center_x=0, center_y=0, scale=2.0)
        
        # Atributos do jogador
        self.class_ = None
        self.speed = None
        self.equipped_weapon = None
        self.inventory = Inventory()
        self.attack_cooldown = None
        
        # Carregar animações
        self.load_animations()
        
        # Estados de animação e movimento
        self.animation_state = 0
        self.direction = "right"
        self.LENGTH_WALK_ANIMATION = 6
        self.attack_timer = 0.0
        self.move_state_x = 0
        self.move_state_y = 0
        
        self.attack_hitbox = None
        self.health_bar = None
        
        self.window = arcade.get_window()

    def update(self, delta_time: float = 1/60):
        """ Atualiza a lógica do jogador. """
        self.move_player()
        self.update_anim(delta_time)
        self.health_bar.update()

    def update_anim(self, delta_time: float = 1/60):
       if self.animation_state == 0 and self.idle_textures[self.direction] != self.texture:
           self.texture = self.idle_textures[self.direction]
       elif self.animation_state > 0:
           #x precisa estar entre 0 e 5 com animation_state indo de 1 a infinito
           x = (self.animation_state // 6 % self.LENGTH_WALK_ANIMATION)
           self.texture = self.walk_textures[self.direction][x]
       elif self.animation_state < 0:
           if self.attack_hitbox: self.attack_hitbox.life_time -= delta_time
           if self.attack_hitbox and self.attack_hitbox.life_time <= 0:
                self.attack_hitbox.remove_from_sprite_lists()
                self.attack_hitbox = None
            
           self.attack_timer += delta_time
           if self.attack_timer >= self.attack_cooldown and self.animation_state >= -4:
                self.attack_timer = 0.0
                self.texture = self.attack_textures[self.direction][-self.animation_state - 1]
                self.animation_state -= 1
           elif self.animation_state < -4:
                self.animation_state = 0
           
    def move_player(self):
        if self.move_state_x > 0:
            self.center_x += self.move_state_x * self.speed
            self.direction = "right"
        elif self.move_state_x < 0:
            self.center_x += self.move_state_x * self.speed
            self.direction = "left"
        if self.move_state_y > 0:
            self.center_y += self.move_state_y * self.speed
            self.direction = "up"
        elif self.move_state_y < 0:
            self.center_y += self.move_state_y * self.speed
            self.direction = "down"
        if (self.move_state_x != 0 or self.move_state_y != 0) and self.animation_state >= 0:
            self.animation_state += 1

    def equip_weapon(self, weapon: Item):
        self.equipped_weapon = weapon
        if self.inventory.find_item(weapon.name) is not None: self.inventory.remove_item(weapon)
        '''Verificação temporária (remover depois) 
        Motivo: verificação acontece em todas as chamadas de equip_weapon, mas só serve para a primeira vez (load_player)
        '''
        self.attack_damage = weapon.get_damage()
        
    def unequip_weapon(self):
        if self.equipped_weapon:
            self.inventory.add_item(self.equipped_weapon)
            self.equipped_weapon = None
            self.attack_damage = 0
        else:
            print("Nenhuma arma equipada para desequipar.")
    
    def set_hitbox(self):
        self.attack_hitbox = arcade.SpriteSolidColor(50, 40, color=(255, 0, 0, 100))
        self.attack_hitbox.life_time = 0.14
        if self.direction == "right":
            self.attack_hitbox.center_x, self.attack_hitbox.center_y = self.center_x + 8, self.center_y - 8
        elif self.direction == "left":
            self.attack_hitbox.center_x, self.attack_hitbox.center_y = self.center_x - 8, self.center_y - 8
        elif self.direction == "up":
            self.attack_hitbox.center_x, self.attack_hitbox.center_y = self.center_x, self.center_y + 4
        elif self.direction == "down":
            self.attack_hitbox.center_x, self.attack_hitbox.center_y = self.center_x, self.center_y - 12

    def attack(self):
        if self.equipped_weapon is None: return
        self.animation_state = -1

    def get_items(self):
        return self.inventory.get_items()
    
    def load_animations(self):
        self.idle_textures = {
            "right": arcade.load_texture("assets/sprites/player/player.png"),
            "left": arcade.load_texture("assets/sprites/player/player_left.png"),
            "up": arcade.load_texture("assets/sprites/player/player_up.png"),
            "down": arcade.load_texture("assets/sprites/player/player_down.png")}
        
        self.walk_textures = {"right": [], "left": [], "up": [], "down": []}
        for i in range(1, 7):
            right = arcade.load_texture(f"assets/sprites/player/player_walk_right_{i}.png")
            left = arcade.load_texture(f"assets/sprites/player/player_walk_left_{i}.png")
            up = arcade.load_texture(f"assets/sprites/player/player_walk_up_{i}.png")
            down = arcade.load_texture(f"assets/sprites/player/player_walk_down_{i}.png")
            self.walk_textures["right"].append(right)
            self.walk_textures["left"].append(left)
            self.walk_textures["up"].append(up)
            self.walk_textures["down"].append(down)
        
        self.attack_textures = {"right": [], "left": [], "up": [], "down": []}
        for i in range(1, 5):
            right = arcade.load_texture(f"assets/sprites/player/player_attack_right_{i}.png")
            left = arcade.load_texture(f"assets/sprites/player/player_attack_left_{i}.png")
            up = arcade.load_texture(f"assets/sprites/player/player_attack_up_{i}.png")
            down = arcade.load_texture(f"assets/sprites/player/player_attack_down_{i}.png")
            self.attack_textures["right"].append(right)
            self.attack_textures["left"].append(left)
            self.attack_textures["up"].append(up)
            self.attack_textures["down"].append(down)
    
    def load_player(self, data):
        self.inventory.load_inventory(data["inventory"])
        if data["equipped_weapon"]:
            self.equip_weapon(Item(data["equipped_weapon"]))
        self.center_x, self.center_y = data["position"]
        self.max_hp = data["max_hp"]
        self.current_hp = self.max_hp
        self.speed = data["speed"]
        self.attack_cooldown = data["attack_cooldown"]
        self.class_ = data["class"]

        self.health_bar = HealthBar(self, self.window.game_view.hud_sprite_list, self.max_hp, height=10)
        self.window.inventory_view.initialize_inventory(self.inventory.get_items(), self.class_, self.speed, self.equipped_weapon, 20)  # Adiciona o ataque como 20 temporariamente