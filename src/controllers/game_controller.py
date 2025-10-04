import arcade
from src.game_objects.player import Player
from src.views.game_view import GameView

class Controller():
    def __init__(self, player: Player, game_view: GameView):
        self.player = player
        self.game_view = game_view
    
        