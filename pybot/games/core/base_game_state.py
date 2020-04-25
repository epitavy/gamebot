from abc import ABC, abstractmethod


class BaseGameState(ABC):
    """Base class for game stae representation.

    It provides an API to translate the state of a game from its specific representation
    to a more suitable representation for calculation and algorithm.
    """

    @abstractmethod
    def possible_next_states(self):
        """Return possible states at a distance of one move from this current sate."""
        pass

    @abstractmethod
    def to_list(self):
        """Return the state in the form of a list of numbers."""
        pass

    @property
    def last_move(self):
        """Return the move that lead to this current state.

        The move may be represented by its uid.
        """
        return self._origin_move

    @property
    def player(self):
        """Return the player that should play the next move."""
        return self._player

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass


def mat_to_tuple(mat):
    return tuple(tuple(line) for line in mat)


def mat_to_list(mat):
    return list(list(line) for line in mat)
