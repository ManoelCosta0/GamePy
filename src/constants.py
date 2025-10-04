WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
WINDOW_TITLE = "GAME"

BACKGROUND_IMAGE = "assets/ui/background.jpg"
FONT_PATH = "assets/fonts/alagard.ttf"
UI_PATH = "assets/ui/"

BUTTON_SCALE = 0.5
BUTTONS_TEXTURE = {
    "new_game": UI_PATH + "new_game_button.png",
    "continue": UI_PATH + "continue_button.png",
    "resume": UI_PATH + "pause_screen/resume_button.png",
    "controls": UI_PATH + "pause_screen/controls_button.png",
    "exit": UI_PATH + "pause_screen/exit_button.png",
    "inventory": UI_PATH + "pause_screen/inventory_button.png"
}
BUTTONS_HOVERED_TEXTURE = {
    "new_game": UI_PATH + "new_game_button_hover.png",
    "continue": UI_PATH + "continue_button_hover.png",
    "resume": UI_PATH + "pause_screen/resume_button_hover.png",
    "controls": UI_PATH + "pause_screen/controls_button_hover.png",
    "exit": UI_PATH + "pause_screen/exit_button_hover.png",
    "inventory": UI_PATH + "pause_screen/inventory_button_hover.png"
}

BUTTONS_POSITION_X = {
    "new_game": 395,
    "continue": 395,
    "resume": WINDOW_WIDTH/2,
    "controls": WINDOW_WIDTH/2,
    "exit": WINDOW_WIDTH/2,
    "inventory": WINDOW_WIDTH/2
    }

BUTTONS_POSITION_Y = {
    "new_game": 445,
    "continue": 345,
    "resume": 400,
    "controls": 310,
    "inventory": 220,
    "exit": 130
}

PLAYER_IMAGE = "assets/sprites/player.png"
PLAYER_SCALE = 0.5
PLAYER_INITIAL_X = 400
PLAYER_INITIAL_Y = 1500
MOVEMENT_SPEED = 5