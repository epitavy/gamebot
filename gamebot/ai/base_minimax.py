from gamebot.genetics import BaseAlgorithm
from abc import ABC, abstractmethod


class BaseMinimax(BaseAlgorithm, ABC):
    """An implementation of minimax with alpha beta pruning.

    It is designed to run with a BaseGameEvaluator as evaluator.
    The only abstract methods are the state evaluation method and the evaluator property
    that should be implemented for any concrete subclass."""

    def __init__(self):
        self._score = 0
        self._max_depth = (
            3  # A depth of 0 means that no branch of the tree is evaluated
        )

    def run(self, input_state):
        """Take a game state as input and return a move uid."""

        self._player = input_state.player
        self._bestmove = None
        self._alphabeta(input_state, self._max_depth, float("-inf"))

        return self._bestmove

    def _alphabeta(self, state, depth, bound):
        """Minimax with alpha beta pruning. Return the score of the most valuable move.

        The move is stored in the instance variable `bestmove`. We used the negamax variant."""

        # Handle final cases
        if state.has_won(state.player):
            return -1e9 - depth  # Even if it is a loose, loose as far as possible
        if state.has_won(state.next_player):
            return 1e9 + depth  # Win as early as possible
        if depth == 0:
            return self.state_score(state)
        if state.is_tie():
            return 0

        next_states = state.possible_next_states()

        score = float("-inf")

        for s in next_states:
            _score = self._alphabeta(s, depth - 1, score)
            if _score > score:
                if depth == self._max_depth:  # Top level node, update best move
                    self._bestmove = s.last_move
                score = _score
            if -score <= bound:
                return -score

        return -score

    @abstractmethod
    def state_score(self, state):
        """Return the estimated score for the given state.

        The score should be positive if the player (from the `player` property)  is likely to win
        and negative if he his likely to loose.
        Final states might be ignored in this evaluation, minimax alogorithm already check that.
        """
        pass

    def evaluate(self):
        self._score = self.evaluator.evaluate(self)

    @property
    def score(self):
        return self._score

    @property
    def parameters(self):
        """Minimax has no free parameter.

        However, any sublass can (and should) forward the parameters used by 'state_score'.
        """
        return []

    @parameters.setter
    def parameter(self, parameters):
        """Minimax has no free parameter.

        However, any sublass can (and should) forward the parameter used by `state_score`.
        """
        pass

    @property
    def max_depth(self):
        """Return the max depth of the search tree."""
        return self._max_depth

    @max_depth.setter
    def max_depth(self, depth):
        if depth > 0:
            self._max_depth = depth
        else:
            raise ValueError("Depth should be strictly positive")

    @property
    @abstractmethod
    def evaluator(self):
        """The evaluator type should be a subclass of BaseGameEvaluator."""
        pass
