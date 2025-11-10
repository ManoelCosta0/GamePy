import arcade
import random
import os
import json
import time

from src import constants as const
from src.views.game_view import GameView

class MenuView(arcade.View):
    """
    Tela do Menu Principal.
    """
    def __init__(self):
        super().__init__()

        self.ui_manager = arcade.gui.UIManager()
        self.background_sprite_list = arcade.SpriteList()

        self.splash_screen = arcade.Sprite("assets/ui/home_screen/splash_screen.png", center_x=self.window.width / 2, center_y=self.window.height / 2)
        self.background_sprite_list.append(self.splash_screen)

        self.timer = 0.0
        
        self.developer_mode = self.window.developer_mode
        if self.developer_mode: print("Developer mode is ON in MenuView")

        self.new_game_button = arcade.gui.UITextureButton(
            x=950, y=345, width=379, height=142, 
            texture=arcade.load_texture(const.BUTTONS_TEXTURE["new_game"]), 
            texture_hovered=arcade.load_texture(const.BUTTONS_HOVERED_TEXTURE["new_game"]),
            scale=const.BUTTON_SCALE)

        self.continue_button = arcade.gui.UITextureButton(
            x=950, y=245, width=379, height=142, 
            texture=arcade.load_texture(const.BUTTONS_TEXTURE["continue"]), 
            texture_hovered=arcade.load_texture(const.BUTTONS_HOVERED_TEXTURE["continue"]),
            texture_disabled=arcade.load_texture("assets/ui/home_screen/continue_button_disabled.png"),
            scale=const.BUTTON_SCALE)
        
        self.exit_button = arcade.gui.UITextureButton(
            x=950, y=145, width=379, height=142, 
            texture=arcade.load_texture(const.BUTTONS_TEXTURE["exit"]), 
            texture_hovered=arcade.load_texture(const.BUTTONS_HOVERED_TEXTURE["exit"]),
            scale=const.BUTTON_SCALE)
        
        self.intro_phase = ""

    def on_show_view(self):
        self.ui_manager.enable()
        if not os.path.exists("saves/save.json"): self.continue_button.disabled = True

        @self.new_game_button.event("on_click")
        def on_click_new_game_button(event):
            arcade.play_sound(self.window.click_sound, volume=self.window.volume)
            self.window.show_view(self.window.classes_view)

        @self.continue_button.event("on_click")
        def on_click_continue_button(event):
            arcade.play_sound(self.window.click_sound, volume=self.window.volume)
            self.load_game()
            
        @self.exit_button.event("on_click")
        def on_click_exit_button(event):
            arcade.play_sound(self.window.click_sound, volume=self.window.volume)
            arcade.close_window()

    def on_draw(self):
        self.clear()
        self.background_sprite_list.draw() 
        self.ui_manager.draw()
        
    def on_hide_view(self):
        self.ui_manager.disable()
    
    def on_resize(self, width, height):
        self.splash_screen.center_x = width / 2
        self.splash_screen.center_y = height / 2

    def load_game(self):
        save = {}
        with open("saves/save.json") as file:
            save = json.load(file)
        
        self.window.game_view = GameView()
        self.window.game_view.player.load_player(save)

        self.window.game_view.load_game()
        self.window.show_view(self.window.game_view)

    def on_update(self, delta_time):
        self.timer += delta_time
        if self.developer_mode and self.timer >= 0.2:
            if not self.window.fullscreen: 
                self.window.set_fullscreen(True)
                self.load_game()
            return
        if self.timer >= 0.1 and self.intro_phase == "":
            self.window.set_fullscreen(True)
            self.intro_phase = "Splash Screen"
        elif self.timer >= 4.0 and self.intro_phase == "Splash Screen":
            self.intro_phase = "Transition"
            self.timer = 0.0
            background = arcade.Sprite(f"assets/ui/home_screen/home_background_1.png", center_x=self.window.width / 2, center_y=self.window.height / 2)
            self.background_sprite_list.insert(0, background)
        elif self.intro_phase == "Transition":
            self.splash_screen.alpha -= 5
            if self.splash_screen.alpha <= 0:
                self.intro_phase = "Main Menu"
        elif self.timer >= 1.0 and self.intro_phase == "Main Menu":
            self.intro_phase = None
            self.splash_screen.remove_from_sprite_lists()
            self.ui_manager.add(self.new_game_button)
            self.ui_manager.add(self.continue_button)
            self.ui_manager.add(self.exit_button)