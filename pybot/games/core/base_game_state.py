from abc import ABC, abstractmethod


class BaseGameState(ABC):
    """Base class for game state representation.

    It provides an API to translate the state of a game from its specific representation
    to a more suitable representation for calculation and algorithm.
    """

    @abstractmethod
    def possible_next_states(self):
        """Return a generator of possible states after this current state."""
        pass

    @abstractmethod
    def is_final(self):
        """Return True if it is a final state False otherwise.

        If this state is final possible_next_states must return an empty generator."""

    @property
    def last_move(self):
        """Return the move that leads to this current state.

        The move may be represented by its uid.
        """
        return self._origin_move

    @property
    def player(self):
        """Return the player that should play the next move."""
        return self._player

    @abstractmethod
    def __iter__(self):
        """Return an iterator over the state.

        We shouldd be able to retrieve the full state from this iterator.
        """
        pass

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
