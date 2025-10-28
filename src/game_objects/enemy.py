import arcade
import math
import json
import random

from src.game_objects.entity import Entity
from src.game_objects.item import Item
from src.ui.health_bar import HealthBar

enemy_json = {}
with open("data/enemies.json") as f:
    enemy_json = json.load(f)

class Enemy(Entity):
    """
    Classe para inimigos no jogo.
    """
    def __init__(self, name: str, x: float, y: float):
        data  = enemy_json[name]
        super().__init__(data["image_path"], x, y, max_hp=data["max_hp"], scale=data["scale"])
        
        # Atributos do inimigo
        self.name = name
        self.speed = data["speed"]
        self.drops = data["loot_table"]
        self.attack_damage = data["attack"]
        self.exp_reward = data["exp_reward"]
        
        #Informaçoes do inimigo
        self.range = data["range"]
        self.area = data["area"]
        self.spawn = (x, y)
        self.patrol_point = (x, y)
        self.target = {"x": None, "y": None}
        self.attack_range = data["attack_range"]

        # Constantes de animação (Carregadas uma vez - não mutáveis)
        self.animation_cooldowns = data["animation_cooldowns"]
        self.state_cooldowns = data["state_cooldowns"]
        self.len_anim = data["len_anim"]
        self.textures = {"idle": {}, "walk": {}, "attack": {}, "run": {}}
        self.attack_frame = data["attack_frame"]
        
        # Variáveis de animação
        self.animation_state = 0
        self.timers = {"between_attacks": 0.0, "idle": 0.0, "animation": 0.0, "between_pathfindings": 0.0}
        self.state = "idle"  # "idle", "walk", "run", "attack"
        self.direction = "left"
        
        # Carregar animações
        self.load_animations()
        
        # Carregar barra de vida
        window = arcade.get_window()
        self.health_bar = HealthBar(self, window.game_view.hud_sprite_list, self.max_hp, height=data["lifebar_height"])
        
        # Carregar variáveis de pathfinding
        self.player = window.game_view.player
        self.walls = window.game_view.scene["collide"]
    
    #----------------------
    # Máquinas de estados
    #----------------------
    
    def update(self, delta_time = 1 / 60, *args, **kwargs):
        """ Máquina de estados do inimigo. """
        if not self.is_alive(): self.state = "idle"; self.animation_state = 0
        if self.state == "idle":
            self.update_anim()
            self.timers["idle"] += delta_time
            self.find_player()
            if self.timers["idle"] >= self.state_cooldowns["idle"]:
                self.patrol()
                self.timers["idle"] = 0.0
        elif self.state == "walk":
            self.move_enemy()
            self.update_anim()
            self.find_player()
            if self.target["x"] is not None and self.target["y"] is not None:
                if math.hypot(self.center_x - self.target["x"], self.center_y - self.target["y"]) < 5:
                    self.state = "idle"
                    self.animation_state = 0
        elif self.state == "run":
            self.chase_player()
            self.move_enemy()
            self.update_anim()
        elif self.state == "attack":
            self.timers["between_attacks"] += delta_time
            if self.timers["between_attacks"] >= self.state_cooldowns["between_attacks"]:
                stage = self.update_anim()
                self.is_player_in_range(self.attack_range)
                if stage == self.attack_frame and self.is_player_in_range(self.attack_range*1.15):
                    self.attack()
                elif stage == 0:
                    self.timers["between_attacks"] = 0.0
            elif not self.is_player_in_range(self.attack_range):
                self.find_player()
            if not self.player.is_alive():
                self.state = "idle"
                self.animation_state = 0
        self.timers["animation"] += delta_time
        self.timers["between_pathfindings"] += delta_time
        self.health_bar.update()
                    
    #----------------------
    # Função de atualização de animação
    #----------------------
    
    def update_anim(self):
        """ Atualiza a animação do inimigo. """
        if self.timers["animation"] < self.animation_cooldowns[self.state]: return
        anim_length = self.len_anim[self.state]
        stage = (self.animation_state % anim_length)
        self.texture = self.textures[self.state][self.direction][stage]
        self.animation_state += 1
        self.timers["animation"] = 0.0
        return stage
    
    #----------------------
    # Funções de movimento
    #----------------------
    
    def move_enemy(self):
        """ Move o inimigo em direção a um ponto. """
        if self.target["x"] is None or self.target["y"] is None: return
        
        delta_x = self.target["x"] - self.center_x
        delta_y = self.target["y"] - self.center_y

        length = math.hypot(delta_x, delta_y)
        if length != 0: delta_x /= length; delta_y /= length

        self.center_x += delta_x * self.speed
        self.center_y += delta_y * self.speed
        
        dominant_axis = "x" if abs(delta_x) > abs(delta_y) else "y"
        if dominant_axis == "x":
            self.direction = "right" if delta_x > 0 else "left"
        else:
            self.direction = "up" if delta_y > 0 else "down"

    def patrol(self):
        """ Move o inimigo para um ponto aleatório dentro da área de patrulha. """
        self.move_to(
            random.uniform(self.patrol_point[0]-self.area, self.patrol_point[0]+self.area),
            random.uniform(self.patrol_point[1]-self.area, self.patrol_point[1]+self.area)
        )
    
    def distance_to_player(self) -> float:
        """ Retorna a distância entre o inimigo e o jogador. """
        return math.hypot(self.center_x - self.player.center_x, self.center_y - self.player.center_y)
    
    def chase_player(self):
        """ Move o inimigo em direção ao jogador. """
        if not self.player.is_alive(): return
        distance = self.distance_to_player()
        if distance < self.attack_range*0.65 or (self.direction == "down" and distance < self.attack_range*0.8): # Está em range de ataque
            self.state = "attack"
            self.timers["between_attacks"] = self.state_cooldowns["between_attacks"]
            self.animation_state = 1
            self.target = {"x": None, "y": None}
        elif self.is_player_in_range(self.range): # Não está em range de ataque mas está me range de perseguição
            self.move_to(self.player.center_x, self.player.center_y, state="run")
        else: # Não está em nenhum range
            self.patrol_point = self.position
            self.patrol()
            self.animation_state = 0

    def move_to(self, target_x: float, target_y: float, state: str = "walk"):
        """ Define um ponto para o inimigo se mover. """
        if self.target["x"] != target_x or self.target["y"] != target_y:
            self.target = {"x": target_x, "y": target_y}
            self.state = state
            #self.animation_state = 0

    # ----------------------
    # Funções de ataque
    # ----------------------

    def attack(self):
        """ Realiza um ataque no alvo. """
        self.player.take_damage(self.attack_damage)

    # ----------------------
    # Função de pathfinding
    # ----------------------
    
    def find_player(self):
        if self.timers["between_pathfindings"] >= self.state_cooldowns["between_pathfindings"]:
            self.timers["between_pathfindings"] = 0.0
            if self.is_player_in_range(self.range) and self.player.is_alive():
                self.chase_player()
    
    def is_player_in_range(self, range:float = None) -> bool:
        return arcade.has_line_of_sight(
            self.position,
            self.player.position,
            self.walls,
            max_distance=range if range else self.range,
            check_resolution=2 # Verificar possibilidades de ajuste para performance
        )
    
    #----------------------
    # Funções de morte e respawn
    #----------------------
    
    def respawn(self, delta_time):
        self.current_hp = self.max_hp
        self.center_x, self.center_y = self.spawn
        arcade.get_window().game_view.scene["enemies"].append(self)
        self.health_bar.add_to_sprite_list()
        self.state = "idle"
        self.animation_state = 0
        arcade.unschedule(self.respawn)
    
    def give_drop(self):
        for item in self.drops:
            item = Item(item)
            if random.random() < item.get_drop_chance():
                self.player.inventory.add_item(item)

    def on_die(self):
        self.remove_from_sprite_lists()
        self.player.increase_experience(self.exp_reward)
        self.give_drop()
        self.health_bar.remove_from_sprite_lists()
        self.color = (255, 255, 255, 255)
        arcade.schedule(self.respawn, 15.0)
    
    #----------------------
    # Carregamento de animações
    #----------------------
    
    def load_animations(self):
        for state, length in self.len_anim.items():
            for direction in ("left", "right", "up", "down"):
                base_path = f"assets/sprites/enemies/{self.name.lower()}/{state}/{direction}_"
                self.textures[state][direction] = [arcade.load_texture(f"{base_path}{i+1}.png") for i in range(length)]