import arcade

from src import constants as const

class GameView(arcade.Window):

    def __init__(self):

        super().__init__(const.WINDOW_WIDTH, const.WINDOW_HEIGHT, const.WINDOW_TITLE)

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

    def setup(self):
        pass

    def on_draw(self):
        self.clear()