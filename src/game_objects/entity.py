import arcade

class Entity(arcade.Sprite):
    def __init__(self, image_path: str, scale: float, center_x: float, center_y: float, max_hp: int):
        super().__init__(image_path, scale, center_x=center_x, center_y=center_y)
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack_damage = 0 # Valor padrão, será sobrescrito

    def die(self):
        return super().kill()
    
    def take_damage(self, damage: int):
        self.current_hp -= damage
    