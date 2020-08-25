from gamebot.games.tictactoe import TictactoeEngine, TictactoeMinimax
from .base_game_cli import BaseGameCLI


class TictactoeCLI(BaseGameCLI):
    """Implements the TictactoeCLI.

    This class should not be instancied, you only need to call the `run_cli` method,
    on the class itself.
    """

    engine = TictactoeEngine(0)
    bot = TictactoeMinimax()
    bot.max_depth = 5

    @classmethod
    def player_to_sign(cls, cell):
        if cell == -1:
            return " "
        elif cell == 0:
            return "x"
        else:
            return "o"

    @classmethod
    def print_board(cls, board):
        pts = cls.player_to_sign  # Shortcut

        for line in board:
            print(f"|{pts(line[0])}|{pts(line[1])}|{pts(line[2])}|")
            print("-------")
