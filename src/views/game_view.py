# src/views/game_view.py
import arcade
from src import constants as const
from src.game_objects.player import Player
from src.game_objects.entity import Entity
from src.ui.buttons import SpriteButton

class GameView(arcade.View):
    """
    View principal do jogo, onde toda a lógica de gameplay acontece.
    """
    def __init__(self):
        # Chama o construtor da classe pai (arcade.View)
        super().__init__()

        # Define os atributos da View. É importante inicializá-los aqui.
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        self.sprite_list = None
        self.player = None
        self.enemy = None
        self.weapon = None

        # Chama o método setup para configurar a cena
        self.setup()

    def setup(self):
        """ Configura os componentes do jogo para esta View. """
        self.sprite_list = arcade.SpriteList()
        self.player = Player("assets/sprites/player.png", scale=0.5, center_x=400, center_y=450)
        self.enemy = Entity("assets/sprites/bat.png", scale=0.03, center_x=800, center_y=450, max_hp=50)
        
        self.sprite_list.append(self.player)
        self.sprite_list.append(self.enemy)

    def on_show_view(self):
        """ Código a ser executado quando esta view é mostrada. """
        # Isso garante que a cor de fundo seja aplicada sempre que a view for exibida
        arcade.set_background_color(self.background_color)

    def on_draw(self):
        """ Desenha tudo nesta View. """
        self.clear()
        self.sprite_list.draw()

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
            # Lógica para equipar/criar a arma
            if not self.weapon: # Evita criar várias armas
                self.weapon = arcade.Sprite("assets/sprites/sword.png", scale=0.2)
                self.sprite_list.append(self.weapon)
                self.player.weapon = self.weapon

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
        if button == arcade.MOUSE_BUTTON_LEFT and self.player.weapon:
            print("Ataque")
            check = arcade.check_for_collision(self.player.weapon, self.enemy)
            if check:
                print("Acertou")
                self.enemy.current_hp -= 10
                print(f"Vida do inimigo: {self.enemy.current_hp}")

    def on_update(self, delta_time):
        """ Lógica de atualização da View. """
        self.sprite_list.update()
        
        # Atualiza a posição da arma para seguir o jogador
        if self.player.weapon:
            self.player.weapon.center_x = self.player.center_x
            self.player.weapon.center_y = self.player.center_y

class MenuView(arcade.View):
    """
    Tela do Menu Principal.
    """
    def __init__(self):
        super().__init__()
        self.background_sprite = None
        self.menu_sprite_list = arcade.SpriteList()
        self.button_list = arcade.SpriteList()
        self.window = arcade.get_window()
        self.window.maximize()

    def on_show_view(self):
        """ Chamado quando esta View é mostrada. """
        arcade.set_background_color(arcade.color.BLACK) # Um fundo preto para garantir

        self.background_sprite = arcade.Sprite("assets/UI/background.png", scale=1.15)
        new_game_button = SpriteButton(
            normal_texture_path="assets/UI/New_Game_Buttom_normal.png",
            hover_texture_path="assets/UI/New_Game_Buttom_hover.png", scale=0.2)
        new_game_button.center_x = self.window.width - 200
        new_game_button.center_y = self.window.height / 12

        self.menu_sprite_list.append(self.background_sprite)
        self.button_list.append(new_game_button)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        """ Chamado quando o mouse se move - para o efeito de hover. """
        # Verifica com quais botões o mouse está colidindo
        buttons_colliding = arcade.get_sprites_at_point((x, y), self.button_list)

        # Percorre todos os botões para definir seu estado (hover ou normal)
        for button in self.button_list:
            if button in buttons_colliding:
                button.on_hover()
            else:
                button.on_unhover()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """ Chamado quando um botão do mouse é pressionado. """
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Verifica se o clique foi em cima de algum botão
            buttons_colliding = arcade.get_sprites_at_point((x, y), self.button_list)
            
            if buttons_colliding:
                # Como só temos um botão, podemos pegar o primeiro da lista
                # Em um menu com vários botões, você precisaria de uma lógica para
                # identificar qual botão foi clicado.
                print("Botão 'Novo Jogo' clicado!")
                
                # --- AÇÃO DO BOTÃO ---
                # Cria a nova GameView e mostra na tela
                game_view = GameView()
                self.window.show_view(game_view)

    def on_draw(self):
        """ Desenha o menu. """
        self.clear()
        self.menu_sprite_list.draw()
        self.button_list.draw()
    
    def on_resize(self, width, height):
        self.background_sprite.center_x = width / 2
        self.background_sprite.center_y = height / 2
        self.background_sprite.scale = width / const.WINDOW_WIDTH * 1.15