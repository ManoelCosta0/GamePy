import json
import arcade

from src.game_objects.player import Player
from src.game_objects.item import Item

class GameView(arcade.View):
    """
    View principal do jogo, onde toda a lógica de gameplay acontece.
    """
    def __init__(self, class_: str):
        super().__init__()
        
        self.developer_mode = False

        self.player = Player(class_)
        self.enemy = None
        self.camera = arcade.Camera2D()
        
        self.sprite_list = arcade.SpriteList()
        self.tile_map = arcade.load_tilemap("assets/maps/map.tmx", scaling=4)
        
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.sprite_list.append(self.player)

    def on_draw(self):
        self.clear()
        with self.camera.activate():
            self.scene.draw(pixelated=True)
            self.sprite_list.draw(pixelated=True)
        if self.developer_mode:
            self.window.log_box.on_draw()
    
    def on_update(self, delta_time):
        """ Lógica de atualização da View. """
        self.sprite_list.update()
        self.center_camera_to_player()

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
            self.player.equip_weapon(item)
            self.window.log_box.add_message(f"Você equipou {item.name}.")
        elif key == arcade.key.ESCAPE:
            arcade.play_sound(self.window.click_sound)
            self.window.show_view(self.window.pause_view)
        elif key == arcade.key.I:
            self.window.show_view(self.window.inventory_view)
        elif key == arcade.key.TAB:
            self.developer_mode = not self.developer_mode
        elif key == arcade.key.F1:
            self.save_game()

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
                self.player.attack()
                self.window.log_box.add_message(f"Você atacou com {self.player.equipped_weapon.name}")
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
    
    def save_game(self) -> list:
        save = {
            "class": self.player.class_,
            "inventory": self.player.inventory.get_items(),
            "equipped_weapon": self.player.equipped_weapon.name if self.player.equipped_weapon else None,
            "max_hp": self.player.max_hp,
            "speed": self.player.speed,
            "position": (self.player.center_x, self.player.center_y),
        }
        with open("saves/save.json", "w") as file:
            json.dump(save, file, indent=4)
        
        self.window.log_box.add_message("Jogo salvo com sucesso!")
        return save