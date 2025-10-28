# main.py
import arcade
from src import constants as const
from src.views.menu_view import MenuView
from src.views.classes_view import ClassesView
from src.views.pause_view import PauseView
from src.views.inventory_view import InventoryView
from src.ui.log_box import LogBox

class MyGame(arcade.Window):
    """
    Janela Principal da Aplicação.
    """
    def __init__(self):
        super().__init__(const.WINDOW_WIDTH, const.WINDOW_HEIGHT, const.WINDOW_TITLE, resizable=True)
        
        self.developer_mode = False  # Ativar modo desenvolvedor para toda a aplicação
        self._background_color = (36, 160, 222) # cor de fundo escura
        self.volume = 20/100
        
        # Inicializa as Views
        self.menu_view = MenuView()
        self.classes_view = ClassesView()
        self.game_view = None 
        self.pause_view = PauseView()
        self.inventory_view = InventoryView()
        self.log_box = LogBox(x=10, y=160, width=300, height=150)

        # Carrega os sons
        self.click_sound = arcade.load_sound("assets/sounds/ui/on_click_1.wav")
        
        # Maxima a janela e mostra a View do Menu
        self.show_view(self.menu_view)

if __name__ == "__main__":
    window = MyGame()
    arcade.run()