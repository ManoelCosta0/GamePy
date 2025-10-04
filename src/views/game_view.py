# src/views/game_view.py
import arcade
from src import constants as const
from src.game_objects.player import Player
from src.game_objects.enemy import Enemy
from src.game_objects.item import Item
from src.views.view import View

class GameView(arcade.View):
    """
    View principal do jogo, onde toda a lógica de gameplay acontece.
    """
    def __init__(self):
        super().__init__()

        self.player = Player()
        self.enemy = None
        self.camera = arcade.Camera2D()
        
        self.sprite_list = arcade.SpriteList()
        self.tile_map = arcade.load_tilemap("assets/maps/map.json", scaling=4)
        
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.sprite_list.append(self.player)

    def on_draw(self):
        self.clear()
        with self.camera.activate():
            self.scene.draw()
            self.sprite_list.draw()
    
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
            self.window.inventory_view.add_item_on_display(item)
            self.window.log_box.add_message("Você pegou uma Espada Velha!")
        elif key == arcade.key.ESCAPE:
            self.window.show_view(self.window.pause_view)
        elif key == arcade.key.I:
            self.window.show_view(self.window.inventory_view)
        elif key == arcade.key.TAB:
            self.developer_mode = not self.developer_mode
            print(f"Developer Mode {'ON' if self.developer_mode else 'OFF'}")

    def on_key_release(self, key, modifiers):
        """ Chamado quando uma tecla é liberada. """
        if key == arcade.key.W or key == arcade.key.S:
            self.player.move_state_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player.move_state_x = 0

    def on_mouse_release(self, x, y, button, modifiers):
        """ Chamado quando o botão do mouse é liberado. """
        if button == arcade.MOUSE_BUTTON_LEFT and self.player.equipped_weapon:
            if self.enemy is None: return
            check = arcade.check_for_collision(self.player.equipped_weapon, self.enemy)
            if check:
                self.player.attack(self.enemy)
    
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
    
    def equip_item_on_game(self, item: Item):
        """Equipa um item na tela do jogo."""
        self.sprite_list.append(item)
    
    def unequip_item_on_game(self, item: Item):
        """Remove o item equipado da tela do jogo."""
        if item in self.sprite_list:
            self.sprite_list.remove(item)
            self.window.log_box.add_message(f"Removendo {item.name}...")