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
        
        self.hovered_slot_texture = arcade.load_texture("assets/ui/inventory_screen/slot_hover.png")
        self.normal_slot_texture = arcade.load_texture("assets/ui/inventory_screen/slot.png")
        
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
            texture=self.normal_slot_texture,
            texture_hovered=self.hovered_slot_texture
        )
        self.weapon_slot.item = None  # Inicializa o atributo item como None
        self.organize_button = arcade.gui.UITextureButton(
            x=self.background_sprite.center_x+50, y=self.background_sprite.center_y - 230,
            width=199/2, height=59/2,
            texture=arcade.load_texture("assets/ui/inventory_screen/organize_button.png"),
            texture_hovered=arcade.load_texture("assets/ui/inventory_screen/organize_button_hover.png")
        )
        self.item_desc = arcade.gui.UIWidget()
        
        self.ui_manager.add(self.background_sprite)
        self.ui_manager.add(self.weapon_slot, layer=1)
        self.ui_manager.add(self.grid_1, layer=1)
        self.ui_manager.add(self.grid_2, layer=1)
        self.ui_manager.add(self.organize_button, layer=2)
        self.ui_manager.add(self.item_desc, layer=2)
        
        self.generate_grid(self.grid_1)
        self.generate_grid(self.grid_2, columns=4)
        
        self.use_button = None
        self.drop_button = None
        self.clicked_slot = None

    #----------------------
    # Eventos da View
    #----------------------
    
    def on_show_view(self):
        self.ui_manager.enable()
        self.background.center_x, self.background.center_y = self.window.width / 2, self.window.height / 2
        
        @self.weapon_slot.event("on_click")
        def on_click_weapon_slot(event):
            src = event.source
            self.load_item(src, func="unequip")
        
        self.update_stats()

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
            self.window.show_view(self.origin) if self.origin else self.window.show_view(self.window.game_view)
        elif key == arcade.key.I:
            self.window.show_view(self.window.game_view)
            
    def on_mouse_press(self, x, y, button, modifiers):
        pos_x = x - self.background_sprite.center_x
        pos_y = y - self.background_sprite.center_y
        print(f"Mouse pressionado em ({pos_x}, {pos_y})")
    
    #----------------------
    # Funções de inicialização do Inventário
    #----------------------
    
    def generate_grid(self, grid, columns=6, rows=2):
        """Gera os dois grids de slots do inventário."""
        for row in range(rows):
            for column in range(columns):
                slot = arcade.gui.UITextureButton(
                    width=138/2, height=137/2,
                    texture=self.normal_slot_texture,
                    texture_hovered=self.hovered_slot_texture
                )
                @slot.event("on_click")
                def on_click(event):
                    src = event.source
                    self.load_item(src, func="equip")
                grid.add(slot, column=column, row=row)

    def initialize_inventory(self, items, class_name, speed, equipped, damage):
        """Inicializa o inventário com a classe, os itens e os stats do jogador."""
        
        # Classe
        self.class_icon = arcade.gui.UISpriteWidget(
            x=self.background_sprite.center_x - 365, y=self.background_sprite.center_y + 68,
            width=198/2, height=193/2,
            sprite=arcade.Sprite(f"assets/ui/inventory_screen/{class_name}_icon.png")
            )
        self.ui_manager.add(self.class_icon, layer=1)
        
        # Stats
        self.create_text_box(
            parent=self.background_sprite,
            x=self.background_sprite.center_x - 390,
            start_y=self.background_sprite.center_y - 140,
            width=348/2, spacing=10, font_size=14,
            texts=[
                f"Class: {class_name}",
                f"Speed: {speed}",
                f"Damage: {damage}"
            ]
        )
        
        # Items
        for item in items:
            self.add_item_to_grid(item)
            
        # Weapon Slot
        if equipped:
            self.set_equipped_item(Item(equipped))

    #----------------------
    # Funções de operações do inventário
    #----------------------
    
    def add_item_to_grid(self, item: Item):
        """Adiciona um item ao grid do inventário."""
        slot = self.get_empty_slot(item.name)
        if slot and (not hasattr(slot, 'item') or slot.item is None):
            item_icon = arcade.gui.UISpriteWidget(
                x=0, y=0,
                width=114/2, height=114/2,
                sprite=item
            )
            slot.item = item
            slot.add(item_icon)
        elif slot and hasattr(slot, 'item') and item.stackable and slot.item.name == item.name:
            slot.item.amount += 1
        else:
            self.window.log_box.add_message("Inventário cheio!")

    def remove_item_from_grid(self, item: Item):
        """Remove um item do grid do inventário."""
        # Remove do backend
        player = self.window.game_view.player
        player.inventory.remove_item(item)
        
        # Remove o item na interface
        self.clicked_slot.item = None
        self.clicked_slot.remove(self.clicked_slot.children[1])
        
    def set_equipped_item(self, item: Item):
        """Define o item equipado no slot de arma."""
        # Equipa no backend
        player = self.window.game_view.player
        player.equip_weapon(item)
        
        # Equipa na interface
        item_icon = arcade.gui.UISpriteWidget(
            x=0, y=0,
            width=114/2.3, height=114/2.3,
            sprite=item
        )
        self.weapon_slot.item = item
        self.weapon_slot.add(item_icon)
        self.update_stats()
        
    def equip_item(self, item: Item):
        """Equipa um item no slot de arma."""
        # Desequipa o item atual, se houver
        self.unequip_item()
        
        # Remove o item do inventário
        self.remove_item_from_grid(item)
        
        self.set_equipped_item(item)
        
    def unequip_item(self):
        """Desequipa o item do slot de arma."""
        # Desequipa no backend
        player = self.window.game_view.player
        player.unequip_weapon()
        
        # Desequipa na interface
        if hasattr(self.weapon_slot, 'item') and self.weapon_slot.item:
            self.weapon_slot.item = None
            self.weapon_slot.remove(self.weapon_slot.children[1])
        self.update_stats()

    #-------------------------
    # Funções de interação com itens
    #-------------------------
    
    def load_item_desc(self, item: Item):
        """Carrega a descrição do item selecionado."""
        self.create_text_box(
            parent=self.item_desc,
            x=self.background_sprite.center_x + 195,
            start_y=self.background_sprite.center_y - 100,
            width=200, spacing=15, font_size=12,
            texts=[
                f"Name: {item.name}",
                f"Amount: {item.amount}",
                f"Damage: {item.get_damage()}",
                f"Description: {item.description}"
            ]
        )
        
    def load_item_buttons(self, equip_or_unequip: str="equip"):
        """Carrega os botões de ação do item selecionado."""
        
        self.organize_button.center_x = self.background_sprite.center_x - 50
        
        self.drop_button = arcade.gui.UITextureButton(
            x=self.organize_button.center_x + 60, y=self.background_sprite.center_y - 230,
            width=133/2, height=56/2,
            texture=arcade.load_texture("assets/ui/inventory_screen/drop_button.png"),
        )
        self.use_button = arcade.gui.UITextureButton(
            x=self.drop_button.center_x + 40, y=self.background_sprite.center_y - 230,
            width=175/2, height=59/2,
            texture=arcade.load_texture(f"assets/ui/inventory_screen/{equip_or_unequip}_button.png"),
        )
        self.ui_manager.add(self.use_button, layer=2)
        self.ui_manager.add(self.drop_button, layer=2)
        
        @self.drop_button.event("on_click")
        def on_click_drop(event):
            if self.clicked_slot and hasattr(self.clicked_slot, 'item') and self.clicked_slot != self.weapon_slot:
                item = self.clicked_slot.item
                self.remove_item_from_grid(item)
                self.close_item_desc()
                self.clicked_slot = None
            elif self.clicked_slot == self.weapon_slot:
                self.window.log_box.add_message("Não é possível dropar o item equipado!")

        @self.use_button.event("on_click")
        def on_click_use(event):
            if self.clicked_slot and hasattr(self.clicked_slot, 'item'):
                item = self.clicked_slot.item
                if item.type == "Material": return  # Materiais não podem ser equipados
                if equip_or_unequip == "equip":
                    self.equip_item(item)
                elif equip_or_unequip == "unequip":
                    self.unequip_item()
                self.close_item_desc()
                self.clicked_slot = None
        
    def close_item_desc(self):
        """Fecha a descrição do item selecionado."""
        self.organize_button.center_x = self.background_sprite.center_x + 50
        if self.use_button:
            self.ui_manager.remove(self.use_button)
            self.use_button = None
        if self.drop_button:
            self.ui_manager.remove(self.drop_button)
            self.drop_button = None
        if self.item_desc.children:
            self.item_desc.clear()
        if self.clicked_slot:
            self.clicked_slot.texture = self.normal_slot_texture

    def load_item(self, src, func: str):
        
        if self.clicked_slot is not None and self.clicked_slot == src: # Clicou no mesmo slot
            self.close_item_desc()
        elif hasattr(src, 'item') and src.item:
            self.close_item_desc()
            self.load_item_desc(src.item)
            self.load_item_buttons(func)
            self.clicked_slot = src
            self.clicked_slot.texture = self.hovered_slot_texture
        else: # Clicou em um slot vazio?
            self.close_item_desc()
            self.clicked_slot = None
    
    #-------------------------
    # Funções auxiliares
    #-------------------------
    
    def get_empty_slot(self, name):
        """Retorna o primeiro slot vazio do inventário."""
        for slot in self.grid_1.children + self.grid_2.children:
            if len(slot.children) <= 1 or (slot.item.name == name and slot.item.stackable):
                return slot
            elif slot.item is None:
                return slot
        return None

    def create_text_box(self, parent, x, start_y, width, spacing, font_size=12, texts=[]):
        """Cria uma caixa de texto na tela."""
        y = start_y
        for text in texts:
            label = arcade.gui.UILabel(
                text=text,
                x=x, y=y,
                width=width, height=font_size+2,
                font_name="alagard", font_size=font_size, text_color=arcade.color.WHITE,
                multiline=True
            )
            parent.add(label)
            y -= font_size + spacing  # Espaçamento entre as caixas de texto
    
    def update_stats(self):
        player = self.window.game_view.player
        damage = player.attack_damage
        speed = player.speed
        # Atualiza a caixa de stats
        for child in self.background_sprite.children:
            if isinstance(child, arcade.gui.UILabel):
                if "Damage:" in child.text:
                    child.text = f"Damage: {damage}"
                elif "Speed:" in child.text:
                    child.text = f"Speed: {speed}"