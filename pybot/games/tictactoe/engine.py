import copy

from ..core import BaseGameState, mat_to_tuple, mat_to_list
from pybot.genetics import BaseGameEvaluator


class TictactoeEngine(BaseGameEvaluator):
    """Tictactoe game logic is fully encapsulated in this class."""

    def __init__(self, player):
        self.board = [[-1 for _ in range(3)] for _ in range(3)]
        self.current_player = player
        self._state = TictactoeState(None, player, mat_to_tuple(self.board))

    def is_valid_move(self, move):
        i, j = move
        if i < 0 or i >= 3 or j < 0 or j >= 3:
            return False

        return self.board[i][j] == -1 # Empty cell


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
        self.play(move)

    def play(self, move):
        """Return True is the move has been played.

        Move is a tuple of the following form: (coordX, coordY)."""

        if not self.is_valid_move(move):
            return False

        i, j = move

        self.board[i][j] = self.current_player
        self.next_turn()
        self._state = TictactoeState(3 * i + j, self.current_player, self.board)

        return True

    def scoring(self):
        return 0


class TictactoeState(BaseGameState):
    """A move in tictactoe is represented with the number of the cell and the player in a tuple."

    The player is either 0 or 1. An empty cell is represented by -1.
    """

    def __init__(self, cell_played, player, board):
        self._board = copy.copy(board)
        self._origin_move = (cell_played, player)

    def possible_next_states(self):
        player = self._origin_move[1]

        for i in range(3):
            for j in range(3):
                if self._board[i][j] == -1:
                    self._board[i][j] = player
                    move = (3 * i + j, player)
                    yield TictactoeState(move, self.next_player, self._board)
                    self._board[i][j] == -1  # Back to original state

    def to_list(self):
        flat_board = [self._board[i][j] for i in range(3) for j in range(3)]
        return flat_board + self._origin_move[1]


    @property
    def next_player(self):
        if self._origin_move[1] == 0:
            return 1
        return 0


    def __eq__(self, other):
        return self._board == other._board

    def __hash__(self):
        return hash(tuple(self.to_list()))
