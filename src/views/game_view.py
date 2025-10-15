import json
import arcade

from src.game_objects.enemy import Enemy
from src.game_objects.player import Player
from src.game_objects.item import Item
from src.ui.hud import HUD as hud

class GameView(arcade.View):
    """
    View principal do jogo, onde toda a lógica de gameplay acontece.
    """
    def __init__(self):
        super().__init__()
        
        self.developer_mode = False
        
        self.enemies_list = arcade.SpriteList()
        self.hud_sprite_list = arcade.SpriteList()
        self.hud_manager = arcade.gui.UIManager()
        self.hit_box_list = arcade.SpriteList()
        
        layer_options = {
            "walls": {"use_spatial_hash": True},
            "collide": {"use_spatial_hash": True}
        }
        
        self.tile_map = arcade.load_tilemap("assets/maps/map.tmx", scaling=4, layer_options=layer_options)
        
        self.player = Player()
        self.camera = arcade.Camera2D()
        
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite("Player", self.player)

        # Adcionar "walls" como paredes e "collide" como colisões
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, [self.scene["walls"], self.scene["collide"], self.enemies_list])

        hud(self.hud_manager)

    def on_show_view(self):
        self.hud_manager.enable()
        self.enemy = Enemy("Slime1", 1000, 1500)
        self.enemies_list.append(self.enemy)

    def on_hide_view(self):
        self.hud_manager.disable()

    def on_draw(self):
        self.clear()
        with self.camera.activate():
            self.scene.draw(pixelated=True)
            self.hit_box_list.draw(pixelated=True)
            self.hud_sprite_list.draw(pixelated=True)
            self.enemies_list.draw(pixelated=True)
        self.hud_manager.draw(pixelated=True)
        if self.developer_mode:
            self.window.log_box.on_draw()
    
    def on_update(self, delta_time):
        """ Lógica de atualização da View. """
        self.player.update()
        self.enemies_list.update()
        self.hud_sprite_list.update()
        self.hit_box_list.update()
        self.physics_engine.update()
        self.center_camera_to_player()
        self.scene.update(delta_time=delta_time)

        if self.player.animation_state < 0 and self.player.attack_hitbox:
            collision_list = arcade.check_for_collision_with_list(self.player.attack_hitbox, self.enemies_list)
            for enemy in collision_list:
                enemy.hurt_enemy(self.player.attack_damage)
                self.player.attack_hitbox.kill()
                self.player.attack_hitbox = None
                self.hit_box_list.clear()

    def on_key_press(self, key, modifiers):
        """ Chamado sempre que uma tecla é pressionada. """
        if key == arcade.key.W:
            self.player.move_state_y = 1
        elif key == arcade.key.S:
            self.player.move_state_y = -1
        elif key == arcade.key.A:
            self.player.move_state_x = -1
        elif key == arcade.key.D:
            self.player.move_state_x = 1
        elif key == arcade.key.E:
            item = Item("Espada Velha")
            self.player.inventory.add_item(item)
            #self.player.equip_weapon(item)
            self.window.log_box.add_message(f"Você equipou {item.name}.")
        elif key == arcade.key.ESCAPE:
            arcade.play_sound(self.window.click_sound)
            self.window.show_view(self.window.pause_view)
        elif key == arcade.key.I:
            self.window.show_view(self.window.inventory_view)
            self.window.inventory_view.origin = self
        elif key == arcade.key.TAB:
            self.developer_mode = not self.developer_mode
        elif key == arcade.key.F1:
            self.save_game()
        elif key == arcade.key.K:
            astar_barrier = arcade.AStarBarrierList(
                self.enemies_list[0], 
                blocking_sprites=self.scene["collide"], 
                grid_size=64,
                left=-2000, right=4000, bottom=-2000, top=3000
                )
            path = arcade.astar_calculate_path(
                start_point=self.enemies_list[0].position,
                end_point=self.player.position,
                astar_barrier_list=astar_barrier)
            
            print(path)

    def on_key_release(self, key, modifiers):
        """ Chamado quando uma tecla é liberada. """
        if key == arcade.key.W or key == arcade.key.S:
            self.player.move_state_y = 0
            self.player.animation_state = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player.move_state_x = 0
            self.player.animation_state = 0

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.player.equipped_weapon:
                self.player.set_hitbox()
                self.hit_box_list.clear()
                self.hit_box_list.append(self.player.attack_hitbox)
                self.player.attack()
                
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
            "attack_cooldown": self.player.attack_cooldown,
            "position": (self.player.center_x, self.player.center_y),
        }
        with open("saves/save.json", "w") as file:
            json.dump(save, file, indent=4)
        
        self.window.log_box.add_message("Jogo salvo com sucesso!")