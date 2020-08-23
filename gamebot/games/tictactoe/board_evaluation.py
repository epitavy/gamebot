"""
    This file is here for testing purpose. It allows to test minimax and the tictactoe code
    without any genetics involved.
    The purpose of the board evaluation is NOT to be accurate or interesting. It should just
    give very basic hints to make the AI win a game against a beginner player.
"""

from gamebot.ai import BaseMinimax


class TictactoeMinimax(BaseMinimax):
    """This class is meant to be pluged directly in the Tictactoe game as a player since
    it inherits from BaseAlgorithm.
    """

    @staticmethod
    def two_pieces_patterns():
        """Return a generator on all the 2-pieces possible patterns."""

        for i in range(9):
            for j in range(i + 1, 9):
                if i // 3 == j // 3 or i % 3 == j % 3:
                    yield (i, j)

        # yield diagonals
        yield from [(0, 4), (0, 8), (4, 8), (2, 4), (2, 6), (4, 6)]

    def state_score(self, state):
        """This function uses a TictactoeState object as state."""
        score = 0
        board = list(state)[1:]

        for i, j in self.two_pieces_patterns():
            if state.player == board[i] and board[i] == board[j]:
                score += 1
            elif state.next_player == board[i] and board[i] == board[j]:
                score -= 1

        return score

    @property
    def evaluator(self):
        pass
