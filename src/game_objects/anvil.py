import arcade

anvil_dir = "assets/sprites/details/bigorna.png"

class Anvil(arcade.Sprite):
    def __init__(self, position, player, scene):
        self.anvil = arcade.load_texture(anvil_dir)
        super().__init__(self.anvil, center_x=position[0], center_y=position[1], scale=3.0)
        
        self.player = player
        
        self.game_view = arcade.get_window().game_view
        
        self.hitbox = None
        scene.add_sprite("interactive_obj", self)
        self.set_interaction_area(position, scene)
        
        self.activated = False
        
        self.interaction_key = arcade.Sprite("assets/ui/util/interaction_key_E.png", center_x=position[0] + 40, center_y=position[1]-30, scale=0.4)
        scene.add_sprite("details", self.interaction_key)
        self.interaction_key.visible = False

    def set_interaction_area(self, position, scene):
        self.hitbox = arcade.SpriteSolidColor(140, 140, color=(255, 0, 0, 0))
        self.hitbox.center_x, self.hitbox.center_y = position[0], position[1] - 25
        scene.add_sprite("interactive_area", self.hitbox)

    def update(self, delta_time: float = 1/60):
        """ Atualiza a lógica da bigorna. """
        if self.player.collides_with_sprite(self.hitbox):
            self.interaction_key.visible = True
        elif self.interaction_key.visible:
            self.interaction_key.visible = False
    
    def on_interact(self, view, obj):
        view.window.log_box.add_message("Você interagiu com a bigorna!")
        
        