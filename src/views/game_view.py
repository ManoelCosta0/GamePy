import arcade

from src import constants as const
from src.game_objects.player import Player

class GameView(arcade.Window):

    def __init__(self):

        super().__init__(const.WINDOW_WIDTH, const.WINDOW_HEIGHT, const.WINDOW_TITLE)
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        self.all_sprites = arcade.SpriteList()
        self.player = None

    def setup(self):
        self.player = Player("assets/sprites/player.png", scale=0.05, center_x=800, center_y=450)
        self.all_sprites.append(self.player)

    def on_draw(self):
        self.clear()
        self.all_sprites.draw()