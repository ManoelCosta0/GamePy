import arcade
from src.views.game_view import GameView

def main():
    window = GameView()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()