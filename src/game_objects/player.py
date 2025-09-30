from src.game_objects.entity import Entity
from src.game_objects.inventory import Inventory
from src import constants as const

class Player(Entity):
    def __init__(self):
        super().__init__(const.PLAYER_IMAGE, const.PLAYER_SCALE, const.PLAYER_INITIAL_X, const.PLAYER_INITIAL_Y, max_hp=100)
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_moving = False
        self.equipped_weapon = None  # Arma equipada
        self.inventory = Inventory()

    def update(self, *args, **kwargs):
        # Lógica de atualização do jogador
        if self.is_moving:
            self.center_x += self.velocity_x
            if self.equipped_weapon:
                self.equipped_weapon.center_x += self.velocity_x
                self.equipped_weapon.center_y += self.velocity_y
            self.center_y += self.velocity_y
    
    def equip_weapon(self, weapon, index: int):
        self.equipped_weapon = weapon
        self.inventory.equip_item(weapon, index)
        weapon.center_x = self.center_x
        weapon.center_y = self.center_y
        print(f"Dano da arma: {weapon.get_damage()}")
        self.attack_damage = weapon.get_damage()
    
    def unequip_weapon(self):
        if self.equipped_weapon:
            self.inventory.unequip_item(self.equipped_weapon)
            self.equipped_weapon = None
            self.attack_damage = 0
        else:
            print("Nenhuma arma equipada para desequipar.")
    
    def attack(self, target):
        if self.equipped_weapon:
            print(f"Atacando {target.name} causando {self.attack_damage} de dano.")
            target.take_damage(self.attack_damage)
    
    def get_items(self):
        return self.inventory.slot_items