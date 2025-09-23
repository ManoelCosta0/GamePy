# src/ui/buttons.py
import arcade

class SpriteButton(arcade.Sprite):
    """
    Um sprite que funciona como um botão, com texturas para estado
    normal e quando o mouse está sobre ele (hover).
    """
    def __init__(self, normal_texture_path, hover_texture_path, scale=1):
        # 1. Chame o construtor pai (arcade.Sprite) com o CAMINHO da textura normal.
        #    Isso vai carregar a imagem e criar a textura inicial automaticamente.
        super().__init__(normal_texture_path, scale)
        
        # 2. Guarde uma referência à textura normal que o super() acabou de criar.
        self.normal_texture = self.texture
        
        # 3. Agora, carregue a textura de hover separadamente.
        self.hover_texture = arcade.load_texture(hover_texture_path)
        
        self.is_hovered = False

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