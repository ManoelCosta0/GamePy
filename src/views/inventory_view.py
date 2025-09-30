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
        self.item_detail_view = None
        self.setup()

    def setup(self):
        # Instâncias dos sprites do inventário
        self.inventory_box = arcade.Sprite("assets/UI/inventory_box.png", center_x=800, center_y=400, scale=0.8)
        self.weapon_slot = Slot("assets/UI/inventory_weapon_slot.png", 800 - 140, 400 + 84, 0.4, "weapon")
        self.armor_slot = Slot("assets/UI/inventory_armor_slot.png", 800 - 140, 400 - 47, 0.4, "armor")
        self.accessory_slot = Slot("assets/UI/inventory_accessory_slot.png", 800 - 140, 400 - 153, 0.25, "accessory")
        self.uslot = arcade.load_texture("assets/UI/inventory_unavailable_slot.png")
        self.normal_slot = arcade.load_texture("assets/UI/inventory_available_slot.png")

        self.create_slots() # Cria os slots do inventário

        # Adiciona os sprites à lista geral
        self.general_sprite_list.append(self.inventory_box)
        self.inventory_elements.append(self.weapon_slot)
        self.inventory_elements.append(self.armor_slot)
        self.inventory_elements.append(self.accessory_slot)

    def on_show_view(self):
        self.background_sprite.center_x = self.window.width / 2
        self.background_sprite.center_y = self.window.height / 2

    def on_draw(self):
        """ Desenha todos os elementos da View. """
        self.clear()
        self.general_sprite_list.draw()
        self.inventory_elements.draw()
        self.item_sprites.draw()
        if self.item_detail_view:
            self.item_detail_view.on_draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.pause_view)
        elif key == arcade.key.I:
            self.window.show_view(self.game_view)
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
            pos_x = 800 - elements_colliding[0].center_x
            pos_y = 400 - elements_colliding[0].center_y
            print(f"Elemento {elements_colliding[0]} solto na posição ({pos_x}, {pos_y}) relativa ao centro")
        elif self.item_detail_view and self.developer_mode:
            self.item_detail_view.on_mouse_release(x, y)
    
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

                if action == "equip":
                    self.game_view.player.equip_weapon(self.item_detail_view.item)
                    self.game_view.player.inventory.equip_item(self, self.item_detail_view.item, self.item_detail_view.index)
                    self.game_view.general_sprite_list.append(self.game_view.player.equipped_weapon)
                    item_sprite = self.weapon_slot.add_item_on_slot(self.item_detail_view.item)
                    self.item_sprites.append(item_sprite)
                    self.item_sprites.swap(len(self.item_sprites) - 1, 0)  # Move o sprite do item equipado para o início da lista
                    self.window.log_box.add_message(f"Você equipou {self.item_detail_view.item.name}.")
                elif action == "discard":
                    self.game_view.player.inventory.remove_item(self, self.item_detail_view.index)
                    self.window.log_box.add_message(f"Você descartou {self.item_detail_view.item.name}.")
                elif action == "unequip":
                    print(f"Desequipando {self.item_detail_view.item.name}")
                    self.game_view.player.equipped_weapon = None
                    self.game_view.player.inventory.unequip_item(self, self.item_detail_view.item)
                    self.weapon_slot.remove_item_from_slot()
                    self.item_sprites.pop(0)

                self.item_detail_view = None
            elif self.item_detail_view and not self.item_detail_view.background_sprite.collides_with_point((x, y)):
                # Se clicar fora da tela de detalhes
                self.item_detail_view = None

    def create_slots(self):
        """Cria os slots do inventário."""
        for j in range(4):
            for i in range(3):
                slot = Slot("assets/UI/inventory_available_slot.png", 
                            self.inventory_box.center_x - 20 + i * 95, 
                            self.inventory_box.center_y + 80 - j * 90, 
                            0.12, "normal")
                self.inventory_elements.append(slot)

    def restructure_slots(self):
        """ Reestrutura os slots do inventário após a remoção de um item. """
        self.item_sprites.clear()
        for slot in self.inventory_elements:
            if slot.slot_type == "normal":
                slot.remove_item_from_slot()

        remaining_items = self.game_view.player.inventory.slot_items
        for index, item in enumerate(remaining_items):
            self.add_item_on_display(item, index)

    def add_item_on_display(self, item: Item, index: int):
        """Adiciona um item à tela do inventário."""
        item_sprite = self.inventory_elements[index].add_item_on_slot(item)
        self.item_sprites.append(item_sprite)