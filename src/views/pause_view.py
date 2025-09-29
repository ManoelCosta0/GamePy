import arcade
from src import constants as const
from src.views.view import View
from src.ui.buttons import SpriteButton

class PauseView(View):
    """
    Tela de Pausa do Jogo.
    """
    def __init__(self):
        super().__init__()

        self.background_sprite = arcade.Sprite("assets/UI/pause_background.png", scale=1)
        self.background_sprite.center_x = self.window.width / 2
        self.background_sprite.center_y = self.window.height / 2

        resume_button = SpriteButton(
            name="continue",
            normal_texture_path="assets/UI/continue_button_normal.png",
            hover_texture_path="assets/UI/continue_button_hover.png")

        inventory_button = SpriteButton(
            name="inventory",
            normal_texture_path="assets/UI/inventory_button_normal.png",
            hover_texture_path="assets/UI/inventory_button_hover.png")

        exit_button = SpriteButton(
            name="exit",
            normal_texture_path="assets/UI/sair_button_normal.png",
            hover_texture_path="assets/UI/sair_button_hover.png")

        self.general_sprite_list.append(self.background_sprite)
        self.button_list.append(resume_button)
        self.button_list.append(inventory_button)
        self.button_list.append(exit_button)

    def on_show_view(self):
        """ Chamado quando esta View é mostrada. """
        arcade.set_background_color(arcade.color.BLACK)
        self.background_sprite.center_x = self.window.width / 2
        self.background_sprite.center_y = self.window.height / 2

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """ Chamado quando um botão do mouse é pressionado. """
        if button == arcade.MOUSE_BUTTON_LEFT:

            button_colliding = arcade.get_sprites_at_point((x, y), self.button_list)

            if button_colliding and not self.developer_mode:
                match button_colliding[0].name:
                    case "continue":
                        self.window.show_view(self.game_view)
                    case "inventory":
                        self.window.show_view(self.inventory_view)
                    case "exit":
                        self.window.show_view(self.menu_view)