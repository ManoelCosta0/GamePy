import arcade

class HealthBar:
    def __init__(self, owner: arcade.Sprite, sprite_list: arcade.SpriteList, max_health: int, height):
        self.owner = owner
        self.max_health = max_health
        self.current_health = max_health
        self.position = (0, 0)
        self.height = height

        self.background_sprite = arcade.Sprite("assets/ui/hud/healthbar_background.png", center_x=0, center_y=0, scale=0.07)
        self.foreground_sprite = arcade.Sprite("assets/ui/hud/healthbar_foreground.png", center_x=0, center_y=0, scale=0.07)

        sprite_list.append(self.background_sprite)
        sprite_list.append(self.foreground_sprite)

    def update(self):
        if self.owner.current_hp != self.current_health and self.owner.current_hp >= 0:
            delta_health = self.current_health - self.owner.current_hp
            self.current_health = max(0, min(self.current_health - delta_health, self.max_health))
            self.foreground_sprite.width = (self.current_health / self.max_health) * self.background_sprite.width
            
        self.position = (self.owner.center_x, self.owner.center_y + self.height)
        self.background_sprite.position = self.position
        self.foreground_sprite.position = self.position
        self.foreground_sprite.left = self.background_sprite.left + 0.595