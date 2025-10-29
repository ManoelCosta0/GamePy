import arcade

campfire_dir = "assets/sprites/details/campfire/"

class Campfire(arcade.Sprite):
    def __init__(self, data, player, scene, spawn_point: tuple):
        position = tuple(data["position"])
        self.campfire = arcade.load_texture(campfire_dir + "campfire_idle.png")
        super().__init__(self.campfire, center_x=position[0], center_y=position[1], scale=2.0)

        self.state = "idle"
        self.player = player
        
        self.game_view = arcade.get_window().game_view
        
        self.level_required = data["level_required"]
        
        self.hitbox = None
        scene.add_sprite("interactive_obj", self)
        self.set_interaction_area(position, scene)

        self.animation_state = 0
        self.timers = {"animation": 0.0}
        self.animations = {"starting": [], "burning": []}
        self.anim_cooldowns = {"starting": 0.2, "burning": 0.2}
        self.len_anims = {"starting": 8, "burning": 8}
        self.load_animations()
        self.campfire_activated = False
        
        self.spawn_point = spawn_point
        
        self.interaction_key = arcade.Sprite("assets/ui/util/interaction_key_E.png", center_x=position[0] + 50, center_y=position[1]-50, scale=0.4)
        scene.add_sprite("details", self.interaction_key)
        self.interaction_key.visible = False

    def load_animations(self):
        # Carregar animações
        for state in self.animations.keys():
            frames = []
            for i in range(self.len_anims[state]):
                texture = arcade.load_texture(f"{campfire_dir}{state}/_{i+1}.png")
                frames.append(texture)
            self.animations[state] = frames

    def set_interaction_area(self, position, scene):
        self.hitbox = arcade.SpriteSolidColor(140, 140, color=(255, 0, 0, 0))
        self.hitbox.center_x, self.hitbox.center_y = position[0], position[1] - 16
        scene.add_sprite("interactive_area", self.hitbox)

    def update(self, delta_time: float = 1/60):
        """ Atualiza a lógica do campfire. """
        if self.state == "starting":
            self.update_anim(delta_time)
            if self.animation_state >= self.len_anims["starting"]:
                self.state = "burning"
                self.animation_state = 0
        elif self.state == "burning":
            self.update_anim(delta_time)
        if self.player.collides_with_sprite(self.hitbox):
            self.interaction_key.visible = True
        elif self.interaction_key.visible:
            self.interaction_key.visible = False
            
    def update_anim(self, delta_time: float = 1/60):
        self.timers["animation"] += delta_time
        if self.timers["animation"] >= self.anim_cooldowns[self.state]:
            self.timers["animation"] = 0.0
            x = self.animation_state % self.len_anims[self.state]
            self.texture = self.animations[self.state][x]
            self.animation_state += 1
    
    def activate_campfire(self)-> bool:
        """ Ativa o campfire como ponto de spawn.\n 
        Retorna "True" se ativado com sucesso e "False" caso contrário. """
        if self.player.level >= self.level_required:
            self.state = "starting"
            self.animation_state = 0
            self.player.spawn_point = self.spawn_point
            self.campfire_activated = True
            self.player.maximize_health()
            return True
        else:
            arcade.get_window().log_box.add_message(f"Nível {self.level_required} necessário")
            # Tela de aviso de nível necessário aqui
            return False

    def desactivate_campfire(self):
        self.state = "idle"
        self.texture = self.campfire
        self.animation_state = 0
        self.campfire_activated = False
        
        