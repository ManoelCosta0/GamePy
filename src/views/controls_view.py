import arcade
from arcade.gui import UIManager
from src import constants as const

class ControlsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.game_view = arcade.get_window().game_view
        self.sprite_list = arcade.SpriteList()
        
        self.background = arcade.Sprite(const.BACKGROUND_IMAGE, center_x=self.window.width / 2, center_y=self.window.height / 2)
        self.widget = arcade.gui.UISpriteWidget(x=410, y=208-30, width=780, height=484, sprite=arcade.Sprite("assets/ui/controls_screen/controls.png"))
        self.return_button = arcade.gui.UITextureButton(
            x=345, y=600, width=163, height=106, 
            texture=arcade.load_texture("assets/ui/util/return_button.png"), 
            texture_hovered=arcade.load_texture("assets/ui/util/return_button_hover.png"),
            scale=const.BUTTON_SCALE-0.1)
        
        checkbox_texture = arcade.load_texture("assets/ui/controls_screen/checkbox.png")
        checkbox_checked_texture = arcade.load_texture("assets/ui/controls_screen/checkbox_checked.png")
        
        for checkbox, position in self.checkbox_positions.items():
            checkbox_widget = arcade.gui.UITextureButton(
                x=self.widget.center_x + position[0], y=self.widget.center_y - position[1], 
                width=35, height=35,
                texture=checkbox_checked_texture if self.game_view.configs[checkbox] else checkbox_texture,
                texture_hovered=None, # Bug, texture_hovered está aparecendo mesmo nula
                scale=0.5
            )
            @checkbox_widget.event("on_click")
            def on_click_checkbox(event, checkbox=checkbox):
                arcade.play_sound(self.window.click_sound)
                if checkbox == "fps":
                    self.game_view.configs["fps"] = not self.game_view.configs["fps"]
                elif checkbox == "fullscreen":
                    self.window.set_fullscreen(not self.window.fullscreen)
                    self.game_view.configs["fullscreen"] = not self.game_view.configs["fullscreen"]
                elif checkbox == "logbox":
                    self.game_view.configs["logbox"] = not self.game_view.configs["logbox"]
                elif checkbox == "perf_graph":
                    self.game_view.configs["perf_graph"] = not self.game_view.configs["perf_graph"]
                
                # Troca de textura está dando problema. Trocar para lógica mais robusta
                if self.game_view.configs[checkbox]:
                    event.source.texture = checkbox_checked_texture
                else:
                    event.source.texture = checkbox_texture

            self.ui_manager.add(checkbox_widget, layer=1)
            
        
        self.sprite_list.append(self.background)
        self.ui_manager.add(self.widget)
        self.ui_manager.add(self.return_button)

    def on_show_view(self):
        self.ui_manager.enable()
        self.background.center_x = self.window.width / 2
        self.background.center_y = self.window.height / 2
        
        @self.return_button.event("on_click")
        def on_click_return_button(event):
            arcade.play_sound(self.window.click_sound)
            self.window.show_view(self.window.pause_view)

    def on_hide_view(self):
        self.ui_manager.disable()

    def on_draw(self):
        self.clear()
        self.sprite_list.draw()
        self.ui_manager.draw()
    
    x = 180
    y = 63

    checkbox_positions = {
        "fps": (x, y + 0),
        "fullscreen": (x, y + 39),
        "logbox": (x, y + 80),
        "perf_graph": (x, y + 120)
        }