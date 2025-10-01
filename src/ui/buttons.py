# src/ui/buttons.py
import arcade
import src.constants as const

class SpriteButton(arcade.Sprite):
    """
    Classe para botões do jogo
    """
    def __init__(self, name, normal_texture_path, hover_texture_path):
        super().__init__(normal_texture_path, const.BUTTON_SCALE)
        
        self.normal_texture = self.texture
        self.hover_texture = arcade.load_texture(hover_texture_path)
        
        self.name = name
        self.is_hovered = False

        self.center_x = const.BUTTONS_POSITION_X[name]
        self.center_y = const.BUTTONS_POSITION_Y[name]

    def on_hover(self):
        """ Chamado quando o mouse entra na área do botão. """
        if not self.is_hovered:
            self.texture = self.hover_texture
            self.is_hovered = True

    def on_unhover(self):
        """ Chamado quando o mouse sai da área do botão. """
        if self.is_hovered:
            self.texture = self.normal_texture
            self.is_hovered = False