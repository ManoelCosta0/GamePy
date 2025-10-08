import arcade

class Entity(arcade.Sprite):
    """
    Classe base para entidades no jogo, como jogadores e inimigos.
    """
    def __init__(self, image_path: str, center_x: float, center_y: float, max_hp: int = 100, scale: float = 2):
        super().__init__(image_path, scale, center_x=center_x, center_y=center_y)
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack_damage = 0
    
    def take_damage(self, damage: int):
        self.current_hp -= damage
    