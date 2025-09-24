# main.py
import arcade
from src import constants as const
from src.views.menu_view import MenuView
from src.views.game_view import GameView
from src.views.pause_view import PauseView

class MyGame(arcade.Window):
    """
    Janela Principal da Aplicação.
    """
    def __init__(self):
        super().__init__(const.WINDOW_WIDTH, const.WINDOW_HEIGHT, const.WINDOW_TITLE, resizable=True)


        self.menu_view = MenuView()
        self.game_view = GameView()
        self.pause_view = PauseView()

        self.menu_view.game_view = self.game_view
        self.game_view.pause_view = self.pause_view
        self.pause_view.game_view = self.game_view
        self.pause_view.menu_view = self.menu_view

        arcade.get_window().maximize()

        self.show_view(self.menu_view)

if __name__ == "__main__":
    window = MyGame()
    arcade.run()