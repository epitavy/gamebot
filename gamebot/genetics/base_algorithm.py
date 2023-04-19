from abc import ABC, abstractmethod


class BaseAlgorithm(ABC):
    """Base class that every algorithm class should inherit from.

    It defines the API needed by the Genetic class to work correctly
    """

    parameter_count = 0

    @abstractmethod
    def run(self, input_state):
        """Run the algorithm with the given input_state and return a move."""
        pass

    @property
    @abstractmethod
    def score(self):
        """Return the score of the algorithm. It is positive."""
        pass

    @property
    @abstractmethod
    def parameters(self):
        """Return the parameters of the algorithm in an array-like shape.

        The value of the parameters should be normalized to lie between 0 and 1.
        """
        pass

    @parameters.setter
    @abstractmethod
    def parameters(self, parameters):
        """Set the algorithm parameters.

        The data should be unormalized to fit the internal algorithm representation.
        The given parameters are normalized as returned by the getter.
        """
        pass
