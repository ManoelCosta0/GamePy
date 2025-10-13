import arcade
import os
import json

from src import constants
from src.views.game_view import GameView

class ClassesView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = arcade.gui.UIManager()
        self.sprite_list = arcade.SpriteList()
        
        self.background = arcade.Sprite(constants.BACKGROUND_IMAGE, center_x=self.window.width/2, center_y=self.window.height/2)
        
        self.widget = arcade.gui.UISpriteWidget(x=410, y=208-30, width=780, height=484, sprite=arcade.Sprite("assets/ui/classes_screen/classes.png"))
        
        self.return_button = arcade.gui.UITextureButton(
            x=345, y=600, width=163, height=106, 
            texture=arcade.load_texture("assets/ui/util/return_button.png"), 
            texture_hovered=arcade.load_texture("assets/ui/util/return_button_hover.png"),
            scale=constants.BUTTON_SCALE-0.1)
        
        self.select_warrior_button = arcade.gui.UITextureButton(
            x=580, y=230, width=99, height=37, 
            texture=arcade.load_texture("assets/ui/classes_screen/select_button.png"), 
            texture_hovered=arcade.load_texture("assets/ui/classes_screen/select_button_hover.png"),
            scale=1.0)
        
        self.select_assassin_button = arcade.gui.UITextureButton(
            x=905, y=230, width=99, height=37, 
            texture=arcade.load_texture("assets/ui/classes_screen/select_button.png"), 
            texture_hovered=arcade.load_texture("assets/ui/classes_screen/select_button_hover.png"),
            scale=1.0)
        
        self.sprite_list.append(self.background)
        
        self.ui_manager.add(self.select_warrior_button, layer = 1)
        self.ui_manager.add(self.select_assassin_button, layer = 1)

        self.ui_manager.add(self.widget, layer = 0)
        self.ui_manager.add(self.return_button)

    def on_show_view(self):
        self.ui_manager.enable()
        self.background.center_x = self.window.width / 2
        self.background.center_y = self.window.height / 2
        
        @self.return_button.event("on_click")
        def on_click_return_button(event):
            arcade.play_sound(self.window.click_sound)
            self.window.show_view(self.window.menu_view)
            
        @self.select_warrior_button.event("on_click")
        def on_click_warrior_button(event):
            arcade.play_sound(self.window.click_sound)
            self.create_save_file("Warrior")
        
        @self.select_assassin_button.event("on_click")
        def on_click_assassin_button(event):
            arcade.play_sound(self.window.click_sound)
            self.create_save_file("Assassin")
            
    def on_draw(self):
        self.clear()
        self.sprite_list.draw()
        self.ui_manager.draw()
    
    def on_hide_view(self):
        self.ui_manager.disable()
        
    def create_save_file(self, class_):
        if not os.path.exists("saves"):
            os.mkdir("saves")
            
        save_data = {
            "class": class_,
            "inventory": [],
            "equipped_weapon": self.new_game_configs[class_]["equipped_weapon"],
            "max_hp": self.new_game_configs[class_]["max_hp"],
            "speed": self.new_game_configs[class_]["speed"],
            "attack_cooldown": self.new_game_configs[class_]["attack_cooldown"],
            "level": 1,
            "current_xp": 0,
            "position": (600, 1500)
        }
        with open("saves/save.json", "w") as save_file:
            json.dump(save_data, save_file, indent=4)

        self.window.game_view = GameView()
        self.window.game_view.player.load_player(save_data)
        self.window.show_view(self.window.game_view)

    new_game_configs = {
        "Warrior": {
            "max_hp": 150,
            "speed": 4,
            "attack_cooldown": 0.08,
            "equipped_weapon": "Espada Velha"
        },
        "Assassin": {
            "max_hp": 80,
            "speed": 7,
            "attack_cooldown": 0.05,
            "equipped_weapon": "Espada Velha" # Temporário
        }
    }