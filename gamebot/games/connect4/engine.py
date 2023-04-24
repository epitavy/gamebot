import copy

import numpy as np
from scipy.signal import convolve2d

from gamebot.games import BaseGameState

class Connect4Engine:
    """The game engine for connect4."""
    def __init__(self):
        self.dimX = 6
        self.dimY = 7

        self.reset()
        self.current_player = 0
        self._state = Connect4State(None, self.current_player, self.board)

    def reset(self):
        self.board = np.full((self.dimX, self.dimY), -1, dtype=int)

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

    def next_turn(self):
        if self.current_player == 0:
            self.current_player = 1
        else:
            self.current_player = 0

    def is_valid_move(self, col):
        if col < 0 or col >= self.dimY:
            return False

        return self.board[0][col] == -1

    def play(self, move):
        """Return True if the move has been played."""
        if not self.is_valid_move(move):
            return False

        for x in range(self.dimX - 1, -1, -1):
            if self.board[x][move] == -1:
                self.board[x][move] = self.current_player
                break

        self.next_turn()
        self._state = Connect4State(move, self.current_player, self.board)

        return True

    @property
    def state(self):
        return self._state


class Connect4State(BaseGameState):
    """Connect4 game logic is fully encapsulated in this class.

    A move in the board is represented by the column number and the player in a tuple.

    The player is either 0 or 1. An empty cell is represented by -1.
    """

    def __init__(self, col_played, player, board):
        self._board = copy.deepcopy(board)
        self._origin_move = col_played
        self._player = player  # Used in the `player` property of the base class
        self._origin_player = self.next_player

    def possible_next_states(self):
        for col in range(self._board.shape[1]):
            for row in range(self._board.shape[0] - 1, -1, -1):
                if self._board[row][col] == -1:
                    self._board[row][col] = self.player

                    try:
                        yield Connect4State(col, self.next_player, self._board)
                    finally:
                        self._board[row][col] = -1  # Back to original state
                    break

    def is_tie(self):
        for col in range(self._board.shape[1]):
            if self._board[0][col] == -1:
                    return False
        return not (self.has_won(0) or self.has_won(1))

    def has_won(self, player):
        horizontal_kernel = np.array([[ 1, 1, 1, 1]])
        vertical_kernel = np.transpose(horizontal_kernel)
        diag1_kernel = np.eye(4, dtype=np.uint8)
        diag2_kernel = np.fliplr(diag1_kernel)
        detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]

        for kernel in detection_kernels:
            if (convolve2d(self._board == player, kernel, mode="valid") == 4).any():
                return True

        return False

    @property
    def next_player(self):
        if self.player == 0:
            return 1
        return 0

    def __iter__(self):
        yield self.player
        yield from np.nditer(self._board)

    def __eq__(self, other):
        return np.all(self._board == other._board) and self.player == other.player

    def __hash__(self):
        return hash(tuple(self))
