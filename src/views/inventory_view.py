import arcade
from src.game_objects.item import Item
from src import constants

class InventoryView(arcade.View):
    """
    Tela de Inventário do Jogo.
    """
    def __init__(self):
        super().__init__()
        
        self.origin = None
        
        self.sprite_list = arcade.SpriteList()
        self.background = arcade.Sprite(constants.BACKGROUND_IMAGE)
        self.sprite_list.append(self.background)
        
        self.ui_manager = arcade.gui.UIManager()
        self.background_sprite = arcade.gui.UISpriteWidget(
            x=0, y=0,
            width=1831/2, height=1139/2,
            sprite=arcade.Sprite("assets/ui/inventory_screen/inventory_background.png", scale=0.5)
        )
        self.background_sprite.center_on_screen()
        self.background_sprite.center_y -= 50
        self.grid_1 = arcade.gui.UIGridLayout(
            x=self.background_sprite.center_x-190, y=-10, 
            width=self.background_sprite.width, height=self.background_sprite.height,
            align_horizontal="left", align_vertical="top",
            horizontal_spacing=20, vertical_spacing=20,
            column_count=6, row_count=2
        )
        self.grid_2 = arcade.gui.UIGridLayout(
            x=self.background_sprite.center_x-190, y=-10-(2*137/2)-40, 
            width=self.background_sprite.width, height=self.background_sprite.height,
            align_horizontal="left", align_vertical="top",
            horizontal_spacing=20, vertical_spacing=20,
            column_count=4, row_count=2
        )
        self.weapon_slot = arcade.gui.UITextureButton(
            x=self.background_sprite.center_x - 345, y=self.background_sprite.center_y - 55,
            width=138/2.3, height=137/2.3,
            texture=arcade.load_texture("assets/ui/inventory_screen/slot.png"),
            texture_hovered=arcade.load_texture("assets/ui/inventory_screen/slot_hover.png")
        )
        self.ui_manager.add(self.background_sprite)
        self.background_sprite.add(self.weapon_slot)
        self.ui_manager.add(self.grid_1, layer=1)
        self.ui_manager.add(self.grid_2, layer=1)
        self.generate_grid()

    def on_show_view(self):
        self.ui_manager.enable()
        self.background.center_x, self.background.center_y = self.window.width / 2, self.window.height / 2

    def on_hide_view(self):
        self.ui_manager.disable()

    def on_draw(self):
        """ Desenha todos os elementos da View. """
        self.clear()
        self.sprite_list.draw()
        self.ui_manager.draw()
    
    def on_update(self, delta_time):
        self.sprite_list.update()
    
    def on_key_press(self, key, modifiers):
        """ Volta para a View de origem ao pressionar a tecla ESCAPE. """
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.origin)
        elif key == arcade.key.I:
            self.window.show_view(self.window.game_view)
            
    def on_mouse_press(self, x, y, button, modifiers):
        pos_x = x - self.background_sprite.center_x
        pos_y = y - self.background_sprite.center_y
        print(f"Mouse pressionado em ({pos_x}, {pos_y})")
        
    def generate_grid(self):
        """Gera os dois grids de slots do inventário."""
        for column in range(6):
            for row in range(2):
                slot = arcade.gui.UITextureButton(
                    width=138/2, height=137/2,
                    texture=arcade.load_texture("assets/ui/inventory_screen/slot.png"),
                    texture_hovered=arcade.load_texture("assets/ui/inventory_screen/slot_hover.png")
                )
                @slot.event("on_click")
                def on_click(event):
                    print(f"Fonte do evento: {event.source}")
                self.grid_1.add(slot, column=column, row=row)
        
        for column in range(4): 
            for row in range(2):
                slot = arcade.gui.UITextureButton(
                    width=138/2, height=137/2,
                    texture=arcade.load_texture("assets/ui/inventory_screen/slot.png"),
                    texture_hovered=arcade.load_texture("assets/ui/inventory_screen/slot_hover.png")
                )
                @slot.event("on_click")
                def on_click(event):
                    print(f"Fonte do evento: {event.source}")
                self.grid_2.add(slot, column=column, row=row)
    
    def initialize_inventory(self, class_name, speed, damage):
        """Inicializa o inventário com a classe, os itens e os stats do jogador."""
        
        # Classe
        self.class_icon = arcade.gui.UISpriteWidget(
            x=self.background_sprite.center_x - 365, y=self.background_sprite.center_y + 68,
            width=198/2, height=193/2,
            sprite=arcade.Sprite(f"assets/ui/inventory_screen/{class_name}_icon.png")
            )
        self.ui_manager.add(self.class_icon, layer=1)

        arcade.load_font("assets/fonts/SuperLegendBoy.ttf")

        self.player_class = arcade.gui.UILabel(
            text=f"Class: {class_name}",
            x=self.background_sprite.center_x - 390, y=self.background_sprite.center_y - 150,
            width=348/2, height=20,
            font_name="alagard", font_size=15, text_color=arcade.color.WHITE,
        )
        self.player_speed = arcade.gui.UILabel(
            text=f"Speed: {speed}",
            x=self.background_sprite.center_x - 390, y=self.background_sprite.center_y - 175,
            width=348/2, height=20,
            font_name="alagard", font_size=15, text_color=arcade.color.WHITE,
        )
        self.player_damage = arcade.gui.UILabel(
            text=f"Damage: {damage}",
            x=self.background_sprite.center_x - 390, y=self.background_sprite.center_y - 200,
            width=348/2, height=20,
            font_name="alagard", font_size=15, text_color=arcade.color.WHITE,
        )
        self.ui_manager.add(self.player_class, layer=1)
        self.ui_manager.add(self.player_speed, layer=1)
        self.ui_manager.add(self.player_damage, layer=1)
