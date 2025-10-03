import arcade
from arcade.gui import UIManager
from src import constants as const

class ControlsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.sprite_list = arcade.SpriteList()
        
        self.background = arcade.Sprite(const.BACKGROUND_IMAGE)
        self.widget = arcade.gui.UISpriteWidget(x=410, y=208-30, width=780, height=484, sprite=arcade.Sprite("assets/ui/controls_screen/controls.png"))
        self.return_button = arcade.gui.UITextureButton(
            x=345, y=600, width=163, height=106, 
            texture=arcade.load_texture("assets/ui/util/return_button.png"), 
            texture_hovered=arcade.load_texture("assets/ui/util/return_button_hover.png"),
            scale=const.BUTTON_SCALE-0.1)
        
        self.sprite_list.append(self.background)
        self.ui_manager.add(self.widget)
        self.ui_manager.add(self.return_button)

    def on_show_view(self):
        self.ui_manager.enable()
        self.background.center_x = self.window.width / 2
        self.background.center_y = self.window.height / 2
        
        @self.return_button.event("on_click")
        def on_click_return_button(event):
            self.window.show_view(self.window.pause_view)

    def on_hide_view(self):
        self.ui_manager.disable()

    def on_draw(self):
        self.clear()
        self.sprite_list.draw()
        self.ui_manager.draw()