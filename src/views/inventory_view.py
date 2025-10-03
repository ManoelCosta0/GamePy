import arcade
from src.views.view import View
from src.game_objects.item import Item
from src.views.item_detail_view import ItemDetailView
from src.ui.slot import Slot

class InventoryView(View):
    """
    Tela de Inventário do Jogo.
    """
    def __init__(self):
        super().__init__()
        
        self.background_sprite = arcade.Sprite("assets/UI/background.png", scale=1.15, center_x=self.window.width / 2, center_y=self.window.height / 2)
        self.general_sprite_list.append(self.background_sprite)
        self.inventory_elements = arcade.SpriteList()
        self.item_sprites = arcade.SpriteList()
        self.equipped_item_sprites = arcade.SpriteList()
        self.item_detail_view = None
        self.setup()

    def setup(self):
        # Instâncias dos sprites do inventário
        x,y = self.window.width / 2, self.window.height / 2
        self.inventory_box = arcade.Sprite("assets/UI/inventory_box.png", center_x=x, center_y=y, scale=0.8)
        self.weapon_slot = Slot("assets/UI/inventory_weapon_slot.png", x - 140, y + 84, 0.4, "weapon", 9)
        self.armor_slot = Slot("assets/UI/inventory_armor_slot.png", x - 140, y - 47, 0.4, "armor", 10)
        self.accessory_slot = Slot("assets/UI/inventory_accessory_slot.png", x - 140, y - 153, 0.25, "accessory", 11)
        self.uslot = arcade.load_texture("assets/UI/inventory_unavailable_slot.png")
        self.normal_slot = arcade.load_texture("assets/UI/inventory_available_slot.png")

        self.create_slots() # Cria os slots do inventário

        # Adiciona os sprites à lista geral
        self.general_sprite_list.append(self.inventory_box)
        self.inventory_elements.append(self.weapon_slot)
        self.inventory_elements.append(self.armor_slot)
        self.inventory_elements.append(self.accessory_slot)

    def on_show_view(self):
        self.background_sprite.center_x, self.background_sprite.center_y = self.window.width / 2, self.window.height / 2

    def on_draw(self):
        """ Desenha todos os elementos da View. """
        self.clear()
        self.general_sprite_list.draw()
        self.inventory_elements.draw()
        self.item_sprites.draw()
        self.equipped_item_sprites.draw()
        if self.item_detail_view:
            self.item_detail_view.on_draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.pause_view)
        elif key == arcade.key.I:
            self.window.show_view(self.window.game_view)
        elif key == arcade.key.TAB:
            self.developer_mode = not self.developer_mode
            print(f"Developer Mode {'ON' if self.developer_mode else 'OFF'}")

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """ Chamado quando o mouse é arrastado. """
        elements_colliding = arcade.get_sprites_at_point((x, y), self.inventory_elements)

        if elements_colliding and self.developer_mode and self.item_detail_view is None:
            self.is_dragging = True
            elements_colliding[0].center_x += dx
            elements_colliding[0].center_y += dy
        elif self.item_detail_view and self.developer_mode:
            self.is_dragging = True
            self.item_detail_view.on_mouse_drag(x, y, dx, dy)
    
    def on_mouse_release(self, x, y, button, modifiers):
        self.is_dragging = False
        elements_colliding = arcade.get_sprites_at_point((x, y), self.inventory_elements)
        if elements_colliding and self.item_detail_view is None and self.developer_mode:
            pos_x = self.window.width / 2 - elements_colliding[0].center_x
            pos_y = self.window.height / 2 - elements_colliding[0].center_y
            print(f"Elemento {elements_colliding[0]} solto na posição ({pos_x}, {pos_y}) relativa ao centro")
        elif self.item_detail_view and self.developer_mode:
            self.item_detail_view.on_mouse_release(x, y)
    
    def unequip_temp_func(self, player):
        self.weapon_slot.remove_item_from_slot()
        self.equipped_item_sprites.pop(0)
        self.window.game_view.unequip_item_on_game(self.item_detail_view.item)
        self.window.log_box.add_message(f"Você desequipou {self.item_detail_view.item.name}.")
        self.add_item_on_display(self.item_detail_view.item)
    
    def on_mouse_press(self, x, y, button, modifiers):
        """ Chamado quando o botão do mouse é pressionado. """
        if button == arcade.MOUSE_BUTTON_LEFT:
            elements_colliding = arcade.get_sprites_at_point((x, y), self.inventory_elements)

            if elements_colliding and elements_colliding[0].item: 
                # Se clicar no slot com item
                self.item_detail_view = ItemDetailView(
                    elements_colliding[0].item, 
                    self.inventory_box.center_x, 
                    self.inventory_box.center_y,
                    self.inventory_elements.index(elements_colliding[0]))
            elif self.item_detail_view:
                # Se clicar em algo dentro da tela de detalhes
                action = self.item_detail_view.on_mouse_press(x, y)
                player = self.window.game_view.player

                if action == "equip":
                    player.equip_weapon(self.item_detail_view.item, self.item_detail_view.index)
                    if self.weapon_slot.item:
                        self.unequip_temp_func(player)
                    self.equip_item_on_display(player.equipped_weapon)
                    self.window.game_view.equip_item_on_game(player.equipped_weapon)
                    self.window.log_box.add_message(f"Você equipou {self.item_detail_view.item.name}.")
                elif action == "discard":
                    player.inventory.remove_item(self.item_detail_view.index)
                    self.restructure_slots()
                    self.window.log_box.add_message(f"Você descartou {self.item_detail_view.item.name}.")
                elif action == "unequip":
                    player.unequip_weapon()
                    self.unequip_temp_func(player)

                self.item_detail_view = None
            elif self.item_detail_view and not self.item_detail_view.background_sprite.collides_with_point((x, y)):
                # Se clicar fora da tela de detalhes
                self.item_detail_view = None

    def create_slots(self):
        """Cria os slots do inventário."""
        count = 0
        for j in range(4):
            for i in range(3):
                slot = Slot("assets/UI/inventory_available_slot.png", 
                            self.inventory_box.center_x - 20 + i * 95, 
                            self.inventory_box.center_y + 80 - j * 90, 
                            0.12, "normal", count)
                self.inventory_elements.append(slot)
                count += 1

    def get_free_slot_index(self) -> int:
        """ Retorna o índice do primeiro slot livre. """
        for index, slot in enumerate(self.inventory_elements):
            if slot.slot_type == "normal" and slot.item is None:
                return index
        raise Exception("Nenhum slot livre disponível!")

    def restructure_slots(self):
        """ Reestrutura os slots do inventário após a remoção de um item. """
        self.item_sprites.clear()
        for slot in self.inventory_elements:
            if slot.slot_type == "normal":
                slot.remove_item_from_slot()
                

        remaining_items = self.window.game_view.player.get_items()
        for item in remaining_items:
            self.add_item_on_display(item)

    def add_item_on_display(self, item: Item):
        """Adiciona um item à tela do inventário."""
        free_slot_index = self.window.inventory_view.get_free_slot_index()
        item_sprite = self.inventory_elements[free_slot_index].add_item_on_slot(item)
        self.item_sprites.append(item_sprite)

    def equip_item_on_display(self, item: Item):
        """Equipa um item na tela do inventário."""
        self.restructure_slots()
        item_sprite = self.weapon_slot.add_item_on_slot(item)
        self.equipped_item_sprites.append(item_sprite)