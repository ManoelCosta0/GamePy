import arcade

from src import constants as const
from src.game_objects.player import Player

class GameView(arcade.Window):

    def __init__(self):

        super().__init__(const.WINDOW_WIDTH, const.WINDOW_HEIGHT, const.WINDOW_TITLE, resizable=True)
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        self.sprite_list = arcade.SpriteList()
        self.player = None

    def setup(self):
        self.player = Player("assets/sprites/player.png", scale=0.03, center_x=800, center_y=450)
        self.sprite_list.append(self.player)

    def on_draw(self):
        self.clear()
        self.sprite_list.draw()

    def on_key_press(self, key, modifiers):
        """Chamado sempre que uma tecla é pressionada."""
        if key == arcade.key.W:
            self.player.is_moving = True
            self.player.velocity_y = const.MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player.is_moving = True
            self.player.velocity_y = -const.MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player.is_moving = True
            self.player.velocity_x = -const.MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player.is_moving = True
            self.player.velocity_x = const.MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Chamado quando uma tecla é liberada."""
        if key == arcade.key.W or key == arcade.key.S:
            self.player.is_moving = False
            self.player.velocity_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player.is_moving = False
            self.player.velocity_x = 0
        pass

    def on_update(self, delta_time):
        self.sprite_list.update()