import arcade
import collections

class LogBox:
    """
    Uma caixa de Log que exibe mensagens de jogo com um fundo translúcido.
    As mensagens mais recentes aparecem no topo.
    """
    def __init__(self, x: float, y: float, width: int, height: int, max_lines: int = 7):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_lines = max_lines

        self.messages = collections.deque(maxlen=max_lines)

        # Configurações visuais
        self.background_color = (20, 20, 20, 180)  # R, G, B, Alpha (Transparência)
        self.text_color = arcade.color.WHITE
        self.font_size = 14
        self.line_height = self.font_size * 2 # Espaçamento entre linhas

    def add_message(self, text: str):
        """
        Adiciona uma nova mensagem ao topo do log.
        """
        # append adiciona o item no final da lista
        self.messages.append(text)

    def on_draw(self):
        left = self.x
        right = self.x + self.width
        top = self.y + 30
        bottom = self.y - self.height
        
        arcade.draw_lrbt_rectangle_filled(
            left=left,
            right=right,
            top=top,
            bottom=bottom,
            color=self.background_color
        )
        arcade.draw_text(
            "Game Log", 
            x=self.x + 10, 
            y=self.y,
            color=self.text_color,
            font_size= 19,
            font_name="Arial",
            bold=True
        )
        arcade.draw_line(
            self.x + 10, 
            self.y - 10, 
            self.x + self.width - 10, 
            self.y - 10, 
            color=self.text_color, 
            line_width=2
        )

        for i, message in enumerate(self.messages):
            x_position = self.x + 15
            y_position = (self.y) - (self.font_size / 2) - (i * self.line_height) - 25

            arcade.draw_text(
                message,
                x=x_position,
                y=y_position,
                color=self.text_color,
                font_size=self.font_size,
                font_name="calibri",
                anchor_y="center"
            )