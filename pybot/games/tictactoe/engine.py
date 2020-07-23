from ..core import BaseGameState, mat_to_tuple, mat_to_list


class TictactoeEngine:
    """Tictactoe game logic is fully encapsulated in this class."""

    def __init__(self, player):
        self.board = [[-1 for _ in range(3)] for _ in range(3)]
        self.current_player = player

    def is_valid_move(self, move):
        i, j = move
        if i < 0 or i >= 3 or j < 0 or j >= 3:
            return False

        return self.board[i][j] == -1 # Empty cell

    def play(self, move):
        """Return True is the move has been played.

        Move is a tuple of the following form: (coordX, coordY)."""

        if not self.is_valid_move(move):
            return False

        i, j = move

        self.board[i][j] = self.current_player
        self.next_turn()

        return True

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


class TictactoeState(BaseGameState):
    """A move in tictactoe is represented with the number of the cell and the player in a tuple."

    The player is either 0 or 1. An empty cell is represented by -1.
    """

    def __init__(self, move, player, board_list=None, board_tuple=None):
        if board_tuple is None:
            if board_list is None:
                raise ValueError("Either bord_list or board_tuple should be provided")
            self._board = mat_to_tuple(board_list)

        else:
            self._board = board_tuple

        self._origin_move = move
        self._player = player

    def possible_next_states(self):
        states = []
        n_board = mat_to_list(self._board)

        for i in range(3):
            for j in range(3):
                if self._board[i][j] == -1:
                    n_board[i][j] = self._player
                    move = (3 * i + j, self._player)
                    states.append(
                        TictactoeState(move, self.next_player, board_list=n_board)
                    )
                    n_board[i][j] == -1  # Back to original state
        return states

    @property
    def next_player(self):
        if self._player == 0:
            return 1
        return 0

    def to_list(self):
        state_list = []
        for line in self._board:
            state_list += line
        state_list.append(self._player)
        return state_list

    def __eq__(self, other):
        return self._board == other._board

    def __hash__(self):
        return hash(self.board)
