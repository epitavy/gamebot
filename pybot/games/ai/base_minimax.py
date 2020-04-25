from genetics import BaseAlgorithm
from abc import ABC, abstractmethod


class BaseMinimax(BaseAlgorithm, ABC):
    """An implementation of minimax with alpha beta pruning.

    It is designed to run with a BaseGameEvaluator as evaluator.
    The only abstract methods are the state evaluation method and the evaluator property
    that should be implemented for any subclass."""

    def __init__(self):
        self._score = 0
        self._max_depth = (
            3
        )  # A depth of 0 means that no branch of the tree is evaluated

    def run(self, input_state):
        """Take a game state as input and return a move, that maybe the uid of the move."""

        self._player = input_state.player
        # alpha and beta need to be non local to vary trought the recursions
        self._alpha = float("-inf")
        self._beta = float("+inf")
        next_state, score = _alphabeta(input_state, self._max_depth)
        return next_state.last_move

    def _alphabeta(self, state, depth):
        """Minimax with alpha beta pruning. Return the next state with the highest value."""
        if depth == 0:
            return (state, self.state_score(state))

        next_states = state.possible_next_states()

        if state.player == self._player:  # Max node
            state_score = (None, float("-inf"))

            for s in next_states:
                state_score = max(
                    state_score, self._alphabeta(s, depth - 1), key=lambda x: x[1]
                )
                if state_score[1] >= beta:
                    return state_score
                alpha = max(alpha, state_score[1])

        else:  # Min node
            state_score = (None, float("+inf"))

            for s in next_states:
                state_score = min(
                    state_score, self._alphabeta(s, depth - 1), key=lambda x: x[1]
                )
                if alpha >= state_score[1]:
                    return state_score
                beta = min(beta, state_score[1])

        return state_score

    @abstractmethod
    def state_score(self, state):
        """Return the estimated score for the given state.

        The score should be positive if the player (stored in _player)  is likely to win
        and negative if he his likely to loose.
        If the state is a final state (i.e. one of the player won), absolute value of the score
        should be high in comparison to other random states.
        """
        pass

    def evaluate(self):
        self._score = self.evaluator.evaluate(self)

    @property
    def score(self):
        return self._score

    @property
    def parameters(self):
        """Minimax has no free parameters."""
        return []

    @parameters.setter
    def parameter(self, parameters):
        """Minimax has no free parameters."""
        pass

    @property
    def max_depth(self):
        """Return the max depth of the search tree."""
        return self._max_depth

    @max_depth.setter
    def max_depth(self, depth):
        if depth >= 0:
            self._max_depth = depth

    @property
    @abstractmehod
    def evaluator(self):
        """The evaluator type should be a subclass of BaseGameEvaluator."""
        pass

    @classmethod
    def parameter_count(cls):
        """Minimax has no free parameters."""
        return 0
