from colored import fg, attr

from gamebot.ai import BaseMinimaxMLP
from gamebot.games.tictactoe import TictactoeEngine
from .base_game_cli import BaseGameCLI


class TictactoeMinimaxMLP(BaseMinimaxMLP):
    pass


class TictactoeCLI(BaseGameCLI):
    """Implements the TictactoeCLI."""

    def __init__(self):
        self.engine = TictactoeEngine()
        self.bot = TictactoeMinimaxMLP((10, 5, 1), "tictactoeMLP_weights.npy")
        self.bot.max_depth = 2

    @classmethod
    def player_to_sign(cls, cell):
        if cell == -1:
            return " "
        elif cell == 0:
            return fg("blue") + attr("bold") + "x" + attr("reset")
        else:
            return fg("yellow") + attr("bold") + "o" + attr("reset")

    @classmethod
    def print_board(cls, board):
        pts = cls.player_to_sign  # Shortcut

        for line in board:
            print(f"|{pts(line[0])}|{pts(line[1])}|{pts(line[2])}|")
            print("-------")

    @classmethod
    def parse_input(cls, player_input):
        try:
            row, col = map(int, player_input.split())
        except Exception:
            print("You should use only numbers and the following format: 'row col'")
            raise

        return 3 * row + col
