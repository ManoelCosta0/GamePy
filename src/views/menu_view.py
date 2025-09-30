import arcade
from src import constants as const
from src.views.view import View
from src.ui.buttons import SpriteButton

class MenuView(View):
    """
    Tela do Menu Principal.
    """
    def __init__(self):
        super().__init__()

        self.background_sprite = arcade.Sprite("assets/UI/background.png", scale=1.15)
        new_game_button = SpriteButton(
            name="new_game",
            normal_texture_path="assets/UI/New_Game_Buttom_normal.png",
            hover_texture_path="assets/UI/New_Game_Buttom_hover.png")

        self.general_sprite_list.append(self.background_sprite)
        self.button_list.append(new_game_button)
        
    def on_show_view(self):
        """ Chamado quando esta View é mostrada. """
        self.clear()
        arcade.set_background_color(arcade.color.BLACK) # Um fundo preto para garantir
    
    def on_resize(self, width, height):
        self.background_sprite.center_x = width / 2
        self.background_sprite.center_y = height / 2
        self.background_sprite.scale = width / const.WINDOW_WIDTH * 1.15

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """ Chamado quando um botão do mouse é pressionado. """
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Verifica se o clique foi em cima de algum botão
            buttons_colliding = arcade.get_sprites_at_point((x, y), self.button_list)
            
            if buttons_colliding and not self.developer_mode:
                self.window.show_view(self.window.game_view)