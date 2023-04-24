from colored import fg, attr

from gamebot.ai import BaseMinimaxMLP
from gamebot.games.connect4 import Connect4Engine
from .base_game_cli import BaseGameCLI


class Connect4MinimaxMLP(BaseMinimaxMLP):
    pass


class Connect4CLI(BaseGameCLI):
    """Implements the Connect4CLI."""

    def __init__(self):
        self.engine = Connect4Engine()
        input_size = len(self.engine.board) * len(self.engine.board[0]) + 1
        self.bot = Connect4MinimaxMLP((input_size, 5, 1), "connect4MLP_last_weights.npy")
        self.bot.max_depth = 6

    @classmethod
    def player_to_sign(cls, cell):
        if cell == -1:
            return " "
        elif cell == 0:
            return fg("red") + attr("bold") + "o" + attr("reset")
        else:
            return fg("yellow") + attr("bold") + "o" + attr("reset")

    @classmethod
    def print_board(cls, board):
        pts = cls.player_to_sign  # Shortcut

        for i in range(board.shape[1]):
            print(f"-{i}", end="")
        print("-")

        for line in board:
            for cell in line:
                print("|" + pts(cell), end="")
            print("|")

        for i in range(board.shape[1]):
            print(f"-{i}", end="")
        print("-")

    @classmethod
    def parse_input(cls, player_input):
        try:
            col = int(player_input.strip())
        except Exception:
            print("You should use only a number and the following format: 'col'")

        return col

