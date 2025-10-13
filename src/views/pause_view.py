import arcade
from src import constants as const
from arcade.gui import UIManager
from src.views.controls_view import ControlsView

class PauseView(arcade.View):
    """
    Tela de Pausa do Jogo.
    """
    def __init__(self):
        super().__init__()

        self.ui_manager = UIManager()
        self.sprite_list = arcade.SpriteList()
        
        self.developer_mode = False
        if self.developer_mode: print("Developer mode is ON in PauseView")
        
        self.background = arcade.Sprite(const.BACKGROUND_IMAGE, center_x=self.window.width / 2, center_y=self.window.height / 2)

        self.resume_button = arcade.gui.UITextureButton(
            x=self.background.center_x-128, 
            y=const.BUTTONS_POSITION_Y["resume"],
            width=256, height=128,
            texture=arcade.load_texture(const.BUTTONS_TEXTURE["resume"]),
            texture_hovered=arcade.load_texture(const.BUTTONS_HOVERED_TEXTURE["resume"]),
            scale=const.BUTTON_SCALE)

        self.controls_button = arcade.gui.UITextureButton(
            x=self.background.center_x-128, 
            y=const.BUTTONS_POSITION_Y["controls"], 
            width=256, height=128,
            texture=arcade.load_texture(const.BUTTONS_TEXTURE["controls"]),
            texture_hovered=arcade.load_texture(const.BUTTONS_HOVERED_TEXTURE["controls"]),
            scale=const.BUTTON_SCALE)

        self.inventory_button = arcade.gui.UITextureButton(
            x=self.background.center_x-128, 
            y=const.BUTTONS_POSITION_Y["inventory"], 
            width=256, height=128,
            texture=arcade.load_texture(const.BUTTONS_TEXTURE["inventory"]),
            texture_hovered=arcade.load_texture(const.BUTTONS_HOVERED_TEXTURE["inventory"]),
            scale=const.BUTTON_SCALE)

        self.exit_button = arcade.gui.UITextureButton(
            x=self.background.center_x-128, 
            y=const.BUTTONS_POSITION_Y["exit"], 
            width=256, height=128,
            texture=arcade.load_texture(const.BUTTONS_TEXTURE["exit"]),
            texture_hovered=arcade.load_texture(const.BUTTONS_HOVERED_TEXTURE["exit"]),
            scale=const.BUTTON_SCALE)

        self.sprite_list.append(self.background)
        self.ui_manager.add(self.resume_button)
        self.ui_manager.add(self.inventory_button)
        self.ui_manager.add(self.exit_button)
        self.ui_manager.add(self.controls_button)

    def on_draw(self):
        """ Desenha todos os elementos da View de Pausa. """
        self.clear()
        self.sprite_list.draw()
        self.ui_manager.draw()

    def on_show_view(self):
        """ Chamado quando esta View é mostrada. """
        self.ui_manager.enable()
        self.background.center_x = self.window.width / 2
        self.background.center_y = self.window.height / 2
        
        @self.resume_button.event("on_click")
        def on_click_resume(event):
            arcade.play_sound(self.window.click_sound)
            self.window.show_view(self.window.game_view)

        @self.inventory_button.event("on_click")
        def on_click_inventory(event):
            arcade.play_sound(self.window.click_sound)
            self.window.show_view(self.window.inventory_view)
            self.window.inventory_view.origin = self

        @self.exit_button.event("on_click")
        def on_click_exit(event):
            if self.developer_mode:
                self.window.close()
                return
            arcade.play_sound(self.window.click_sound)
            self.window.show_view(self.window.menu_view)

        @self.controls_button.event("on_click")
        def on_click_controls(event):
            arcade.play_sound(self.window.click_sound)
            self.window.show_view(ControlsView())

    def on_hide_view(self):
        """ Chamado quando esta View é escondida. """
        self.ui_manager.disable()
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.play_sound(self.window.click_sound)
            self.window.show_view(self.window.game_view)