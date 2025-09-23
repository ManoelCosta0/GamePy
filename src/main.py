# main.py
import arcade
from src import constants as const
from src.views.game_view import GameView  # Importa a sua View
from src.views.game_view import MenuView  # Importa a View do Menu

class MyGame(arcade.Window):
    """
    Janela Principal da Aplicação.
    """
    def __init__(self):
        super().__init__(const.WINDOW_WIDTH, const.WINDOW_HEIGHT, const.WINDOW_TITLE, resizable=True)

        game_view = GameView()
        menu_view = MenuView()
        self.show_view(menu_view)

if __name__ == "__main__":
    window = MyGame()
    arcade.run()