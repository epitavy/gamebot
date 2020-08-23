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

    def next_turn(self):
        if self.current_player == 0:
            self.current_player = 1
        else:
            self.current_player = 0

    """BaseGameEvaluator API"""

    def reset(self):
        self.board = [[-1 for _ in range(3)] for _ in range(3)]

    def is_over(self):
        winner = self.get_winner()
        return winner is not None

    def get_winner(self):
        if self._state.has_won(0):
            return 0
        if self._state.has_won(1):
            return 1
        if self._state.is_tie():
            return -1
        return None

    def algoPlay(self, move):
        return self.play((move // 3, move % 3))

    def play(self, move):
        """Return True is the move has been played.

        Move is the move id."""

        x, y = move
        if not self.is_valid_move(x, y):
            return False

        self.board[x][y] = self.current_player
        self.next_turn()
        self._state = TictactoeState(3 * x + y, self.current_player, self.board)

        return True

    def scoring(self):
        return 0

    @property
    def state(self):
        return self._state


class TictactoeState(BaseGameState):
    """A move in tictactoe is represented with the number of the cell and the player in a tuple."

    The player is either 0 or 1. An empty cell is represented by -1.
    """

    def __init__(self, cell_played, player, board):
        self._board = copy.deepcopy(board)
        self._origin_move = cell_played
        self._player = player  # Used in the `player` property of the base class
        self._origin_player = self.next_player

    def possible_next_states(self):
        for i in range(3):
            for j in range(3):
                if self._board[i][j] == -1:
                    self._board[i][j] = self.player
                    cell = 3 * i + j

                    try:
                        yield TictactoeState(cell, self.next_player, self._board)
                    finally:
                        self._board[i][j] = -1  # Back to original state

    def is_tie(self):
        for i in range(3):
            for j in range(3):
                if self._board[i][j] == -1:
                    return False
        return True

    def has_won(self, player):
        for i in range(3):
            if (
                self._board[i][0] == self._board[i][1]
                and self._board[i][1] == self._board[i][2]
                and self._board[i][2] == player
            ):
                return True
            if (
                self._board[0][i] == self._board[1][i]
                and self._board[1][i] == self._board[2][i]
                and self._board[2][i] == player
            ):
                return True

        if (
            self._board[0][0] == self._board[1][1]
            and self._board[1][1] == self._board[2][2]
            and self._board[2][2] == player
        ):
            return True

        if (
            self._board[0][2] == self._board[1][1]
            and self._board[1][1] == self._board[2][0]
            and self._board[2][0] == player
        ):
            return True

        return False

    @property
    def next_player(self):
        if self.player == 0:
            return 1
        return 0

    def __iter__(self):
        yield self.player
        yield from (self._board[i][j] for i in range(3) for j in range(3))

    def __eq__(self, other):
        return self._board == other._board and self.player == other.player

    def __hash__(self):
        return hash(tuple(self))
