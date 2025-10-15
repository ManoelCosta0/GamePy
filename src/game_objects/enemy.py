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
        info  = enemy_json[name]
        super().__init__(info["image_path"], x, y, max_hp=info["max_hp"], scale=info["scale"])
        
        # Atributos do inimigo
        self.name = name
        self.speed = info["speed"]
        self.drops = info["loot_table"]
        self.attack = info["attack"]
        
        #Informaçoes do inimigo
        self.range = 100
        self.area = 150
        self.spawn = (x, y)
        self.target = {"x": None, "y": None}
        self.attack_range = 40
        
        # Constantes de animação (Carregadas uma vez - não mutáveis)
        self.animation_cooldowns = {"idle": 0.17, "walk": 0.12, "attack": 0.1, "run": 0.1}
        self.state_cooldowns = {"between_attacks": 1.0, "idle": 5.0}
        self.len_anim = {"idle": 6, "walk": 8, "attack": 10, "run": 8}
        self.textures = {"idle": {}, "walk": {}, "attack": {}, "run": {}}
        
        # Variáveis de animação
        self.animation_state = 0
        self.timers = {"between_attacks": 0.0, "idle": 0.0, "animation": 0.0}
        self.state = "idle"  # "idle", "walk", "run", "attack"
        self.direction = "left"
        
        # Carregar animações
        self.load_animations()
        
        # Carregar barra de vida
        window = arcade.get_window()
        self.health_bar = HealthBar(self, window.game_view.hud_sprite_list, self.max_hp, height=-40)
        
        # Carregar variáveis de pathfinding
        self.player = window.game_view.player
        self.walls = window.game_view.scene["collide"]
        self.astar_barrier_list = self.load_astar_barrier()
    
    #----------------------
    # Máquinas de estados
    #----------------------
    def update(self, delta_time = 1 / 60, *args, **kwargs):
        """ Máquina de estados do inimigo. """
        if self.state in ["walk", "run"]:
            self.move_enemy()
            self.update_anim()
        elif self.state == "idle":
            self.timers["idle"] += delta_time
            if self.timers["idle"] >= self.state_cooldowns["idle"]:
                #self.patrol()
                self.timers["idle"] = 0.0
            self.update_anim()
        elif self.state == "attack":
            self.timers["between_attacks"] += delta_time
            if self.timers["between_attacks"] >= self.state_cooldowns["between_attacks"]:
                if self.update_anim() == 0: self.timers["between_attacks"] = 0.0
        self.timers["animation"] += delta_time
        self.health_bar.update()
    '''
    def update(self, delta_time = 1 / 60, *args, **kwargs):
        """ Máquina de estados do inimigo. """
        if self.state == "idle":
            self.update_anim() #Verificar se é mais eficiente chamar upodate_anim() primeiro ou por último
            self.timers["idle"] += delta_time
            if self.is_player_in_range():
                self.chase_player()
            elif self.timers["idle"] >= self.state_cooldowns["idle"]:
                self.patrol()
                self.timers["idle"] = 0.0
        elif self.state == "walk":
            self.move_enemy()
            self.update_anim()
            if self.is_player_in_range():
                self.chase_player()
            elif self.target["x"] is not None and self.target["y"] is not None:
                if math.hypot(self.center_x - self.target["x"], self.center_y - self.target["y"]) < 5:
                    self.state = "idle"
                    #self.timers["idle"] = 0.0 
                    self.animation_state = 0
        elif self.state == "run":
            self.move_enemy()
            self.update_anim()
            self.chase_player()
        elif self.state == "attack":
            self.timers["between_attacks"] += delta_time
            if self.timers["between_attacks"] >= self.state_cooldowns["between_attacks"]:
                if self.update_anim() == 0: self.timers["between_attacks"] = 0.0
                if not self.is_player_in_range(self.attack_range):
                    self.chase_player()
        self.timers["animation"] += delta_time
        self.health_bar.update()
        '''
                    
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
            random.uniform(self.spawn[0]-self.area, self.spawn[0]+self.area),
            random.uniform(self.spawn[1]-self.area, self.spawn[1]+self.area)
        )
    
    def chase_player(self):
        """ Move o inimigo em direção ao jogador. """
        self.state = "run"
        # Desafio: lidar com movimentação do player enquanto o inimigo está se movendo
        # Sugestão 1: chamar is_player_in_range() a cada X segundos
        # Sugestão 2: Chamar get_path_to_player() a cada Y segundos (X < Y)
        # Quando get_path_to_player() for chamado, is_player_in_range() não deverá ser chamado
        # Questionamento: Se o player se manter parado, o pathfinding seguirá um caminho fixo?
        # Sugestão 3: Recalcular o caminho a cada path andado
        # Sugestão 4: range de 450
        pass
    
    def move_to(self, target_x: float, target_y: float, state: str = "walk"):
        """ Define um ponto para o inimigo se mover. """
        if self.target["x"] != target_x or self.target["y"] != target_y:
            self.target = {"x": target_x, "y": target_y}
            self.state = state
            self.animation_state = 0

    # ----------------------
    # Função de pathfinding
    # ----------------------
    
    def get_path_to_player(self):
        
        self.astar_barrier_list.left = self.center_x - self.range
        self.astar_barrier_list.right = self.center_x + self.range
        self.astar_barrier_list.bottom = self.center_y - self.range
        self.astar_barrier_list.top = self.center_y + self.range
        
        return arcade.astar_calculate_path(
            self.position,
            self.player.position,
            self.astar_barrier_list
        )
    
    def load_astar_barrier(self):
        return arcade.AStarBarrierList(
                self, 
                blocking_sprites=self.walls, 
                grid_size=64,
                left=0, right=0, bottom=0, top=0)
    
    def is_player_in_range(self, range:float = None) -> bool:
        return arcade.has_line_of_sight(
            self.position,
            self.player.position,
            self.walls,
            max_distance=range if range else self.range,
            check_resolution=2 # Verificar possibilidades de ajuste para performance
        )

    #----------------------
    # Funções de dano
    #----------------------
    
    def hurt_enemy(self, damage: int):
        self.take_damage(damage)
        if self.current_hp <= 0:
            return self.on_die()
        else:
            self.hurt_flash()
            return None

    def hurt_flash(self):
        self.color = (255, 100, 100)  # levemente avermelhado
        self.alpha = 200  # semi-transparente
        arcade.schedule(self.reset_color, 0.15)
    
    def reset_color(self, delta_time):
        self.color = (255, 255, 255)  # volta à cor normal
        self.alpha = 255  # volta à opaco
        arcade.unschedule(self.reset_color)
    
    def on_die(self) -> Item:
        self.remove_from_sprite_lists()
        for item in self.drops:
            item = Item(item)
            drop_chance = item.get_drop_chance()
            if random.random() <= drop_chance:
                return item
    
    #----------------------
    # Carregamento de animações
    #----------------------
    
    def load_animations(self):
        for state, length in self.len_anim.items():
            for direction in ("left", "right", "up", "down"):
                base_path = f"assets/sprites/enemies/{self.name.lower()}/{state}/{direction}_"
                self.textures[state][direction] = [arcade.load_texture(f"{base_path}{i+1}.png") for i in range(length)]