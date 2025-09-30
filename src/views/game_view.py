# src/views/game_view.py
import arcade
from src import constants as const
from src.game_objects.player import Player
from src.game_objects.enemy import Enemy
from src.game_objects.item import Item
from src.views.view import View

class GameView(View):
    """
    View principal do jogo, onde toda a lógica de gameplay acontece.
    """
    def __init__(self):
        super().__init__()

        self.player = None
        self.enemy = None
        self.setup()

    def setup(self):
        """ Configura os componentes do jogo para esta View. """
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        self.player = Player()
        self.enemy = Enemy(name="Bat", x=800, y=450)
        
        self.general_sprite_list.append(self.player)
        self.general_sprite_list.append(self.enemy)

    def on_show_view(self):
        """ Código a ser executado quando esta view é mostrada. """
        # Isso garante que a cor de fundo seja aplicada sempre que a view for exibida
        arcade.set_background_color(self.background_color)

    def on_key_press(self, key, modifiers):
        """ Chamado sempre que uma tecla é pressionada. """
        if key == arcade.key.W:
            self.player.is_moving = True
            self.player.velocity_y = const.MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player.is_moving = True
            self.player.velocity_y = -const.MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player.is_moving = True
            self.player.velocity_x = -const.MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player.is_moving = True
            self.player.velocity_x = const.MOVEMENT_SPEED
        elif key == arcade.key.E:
            item = Item("Espada Velha")
            self.player.inventory.add_item(item)
            self.window.inventory_view.add_item_on_display(item)
            self.window.log_box.add_message("Você pegou uma Espada Velha!")
        elif key == arcade.key.ESCAPE:
            self.window.show_view(self.window.pause_view)
        elif key == arcade.key.I:
            self.window.show_view(self.window.inventory_view)
        elif key == arcade.key.TAB:
            self.developer_mode = not self.developer_mode
            print(f"Developer Mode {'ON' if self.developer_mode else 'OFF'}")

    def on_key_release(self, key, modifiers):
        """ Chamado quando uma tecla é liberada. """
        if key == arcade.key.W or key == arcade.key.S:
            self.player.is_moving = False
            self.player.velocity_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player.is_moving = False
            self.player.velocity_x = 0

    def on_mouse_release(self, x, y, button, modifiers):
        """ Chamado quando o botão do mouse é liberado. """
        if button == arcade.MOUSE_BUTTON_LEFT and self.player.equipped_weapon:
            if self.enemy is None: return
            check = arcade.check_for_collision(self.player.equipped_weapon, self.enemy)
            if check:
                self.player.attack(self.enemy)

    def on_update(self, delta_time):
        """ Lógica de atualização da View. """
        self.general_sprite_list.update()
        
        # Atualiza a posição da arma para seguir o jogador
        if self.player.equipped_weapon:
            self.player.equipped_weapon.center_x = self.player.center_x
            self.player.equipped_weapon.center_y = self.player.center_y
        
        if self.enemy:
            if self.enemy.current_hp <= 0:
                self.window.log_box.add_message(f"Você matou o {self.enemy.name}!")
                drop = self.enemy.on_die()
                if drop:
                    self.player.inventory.add_item(drop)
                    self.window.inventory_view.add_item_on_display(drop)
                    self.window.log_box.add_message(f"{self.enemy.name} dropou {drop.name}!")
                self.enemy = None
    
    def equip_item_on_game(self, item: Item):
        """Equipa um item na tela do jogo."""
        self.window.log_box.add_message(f"Exibindo {item.name}...")
        self.general_sprite_list.append(item)
    
    def unequip_item_on_game(self, item: Item):
        """Remove o item equipado da tela do jogo."""
        if item in self.general_sprite_list:
            self.general_sprite_list.remove(item)
            self.window.log_box.add_message(f"Removendo {item.name}...")