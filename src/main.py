# main.py
import arcade
from src import constants as const
from src.views.menu_view import MenuView
from src.views.game_view import GameView
from src.views.pause_view import PauseView
from src.views.inventory_view import InventoryView
from src.ui.log_box import LogBox

class MyGame(arcade.Window):
    """
    Janela Principal da Aplicação.
    """
    def __init__(self):
        super().__init__(const.WINDOW_WIDTH, const.WINDOW_HEIGHT, const.WINDOW_TITLE, resizable=True)

        self.menu_view = MenuView()
        self.game_view = GameView(class_="Warrior")
        self.pause_view = PauseView()
        self.inventory_view = InventoryView()
        self.log_box = LogBox(x=10, y=const.WINDOW_HEIGHT - 450, width=300, height=230)

        arcade.get_window().maximize()

        self.show_view(self.menu_view)

if __name__ == "__main__":
    window = MyGame()
    arcade.run()