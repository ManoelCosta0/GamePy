import arcade

class Slot(arcade.Sprite):
    def __init__(self, image_file: str, position_x: float, position_y: float, scale: float, slot_type: str):
        super().__init__(image_file, scale=scale)
        self.center_x = position_x
        self.center_y = position_y
        self.slot_type = slot_type
        self.item = None 
        self.normal_slot = arcade.load_texture(image_file)
        if slot_type == "normal":
            self.uslot = arcade.load_texture("assets/UI/inventory_unavailable_slot.png")
        elif slot_type == "weapon":
            self.uslot = arcade.load_texture("assets/UI/inventory_weapon_slot.png")

    def add_item_on_slot(self, item) -> arcade.Sprite:
        """Adiciona um item ao slot."""
        item_sprite = arcade.Sprite(
            item.image_file, 
            scale=item.scale,
            center_x=self.center_x, 
            center_y=self.center_y)
        self.texture = self.uslot
        self.item = item
        return item_sprite

    def remove_item_from_slot(self):
        """Remove o item do slot."""
        self.item = None
        self.texture = self.normal_slot