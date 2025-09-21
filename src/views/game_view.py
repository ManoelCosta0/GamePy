import arcade

from src import constants as const
from src.game_objects.player import Player
from src.game_objects.entity import Entity

class GameView(arcade.Window):

    def __init__(self):

        super().__init__(const.WINDOW_WIDTH, const.WINDOW_HEIGHT, const.WINDOW_TITLE, resizable=True)
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        self.sprite_list = arcade.SpriteList()
        self.player = None

    def setup(self):
        self.player = Player("assets/sprites/player.png", scale=0.5, center_x=400, center_y=450)
        self.enemie = Entity("assets/sprites/bat.png", scale=0.03, center_x=800, center_y=450, max_hp=50)
        self.sprite_list.append(self.player)
        self.sprite_list.append(self.enemie)

    def on_draw(self):
        self.clear()
        self.sprite_list.draw()

    def on_key_press(self, key, modifiers):
        """Chamado sempre que uma tecla é pressionada."""
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
            self.weapon = arcade.Sprite("assets/sprites/sword.png", scale=0.2, center_x=self.player.center_x, center_y=self.player.center_y, angle=45)
            self.sprite_list.append(self.weapon)
            self.player.weapon = self.weapon

    def on_key_release(self, key, modifiers):
        """Chamado quando uma tecla é liberada."""
        if key == arcade.key.W or key == arcade.key.S:
            self.player.is_moving = False
            self.player.velocity_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player.is_moving = False
            self.player.velocity_x = 0
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.player.weapon:
            print("Ataque")
            check = arcade.check_for_collision(self.player.weapon, self.enemie)
            if check:
                print("Acertou")
                self.enemie.current_hp -= 10
                print(f"Vida do inimigo: {self.enemie.current_hp}")

    def on_update(self, delta_time):
        self.sprite_list.update()