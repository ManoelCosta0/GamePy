import arcade
import random
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
        # --- AQUI: Reintroduza uma SpriteList para os backgrounds ---
        self.background_sprite_list = arcade.SpriteList() 
        
        # --- Configurações da transição de Background ---
        self.background_image_paths = [] 
        for i in range(1, 6):
            self.background_image_paths.append(f"assets/ui/home_screen/home_background_{i}.png")
        
        self.current_bg_index = random.randint(0, len(self.background_image_paths) - 1)
        # Inicializa next_bg_index para que bg_sprite_top tenha uma imagem válida.
        # Ele será atualizado corretamente no primeiro ciclo do on_update.
        self.next_bg_index = (self.current_bg_index + 1) % len(self.background_image_paths) 

        # Sprites dedicados para os backgrounds
        self.bg_sprite_bottom = arcade.Sprite(self.background_image_paths[self.current_bg_index])
        self.bg_sprite_top = arcade.Sprite(self.background_image_paths[self.next_bg_index])
        
        # Configuração inicial do sprite de cima (transparente no começo)
        self.bg_sprite_top.alpha = 0

        # --- AQUI: Adicione os sprites de background à nova SpriteList ---
        # A ordem é importante: bottom (fundo) primeiro, top (frente) depois.
        self.background_sprite_list.append(self.bg_sprite_bottom)
        self.background_sprite_list.append(self.bg_sprite_top)

        self.is_transitioning = False
        self.transition_progress = 0.0

        self.TRANSITION_DURATION = 2.0
        self.IMAGE_DISPLAY_DURATION = 60.0
        self.timer = 0.0

        # --- SEU CÓDIGO DE BOTÕES (SEM ALTERAÇÕES) ---
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
        
        self.exit_button = arcade.gui.UITextureButton(
            x=310, y=245, width=379, height=142, 
            texture=arcade.load_texture(const.BUTTONS_TEXTURE["exit"]), 
            texture_hovered=arcade.load_texture(const.BUTTONS_HOVERED_TEXTURE["exit"]),
            scale=const.BUTTON_SCALE)

        self.ui_manager.add(self.new_game_button)
        self.ui_manager.add(self.continue_button)
        self.ui_manager.add(self.exit_button)

    def on_show_view(self):
        self.ui_manager.enable()
        self.on_resize(self.window.width, self.window.height) 
        if not os.path.exists("saves/save.json"): self.continue_button.disabled = True

        @self.new_game_button.event("on_click")
        def on_click_new_game_button(event):
            arcade.play_sound(self.window.click_sound)
            self.window.show_view(self.window.classes_view)

        @self.continue_button.event("on_click")
        def on_click_continue_button(event):
            arcade.play_sound(self.window.click_sound)
            self.load_game()
            
        @self.exit_button.event("on_click")
        def on_click_exit_button(event):
            arcade.play_sound(self.window.click_sound)
            arcade.close_window()

    def on_draw(self):
        self.clear()
        # --- AQUI: Desenhe a SpriteList dos backgrounds ---
        self.background_sprite_list.draw() 
        self.ui_manager.draw()
        
    def on_hide_view(self):
        self.ui_manager.disable()
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
            self.on_resize(self.window.width, self.window.height)
        
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
        
    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)

        for bg_sprite in [self.bg_sprite_bottom, self.bg_sprite_top]:
            if bg_sprite and bg_sprite.texture:
                scale_w = width / bg_sprite.texture.width
                scale_h = height / bg_sprite.texture.height
                scale = max(scale_w, scale_h) 
                
                bg_sprite.scale = scale
                bg_sprite.center_x = width / 2
                bg_sprite.center_y = height / 2

    def on_update(self, delta_time):
        self.timer += delta_time

        if not self.is_transitioning:
            if self.timer >= self.IMAGE_DISPLAY_DURATION:
                self.is_transitioning = True
                self.transition_progress = 0.0 
                self.timer = 0.0
                
                self.current_bg_index = (self.current_bg_index + 1) % len(self.background_image_paths)
                self.next_bg_index = (self.current_bg_index + 1) % len(self.background_image_paths)
                
                self.bg_sprite_top.texture = arcade.load_texture(self.background_image_paths[self.next_bg_index])
                self.bg_sprite_top.alpha = 0
                self.on_resize(self.window.width, self.window.height)

        if self.is_transitioning:
            self.transition_progress += delta_time / self.TRANSITION_DURATION
            
            if self.transition_progress >= 1.0:
                self.transition_progress = 1.0
                self.is_transitioning = False
                
                self.bg_sprite_bottom.texture = self.bg_sprite_top.texture
                self.bg_sprite_bottom.alpha = 255
                
                self.bg_sprite_top.alpha = 0 
            
            self.bg_sprite_top.alpha = int(self.transition_progress * 255)
            if self.bg_sprite_top.alpha > 255: self.bg_sprite_top.alpha = 255