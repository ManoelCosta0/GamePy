import arcade
from src import constants as const
from src.ui.buttons import SpriteButton

class View(arcade.View):
    """
    Classe base para (quase) todas as Views do jogo.
    """
    def __init__(self):
        super().__init__()

        self.game_view = None
        self.menu_view = None
        self.pause_view = None

        self.background_sprite = None
        self.general_sprite_list = arcade.SpriteList()
        self.button_list = arcade.SpriteList()
        self.window = arcade.get_window()
        self.developer_mode = False
        self.is_dragging = False

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        """ Chamado quando o mouse se move - para o efeito de hover. """

        buttons_colliding = arcade.get_sprites_at_point((x, y), self.button_list)

        for button in self.button_list:
            if button in buttons_colliding:
                button.on_hover()
            else:
                button.on_unhover()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.TAB:
            self.developer_mode = not self.developer_mode
            print(f"Developer Mode {'ON' if self.developer_mode else 'OFF'}")

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """ Chamado quando o mouse é arrastado. """
        buttons_colliding = arcade.get_sprites_at_point((x, y), self.button_list)
        
        if buttons_colliding:
            self.is_dragging = True
            buttons_colliding[0].center_x += dx
            buttons_colliding[0].center_y += dy
    
    def on_mouse_release(self, x, y, button, modifiers):
        self.is_dragging = False
        buttons_colliding = arcade.get_sprites_at_point((x, y), self.button_list)
        if buttons_colliding:
            print(f"Botão {buttons_colliding[0].name} solto em ({buttons_colliding[0].center_x}, {buttons_colliding[0].center_y})")

    def on_draw(self):
        """ Desenha o menu de pausa. """
        self.clear()
        self.general_sprite_list.draw()
        self.button_list.draw()