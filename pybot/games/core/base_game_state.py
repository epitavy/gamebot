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
    def is_tie(self):
        """Retutn True is the state is a tie state."""
        pass

    @abstractmethod
    def has_won(self, player):
        """Return True is the given player has won the game on the current state."""
        pass

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

    @property
    @abstractmethod
    def next_player(self):
        """Return the next player, i.e. the one that plays after `player`."""
        pass

    @abstractmethod
    def __iter__(self):
        """Return an iterator over the state.

        We should be able to retrieve the full state from this iterator.
        """
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass
