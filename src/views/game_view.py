import json
import arcade

from src.game_objects.enemy import Enemy
from src.game_objects.player import Player
from src.game_objects.item import Item
from src.ui.hud import HUD as hud
from src.game_objects.campfire import Campfire

spawns = {}
with open("data/spawns_set.json") as f:
    spawns = json.load(f)

class GameView(arcade.View):
    """
    View principal do jogo, onde toda a lógica de gameplay acontece.
    """
    def __init__(self):
        super().__init__()
        
        #Settings
        self.configs = {
            "fps": False,
            "fullscreen": True,
            "logbox": False,
            "perf_graph": False
        }
        self.timers = {"fps": 0.0}
        self.fps = 0
        
        self.enemies_list = arcade.SpriteList()
        self.hud_sprite_list = arcade.SpriteList()
        self.hud_manager = arcade.gui.UIManager()
        self.hit_box_list = arcade.SpriteList()
        self.campfires_list = arcade.SpriteList()
        
        self.campfire = None
        
        self.perf_graph_list = arcade.SpriteList()
        graph = arcade.PerfGraph(200, 120, graph_data="FPS")
        graph.position = (self.window.width - 230, self.window.height - 75)
        self.perf_graph_list.append(graph)
        arcade.enable_timings()

        layer_options = {
            "walls": {"use_spatial_hash": True},
            "collide": {"use_spatial_hash": True},
            "interactive_obj": {"use_spatial_hash": True},
            "interactive_area": {"use_spatial_hash": True},
        }
        
        self.tile_map = arcade.load_tilemap("assets/maps/map.tmx", scaling=3, layer_options=layer_options)
        
        self.player = Player()
        self.camera = arcade.Camera2D()
        
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite("player", self.player)

        # Adcionar "walls" como paredes e "collide" como colisões
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, [self.scene["walls"], self.scene["collide"], self.scene["interactive_obj"], self.scene["enemies"]])

        self.hud = hud(self.hud_manager)

    def on_show_view(self):
        self.hud_manager.enable()

    def on_hide_view(self):
        self.hud_manager.disable()

    def on_draw(self):
        self.clear()
        with self.camera.activate():
            self.scene.draw(pixelated=True)
            self.hit_box_list.draw(pixelated=True)
            self.hud_sprite_list.draw(pixelated=True)
            self.campfires_list.draw(pixelated=True)
            if self.player.level_text:
                self.player.level_text.draw()
        self.hud_manager.draw(pixelated=True)
        
        if self.configs["perf_graph"]:
            self.perf_graph_list.draw()
        if self.configs["logbox"]:
            self.window.log_box.on_draw()
        if self.configs["fps"]:
            arcade.draw_text(
            f"FPS: {self.fps:.1f}", self.window.width - 80, self.window.height - 25,
            arcade.color.WHITE, 14)
    
    def on_update(self, delta_time):
        """ Lógica de atualização da View. """
        self.scene.update(delta_time=delta_time)
        self.physics_engine.update()
        self.player.update()
        self.hit_box_list.update()
        self.campfires_list.update()
        self.hud_sprite_list.update()
        self.center_camera_to_player()
        
        self.timers["fps"] += delta_time
        if self.configs["fps"] and self.timers["fps"] >= 0.2:
            self.timers["fps"] = 0.0
            self.fps = arcade.get_fps()

        if self.player.attack_hitbox:
            collision_list = arcade.check_for_collision_with_list(self.player.attack_hitbox, self.scene["enemies"])
            for enemy in collision_list:
                enemy.take_damage(self.player.attack_damage)
            if self.player.attack_hitbox and len(collision_list) > 0:
                self.player.attack_hitbox.kill()
                self.player.attack_hitbox = None
                self.hit_box_list.clear()

    def on_key_press(self, key, modifiers):
        """ Chamado sempre que uma tecla é pressionada. """
        if key == arcade.key.W or key == arcade.key.UP:
            self.player.move_state_y = 1
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.player.move_state_y = -1
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.player.move_state_x = -1
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.player.move_state_x = 1
        elif key == arcade.key.E:
            collision_list = arcade.check_for_collision_with_list(self.player, self.scene["interactive_area"])
            if collision_list:
                x = self.scene["interactive_area"].index(collision_list[0]) - 1
                campfire = self.scene["interactive_obj"][x]
                if self.campfire != campfire and not campfire.campfire_activated:
                    self.campfire.desactivate_campfire()
                    self.campfire = campfire
                    if self.campfire.activate_campfire():
                        self.window.log_box.add_message("Ponto de spawn atualizado!")
                        self.save_game()
                elif self.campfire == campfire and not campfire.campfire_activated:
                    self.campfire.activate_campfire()
                elif self.campfire == campfire and campfire.campfire_activated:
                    self.campfire.desactivate_campfire()
        elif key == arcade.key.ESCAPE:
            arcade.play_sound(self.window.click_sound, volume=self.window.volume)
            self.window.show_view(self.window.pause_view)
        elif key == arcade.key.I:
            self.window.show_view(self.window.inventory_view)
        elif key == arcade.key.F1:
            self.save_game()
        elif key == arcade.key.K:
            x, y = self.player.position
            position = (int(x), int(y))
            self.window.log_box.add_message(f"Posição do jogador: {position}")
            print(f"Posição do jogador: {position}")
        elif key == arcade.key.LSHIFT:
            self.player.speed += 2

    def on_key_release(self, key, modifiers):
        """ Chamado quando uma tecla é liberada. """
        if key == arcade.key.W or key == arcade.key.S or key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.move_state_y = 0
            self.player.animation_state = 0
        elif key == arcade.key.A or key == arcade.key.D or key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.move_state_x = 0
            self.player.animation_state = 0
        elif key == arcade.key.LSHIFT:
            self.player.speed -= 2
            
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.player.equipped_weapon:
                self.player.attack()
    
    def add_hitbox(self, hitbox):
        self.hit_box_list.clear()
        self.hit_box_list.append(hitbox)
    
    def center_camera_to_player(self):
        screen_center_x, screen_center_y = self.player.position
        if screen_center_x < self.camera.viewport_width/2:
            screen_center_x = self.camera.viewport_width/2
        if screen_center_y < self.camera.viewport_height/2:
            screen_center_y = self.camera.viewport_height/2
        user_centered = screen_center_x, screen_center_y

        self.camera.position = arcade.math.lerp_2d(
            self.camera.position,
            user_centered,
            1,
        )
    
    def save_game(self):
        save = {
            "class": self.player.class_,
            "inventory": self.player.inventory.get_items(),
            "equipped_weapon": self.player.equipped_weapon.name if self.player.equipped_weapon else None,
            "max_hp": self.player.max_hp,
            "speed": self.player.speed,
            "spawn_point": self.player.spawn_point,
            "level": self.player.level,
            "experience": self.player.experience
        }
        with open("saves/save.json", "w") as file:
            json.dump(save, file, indent=4)
        
        self.window.log_box.add_message("Jogo salvo com sucesso!")
    
    def load_game(self):
        for enemy, data in spawns["enemies"].items():
            for x, y in data:
                new_enemy = Enemy(enemy, x, y)
                self.scene["enemies"].append(new_enemy)
        for spawn, data in spawns["campfires"].items():
            spawn = tuple(map(int, spawn.split(',')))
            campfire = Campfire(data, self.player, self.scene, spawn)            
            if spawn == tuple(self.player.spawn_point):
                campfire.activate_campfire()
                self.campfire = campfire