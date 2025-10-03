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

        self.setup()

    def setup(self):
        """ Configura os componentes da View de Pausa. """
        self.background_sprite = arcade.Sprite(const.BACKGROUND_IMAGE)
        self.background_sprite.center_x = self.window.width / 2
        self.background_sprite.center_y = self.window.height / 2

        resume_button = SpriteButton(
            name="resume",
            normal_texture_path=const.BUTTONS_TEXTURE["resume"],
            hover_texture_path=const.BUTTONS_HOVERED_TEXTURE["resume"])
        
        controls_button = SpriteButton(
            name="controls",
            normal_texture_path=const.BUTTONS_TEXTURE["controls"],
            hover_texture_path=const.BUTTONS_HOVERED_TEXTURE["controls"])

        inventory_button = SpriteButton(
            name="inventory",
            normal_texture_path=const.BUTTONS_TEXTURE["inventory"],
            hover_texture_path=const.BUTTONS_HOVERED_TEXTURE["inventory"])

        exit_button = SpriteButton(
            name="exit",
            normal_texture_path=const.BUTTONS_TEXTURE["exit"],
            hover_texture_path=const.BUTTONS_HOVERED_TEXTURE["exit"])

        self.general_sprite_list.append(self.background_sprite)
        self.button_list.append(resume_button)
        self.button_list.append(inventory_button)
        self.button_list.append(exit_button)
        self.button_list.append(controls_button)

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
                    case "resume":
                        self.window.show_view(self.window.game_view)
                    case "inventory":
                        self.window.show_view(self.window.inventory_view)
                    case "exit":
                        self.window.show_view(self.window.menu_view)
                    case "controls":
                        self.window.log_box.add_message("Funcionalidade por vir")