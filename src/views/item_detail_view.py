import arcade
from src.game_objects.item import Item
from src.ui.slot import Slot

class ItemDetailView():
    """
    Tela de Detalhes do Item.
    """
    def __init__(self, item: Item, center_x: float, center_y: float, index: int):
        super().__init__()
        self.background_sprite = arcade.Sprite("assets/UI/item_box.png", center_x=center_x + 400, center_y=center_y-20, scale=0.4)
        self.item = item
        self.index = index
        self.general_sprite_list = arcade.SpriteList()
        self.general_sprite_list.append(self.background_sprite)
        self.detail_elements = arcade.SpriteList()
        self.setup()

    def setup(self):
        # Configura os elementos da tela de detalhes do item
        self.slot = Slot("assets/UI/inventory_unavailable_slot.png", self.background_sprite.center_x, self.background_sprite.center_y+90, 0.12, "normal")
        self.item_sprite = arcade.Sprite(self.item.image_file, center_x=self.slot.center_x, center_y=self.slot.center_y, scale=self.item.scale)
        self.detail_elements.append(self.slot)
        self.detail_elements.append(self.item_sprite)

        # Texto do nome do item
        self.item_name_text = arcade.Text(
            text=self.item.name,
            x=self.background_sprite.center_x,
            y=self.background_sprite.center_y + 25,
            color=arcade.color.WHITE,
            font_size=16,
            anchor_x="center"
        )

        # Texto da descrição do item
        self.item_description_text = arcade.Text(
            text=self.item.description,
            x=self.background_sprite.center_x + 15,
            y=self.background_sprite.center_y - 10,
            color=arcade.color.LIGHT_GRAY,
            font_size=11,
            anchor_x="center",
            width=250,
            align="left",
            multiline=True
        )

        self.button = "equip" if self.index < 12 else "unequip"
        self.equip_button = arcade.Sprite(f"assets/UI/{self.button}_button.png", center_x=self.background_sprite.center_x - 56, center_y=self.background_sprite.center_y - 137, scale=0.14)
        self.discard_button = arcade.Sprite("assets/UI/discard_button.png", center_x=self.background_sprite.center_x + 62, center_y=self.background_sprite.center_y - 137, scale=0.14)

        self.detail_elements.append(self.equip_button)
        self.detail_elements.append(self.discard_button)

    def on_draw(self):
        """ Desenha todos os elementos da View. """
        self.general_sprite_list.draw()
        self.item_name_text.draw()
        self.item_description_text.draw()
        self.detail_elements.draw()

    def on_mouse_drag(self, x, y, dx, dy):
        """ Chamado quando o mouse é arrastado e a tela de detalhes está aberta"""
        elements_colliding = arcade.get_sprites_at_point((x, y), self.detail_elements)
        if elements_colliding:
            elements_colliding[0].center_x += dx
            elements_colliding[0].center_y += dy
        
    def on_mouse_release(self, x, y):
        """ Chamado quando o mouse é solto e a tela de detalhes está aberta"""
        elements_colliding = arcade.get_sprites_at_point((x, y), self.detail_elements)
        if elements_colliding:
            pos_x = self.background_sprite.center_x - elements_colliding[0].center_x
            pos_y = self.background_sprite.center_y - elements_colliding[0].center_y
            print(f"Elemento {elements_colliding[0]} solto na posição ({pos_x}, {pos_y}) relativa ao centro da tela de detalhes")

    def on_mouse_press(self, x, y) -> str:
        elements_colliding = arcade.get_sprites_at_point((x, y), self.detail_elements)
        if elements_colliding:
            if elements_colliding[0] == self.equip_button:
                return self.button
            elif elements_colliding[0] == self.discard_button:
                return "discard"