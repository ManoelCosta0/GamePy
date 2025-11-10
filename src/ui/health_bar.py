import arcade

class HealthBar:
    def __init__(self, owner: arcade.Sprite, sprite_list: arcade.SpriteList, height: int, visible: bool = False):
        self.owner = owner
        self.current_health = self.owner.max_hp
        self.position = (0, 0)
        self.height = height
        self.visible = visible
        self.sprite_list = sprite_list

        self.background_sprite = arcade.Sprite("assets/ui/hud/healthbar_background.png", center_x=0, center_y=0, scale=0.07)
        self.foreground_sprite = arcade.Sprite("assets/ui/hud/healthbar_foreground.png", center_x=0, center_y=0, scale=0.07)

        self.background_sprite.visible = visible
        self.foreground_sprite.visible = visible
        
        sprite_list.append(self.background_sprite)
        sprite_list.append(self.foreground_sprite)

    def update(self):
        if self.owner.current_hp != self.current_health:
            delta_health = self.current_health - self.owner.current_hp
            self.current_health = max(0, min(self.current_health - delta_health, self.owner.max_hp))
            self.foreground_sprite.width = (self.current_health / self.owner.max_hp) * self.background_sprite.width
            if not self.visible:
                self.toggle_visibility()
            
        self.position = (self.owner.center_x, self.owner.center_y + self.height)
        self.background_sprite.position = self.position
        self.foreground_sprite.position = self.position
        self.foreground_sprite.left = self.background_sprite.left + 0.595
    
    def remove_from_sprite_lists(self):
        self.background_sprite.remove_from_sprite_lists()
        self.foreground_sprite.remove_from_sprite_lists()
        
    def add_to_sprite_list(self):
        self.sprite_list.append(self.background_sprite)
        self.sprite_list.append(self.foreground_sprite)

    def toggle_visibility(self):
        self.visible = not self.visible
        self.background_sprite.visible = self.visible
        self.foreground_sprite.visible = self.visible