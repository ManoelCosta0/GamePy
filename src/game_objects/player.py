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
        super().__init__("assets/sprites/player/player_idle_right_1.png", center_x=0, center_y=0, scale=2.1)
        
        # Atributos do jogador
        self.class_ = None
        self.speed = None
        self.level = None
        self.experience = None
        self.attack_damage = 0
        self.auto_heal_factor = 1.05
        
        self.spwan_point = (0, 0)
        self.equipped_weapon = None
        self.inventory = Inventory()
        
        # Estados de animação e movimento
        self.state = "idle"
        self.animation_state = 0
        self.direction = "right"
        self.move_state_x = 0
        self.move_state_y = 0
        self.len_anims = {"walk": 6, "attack": 4, "idle": 1}
        
        # Carregar animações
        self.load_animations()
        
        self.timers = {"attack": 0.0, "animation": 0.0, "heal": 0.0, "without_take_damage": 0.0}
        self.cooldowns = {"attack": 0.3, "walk": 0.3, "idle": 0,"between_attack": 10, "heal": 4.0}

        self.attack_hitbox = None
        self.health_bar = None
        self.level_text = None
        
        self.window = arcade.get_window()
        self.hud = None
        
        self.old_health = None

    def update(self, delta_time: float = 1/60):
        """ Atualiza a lógica do jogador. """
        
        self.timers["animation"] += delta_time
        self.timers["attack"] += delta_time
        
        if self.state == "attack":
            self.update_anim(delta_time)
            self.move_player()
            
            if self.attack_hitbox:
                self.attack_hitbox.life_time -= delta_time
                if self.attack_hitbox.life_time <= 0:
                    self.attack_hitbox.remove_from_sprite_lists()
                    self.attack_hitbox = None
                    
            if self.animation_state >= self.len_anims["attack"]:
                if self.move_state_x == 0 and self.move_state_y == 0:
                    self.state = "idle"
                else:
                    self.state = "walk"
        elif self.move_state_x != 0 or self.move_state_y != 0:
            self.state = "walk"
            self.move_player()
            self.update_anim(delta_time)
        else:
            self.state = "idle"
            self.animation_state = 0
            self.update_anim(delta_time)
            
        self.health_bar.update()
        self.auto_heal(delta_time)
        self.set_level_text()

    def update_anim(self, delta_time: float = 1/60):
        self.timers["animation"] += delta_time
        if self.timers["animation"] >= self.cooldowns[self.state]:
            self.timers["animation"] = 0.0
            x = self.animation_state % self.len_anims[self.state]
            self.texture = self.animations[self.state][self.direction][x]
            self.animation_state += 1
           
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

    def equip_weapon(self, weapon: Item):
        self.equipped_weapon = weapon
        self.attack_damage = weapon.get_damage()
        self.cooldowns["between_attack"] = weapon.get_attack_speed()
        
    def unequip_weapon(self):
        if self.equipped_weapon:
            self.inventory.add_item(self.equipped_weapon)
            self.equipped_weapon = None
            self.attack_damage = 0
    
    def set_hitbox(self):
        self.attack_hitbox = arcade.SpriteSolidColor(50, 40, color=(255, 0, 0, 0))
        self.attack_hitbox.life_time = 0.14
        if self.direction == "right":
            self.attack_hitbox.center_x, self.attack_hitbox.center_y = self.center_x + 8, self.center_y - 8
        elif self.direction == "left":
            self.attack_hitbox.center_x, self.attack_hitbox.center_y = self.center_x - 8, self.center_y - 8
        elif self.direction == "up":
            self.attack_hitbox.center_x, self.attack_hitbox.center_y = self.center_x, self.center_y + 4
        elif self.direction == "down":
            self.attack_hitbox.center_x, self.attack_hitbox.center_y = self.center_x, self.center_y - 12
        self.window.game_view.add_hitbox(self.attack_hitbox)

    def attack(self):
        if self.equipped_weapon and self.timers["attack"] >= self.cooldowns["between_attack"]:
            #self.timers["attack"] = 0.0
            self.state = "attack"
            self.animation_state = 0
            self.set_hitbox()
            self.timers["attack"] = 0.0
            
            
    def auto_heal(self, delta_time):
        """ Cura automática do jogador ao longo do tempo. """
        self.timers["heal"] += delta_time
        if self.old_health and self.current_hp < self.old_health:
            self.old_health = self.current_hp
            self.timers["heal"] = 0.0
            self.timers["without_take_damage"] = 0.0
            self.auto_heal_factor = 1.05
        elif self.old_health:
            self.timers["without_take_damage"] += delta_time
            if self.timers["without_take_damage"] > 5.0:
                self.auto_heal_factor += 0.01
                self.timers["without_take_damage"] = 0.0
        if self.current_hp < self.max_hp and self.timers["heal"] >= self.cooldowns["heal"]:
            self.current_hp *= self.auto_heal_factor
            if self.current_hp > self.max_hp:
                self.current_hp = self.max_hp
            self.timers["heal"] = 0.0
        elif self.current_hp >= self.max_hp:
            self.old_health = self.max_hp
            self.auto_heal_factor = 1.05

    def _fade_in_respawn(self, delta_time):
        """Faz o sprite reaparecer gradualmente após respawn."""
        self.alpha += 15
        if self.alpha >= 255:
            arcade.unschedule(self._fade_in_respawn)
            self.alpha = 255
            self.health_bar.add_to_sprite_list()
            self.current_hp = self.max_hp
        
    def respawn(self, delta_time):
        """Reaparece o jogador no ponto de spawn após morrer."""
        arcade.unschedule(self.respawn)
        self.color = (255, 255, 255)
        self.alpha = 0
        arcade.schedule(self._fade_in_respawn, 0.05)
    
    def on_die(self):
        self.health_bar.remove_from_sprite_lists()
        self.position = self.spawn_point
        arcade.schedule(self.respawn, 1.0)

    def get_items(self):
        return self.inventory.get_items()
    
    def load_animations(self):
        # Unificar carregamento de texturas por estado e direção
        self.animations = {}
        directions = ["right", "left", "up", "down"]
        
        for state, i in self.len_anims.items():
            self.animations[state] = {}
            for direction in directions:
                self.animations[state][direction] = []
                for j in range(i):
                    texture = arcade.load_texture(f"assets/sprites/player/player_{state}_{direction}_{j+1}.png")
                    self.animations[state][direction].append(texture)

    def load_player(self, data):
        equipped = None
        if data["equipped_weapon"]:
            equipped = data["equipped_weapon"]
        self.position, self.spawn_point = data["spawn_point"], data["spawn_point"]
        self.max_hp = data["max_hp"]
        self.current_hp = self.max_hp
        self.speed = data["speed"]
        self.class_ = data["class"]
        self.level = data["level"]
        self.experience = data["experience"]

        self.health_bar = HealthBar(self, self.window.game_view.hud_sprite_list, self.max_hp, height=32)
        self.window.inventory_view.initialize_inventory(self.inventory.load_inventory(data["inventory"]), self.class_, self.speed, equipped, 0)
        
        self.hud = self.window.game_view.hud
        self.hud.set_level(self.level)
        self.hud.set_xp(self.experience, self.get_max_experience())
        self.set_level_text()

        self.old_health = self.max_hp

    def increase_experience(self, amount):
        self.experience += amount
        next_level_exp = self.get_max_experience()
        
        if self.experience >= next_level_exp:
            self.level += 1
            self.experience -= next_level_exp
            next_level_exp = self.get_max_experience()
            self.hud.set_level(self.level)
            self.level_text.text = f"Lv. {self.level}"
        
        self.hud.set_xp(self.experience, next_level_exp)
    
    def get_max_experience(self):
        return 5**self.level + 20 * self.level + 80
    
    def set_level_text(self):
        if self.level_text:
            self.level_text.x = self.center_x + 17
            self.level_text.y = self.center_y + 47
        else:
            self.level_text = arcade.Text(
                text=f"Lv. {self.level}",
                x=self.center_x + 17,
                y=self.center_y + 50,
                color=arcade.color.WHITE,
                font_size=8,
                width=20,
                font_name="arial",
                bold=True,
                anchor_x="right",
                anchor_y="top"
        )
        