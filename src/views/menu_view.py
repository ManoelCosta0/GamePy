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

        self.background_sprite = arcade.Sprite(const.BACKGROUND_IMAGE)
        
        new_game_button = SpriteButton(
            name="new_game",
            normal_texture_path=const.BUTTONS_TEXTURE["new_game"],
            hover_texture_path=const.BUTTONS_HOVERED_TEXTURE["new_game"])
        
        continue_button = SpriteButton(
            name="continue",
            normal_texture_path=const.BUTTONS_TEXTURE["continue"],
            hover_texture_path=const.BUTTONS_HOVERED_TEXTURE["continue"])

        self.general_sprite_list.append(self.background_sprite)
        self.button_list.append(new_game_button)
        self.button_list.append(continue_button)
        
    def on_show_view(self):
        """ Chamado quando esta View é mostrada. """
        self.clear()
        arcade.set_background_color(arcade.color.BLACK) # Um fundo preto para garantir
    
    def on_resize(self, width, height):
        self.background_sprite.center_x = width / 2
        self.background_sprite.center_y = height / 2
        self.background_sprite.scale = width / const.WINDOW_WIDTH

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """ Chamado quando um botão do mouse é pressionado. """
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Verifica se o clique foi em cima de algum botão
            buttons_colliding = arcade.get_sprites_at_point((x, y), self.button_list)
            
            if buttons_colliding and not self.developer_mode:
                match buttons_colliding[0].name:
                    case "new_game":
                        self.window.show_view(self.window.game_view)
                    case "continue":
                        self.window.log_box.add_message("Funcionalidade por vir")