import arcade
import os
import json

from src import constants as const
from src.views.game_view import GameView

class MenuView(arcade.View):
    """
    Tela do Menu Principal.
    """
    def __init__(self):
        super().__init__()

        self.ui_manager = arcade.gui.UIManager()
        self.sprite_list = arcade.SpriteList()
        
        self.background_sprite = arcade.Sprite("assets/ui/home_background.png")
        
        self.new_game_button = arcade.gui.UITextureButton(
            x=310, y=445, width=379, height=142, 
            texture=arcade.load_texture(const.BUTTONS_TEXTURE["new_game"]), 
            texture_hovered=arcade.load_texture(const.BUTTONS_HOVERED_TEXTURE["new_game"]),
            scale=const.BUTTON_SCALE)

        self.continue_button = arcade.gui.UITextureButton(
            x=310, y=345, width=379, height=142, 
            texture=arcade.load_texture(const.BUTTONS_TEXTURE["continue"]), 
            texture_hovered=arcade.load_texture(const.BUTTONS_HOVERED_TEXTURE["continue"]),
            texture_disabled=arcade.load_texture("assets/ui/home_screen/continue_button_disabled.png"),
            scale=const.BUTTON_SCALE)

        self.sprite_list.append(self.background_sprite)
        self.ui_manager.add(self.new_game_button)
        self.ui_manager.add(self.continue_button)

    def on_show_view(self):
        """ Chamado quando esta View é mostrada. """
        self.ui_manager.enable()
        self.background_sprite.center_x = self.window.width / 2
        self.background_sprite.center_y = self.window.height / 2

        if not os.path.exists("saves/save.json"): self.continue_button.disabled = True

        @self.new_game_button.event("on_click")
        def on_click_new_game_button(event):
            self.window.show_view(self.window.classes_view)

        @self.continue_button.event("on_click")
        def on_click_continue_button(event):
            self.load_game()

    def on_draw(self):
        """ Desenha a View. """
        self.clear()
        self.sprite_list.draw()
        self.ui_manager.draw()
        
    def on_hide_view(self):
        self.ui_manager.disable()
        
    def load_game(self):
        save = {}
        with open("saves/save.json") as file:
            save = json.load(file)
        
        game_view = GameView(save["class"])
        game_view.player.load_player(
            save["inventory"], 
            save["equipped_weapon"], 
            save["position"],
            save["max_hp"],
            save["speed"])
        
        self.window.game_view = game_view
        self.window.show_view(game_view)