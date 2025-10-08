import arcade
'''
1. Construtor adiciona HUD na tela
2. Função de modificar valores do HUD
3. Botão de menu para abrir inventário (inicialmente não funciona)
'''
class HUD:
    def __init__(self, ui_manager):
        self.ui_manager = ui_manager
        self.hud_sprite = arcade.gui.UISpriteWidget(
            x=15, y=self.ui_manager.window.height - 15 - 276/2.5,
            width=613/2.5, height=276/2.5,
            sprite = arcade.Sprite("assets/ui/hud/hud_background.png"))
        
        self.menu_button = arcade.gui.UITextureButton(
            x=115, y=self.ui_manager.window.height - 89 - 69/2.5,
            width=322/2.5, height=69/2.5,
            texture=arcade.load_texture("assets/ui/hud/menu_button.png"),
            texture_hovered=arcade.load_texture("assets/ui/hud/menu_button_hovered.png"))
        
        self.level_label = arcade.gui.UILabel(
            text="19",
            x=55, y=self.ui_manager.window.height - 105,
            width=50, height=50,
            font_name = "alagard",
            font_size=45, 
            text_color=arcade.color.BLACK,
            align="center")

        self.xp_label = arcade.gui.UILabel(
            text="Xp. 0/100",
            x=130, y=self.ui_manager.window.height - 113,
            width=100, height=50,
            font_name = "alagard",
            font_size=14, 
            text_color=arcade.color.BLACK,
            align="center")

        @self.menu_button.event("on_click")
        def on_click(event):
            print("Menu button clicked! (Functionality not implemented yet)")
        
        self.ui_manager.add(self.hud_sprite)
        self.ui_manager.add(self.menu_button, layer=1)
        self.ui_manager.add(self.level_label, layer=1)
        self.ui_manager.add(self.xp_label, layer=1)
    
    def set_level(self, level: int):
        self.level_label.text = str(level)

    def set_xp(self, current_xp: int, max_xp: int):
        self.xp_label.text = f"Xp. {current_xp}/{max_xp}"