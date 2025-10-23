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
        if self.current_hp <= 0:
            self.death_flash()
        else:
            self.hurt_flash()
    
    def hurt_flash(self):
        self.color = (255, 100, 100)  # levemente avermelhado
        self.alpha = 200  # semi-transparente
        arcade.schedule(self.reset_color, 0.15)
    
    def reset_color(self, delta_time):
        self.color = (255, 255, 255)  # volta à cor normal
        self.alpha = 255  # volta à opaco
        arcade.unschedule(self.reset_color)
    
    def death_flash(self):
        """Efeito visual de morte."""
        # Primeiro estágio: fica totalmente vermelho e começa a desaparecer
        self.color = (180, 30, 30)  # tom de vermelho mais escuro
        self.alpha = 255
        arcade.schedule(self._fade_out_death, 0.05)

    def _fade_out_death(self, delta_time):
        """Faz o sprite desaparecer gradualmente após morrer."""
        self.alpha -= 25  # reduz a opacidade em etapas suaves
        if self.alpha <= 0:
            self.alpha = 0
            arcade.unschedule(self._fade_out_death)
            self.on_die()
    
    def is_alive(self):
        return self.current_hp > 0

    