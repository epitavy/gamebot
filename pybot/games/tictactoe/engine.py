import copy

from pybot.genetics import BaseGameEvaluator
from ..core import BaseGameState


class TictactoeEngine(BaseGameEvaluator):
    """Tictactoe game logic is fully encapsulated in this class."""

    def __init__(self, player):
        self.board = [[-1 for _ in range(3)] for _ in range(3)]
        self.current_player = player
        self._state = TictactoeState(None, player, self.board)

    def is_valid_move(self, x, y):
        if x < 0 or x >= 3 or y < 0 or y >= 3:
            return False

        return self.board[x][y] == -1  # Empty cell

    def has_win(self, player):
        for i in range(3):
            if (
                self.board[i][0] == self.board[i][1]
                and self.board[i][1] == self.board[i][2]
                and self.board[i][2] == player
            ):
                return True
            if (
                self.board[0][i] == self.board[1][i]
                and self.board[1][i] == self.board[2][i]
                and self.board[2][i] == player
            ):
                return True

        if (
            self.board[0][0] == self.board[1][1]
            and self.board[1][1] == self.board[2][2]
            and self.board[2][2] == player
        ):
            return True

        if (
            self.board[0][2] == self.board[1][1]
            and self.board[1][1] == self.board[2][0]
            and self.board[2][0] == player
        ):
            return True

        return False

    def next_turn(self):
        if self.current_player == 0:
            self.current_player = 1
        else:
            self.current_player = 0

    """BaseGameEvaluator API"""

    def reset(self):
        self.board = [[-1 for _ in range(3)] for _ in range(3)]

    @property
    def is_over(self):
        return self.has_win(0) or self.has_win(1)

    @property
    def state(self):
        return self._state

    def algoPlay(self, move):
        return self.play((move // 3, move % 3))

    def play(self, move):
        """Return True is the move has been played.

        Move is the move id.."""

        x, y = move
        if not self.is_valid_move(x, y):
            return False

        self.board[x][y] = self.current_player
        self.next_turn()
        self._state = TictactoeState(3 * x + y, self.current_player, self.board)

        return True

    def scoring(self):
        return 0


class TictactoeState(BaseGameState):
    """A move in tictactoe is represented with the number of the cell and the player in a tuple."

    The player is either 0 or 1. An empty cell is represented by -1.
    """

    def __init__(self, cell_played, player, board):
        self._board = copy.deepcopy(board)
        self._origin_move = cell_played
        self._origin_player = player
        self._player = (
            self.next_player
        )  # Used in the `player` property of the base class

    def possible_next_states(self):
        for i in range(3):
            for j in range(3):
                if self._board[i][j] == -1:
                    self._board[i][j] = self.player
                    cell = 3 * i + j
                    try:
                        yield TictactoeState(cell, self.player, self._board)
                    finally:
                        self._board[i][j] == -1  # Back to original state

    def is_final(self):
        for i in range(3):
            for j in range(3):
                if self._board[i][j] == -1:
                    return False
        return True

    @property
    def next_player(self):
        if self._origin_player == 0:
            return 1
        return 0

    def __iter__(self):
        yield self._origin_player
        yield from (self._board[i][j] for i in range(3) for j in range(3))

    def __eq__(self, other):
        return self._board == other._board and self._player == other._player

    def __hash__(self):
        return hash(tuple(self))
