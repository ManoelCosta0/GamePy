from src.game_objects.entity import Entity
from src.game_objects.inventory import Inventory
from src import constants as const

class Player(Entity):
    """
    Classe para o jogador no jogo.
    """
    def __init__(self):
        super().__init__("assets/sprites/entities/soldier.png", scale=2, center_x=const.PLAYER_INITIAL_X, center_y=const.PLAYER_INITIAL_Y, max_hp=100)
        self.speed = 5
        self.move_state_x = 0
        self.move_state_y = 0
        self.equipped_weapon = None  # Arma equipada
        self.inventory = Inventory()

    def update(self, delta_time: float = 1/60):
        """ Atualiza a lógica do jogador. """
        self.move_player()
        self.update_weapon_position()
    
    def update_weapon_position(self):
        if self.equipped_weapon:
            self.equipped_weapon.center_x = self.center_x
            self.equipped_weapon.center_y = self.center_y
    
    def move_player(self):
        if self.move_state_x != 0 or self.move_state_y != 0:
            self.center_x += self.move_state_x * self.speed
            self.center_y += self.move_state_y * self.speed

    def equip_weapon(self, weapon, index: int):
        self.equipped_weapon = weapon
        self.inventory.equip_item(weapon, index)
        self.attack_damage = weapon.get_damage()
        weapon.center_x = self.center_x
        weapon.center_y = self.center_y
    
    def unequip_weapon(self):
        if self.equipped_weapon:
            self.inventory.unequip_item(self.equipped_weapon)
            self.equipped_weapon = None
            self.attack_damage = 0
        else:
            print("Nenhuma arma equipada para desequipar.")
    
    def attack(self, target):
        if self.equipped_weapon:
            target.take_damage(self.attack_damage)
    
    def get_items(self):
        return self.inventory.slot_items