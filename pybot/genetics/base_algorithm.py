from abc import ABC, abstractmethod


class BaseAlgorithm(ABC):
    """Base class that every algorithm class should inherit from.

    It defines the API needed by the Genetic class to work correctly
    """

    @abstractmethod
    def run(self, input_state):
        """Run the algorithm with the given input_state."""
        pass

    @abstractmethod
    def evaluate(self):
        """Evaluate the algorithm. It should set the just calculated score."""
        pass

    @property
    @abstractmethod
    def score(self):
        """Return the score of the algorithm. It is positive"""
        pass

    @property
    @abstractmethod
    def parameters(self):
        """Return the algorithm parameters in an array-like form.

        The value of the parameters should be normalized to lie between 0 and 1.
        """
        pass

    @parameters.setter
    @abstractmethod
    def parameters(self, parameters):
        """Set the algorithm parameter.

        The data should be transformed to fit the internal algorithm representation.
        The parameters value has the same form that the one returned by the parameter getter.
        """
        pass

    @property
    @abstractmethod
    def evaluator(self):
        """Return an instance specific evaluator."""
        pass

    @classmethod
    @abstractmethod
    def parameter_count(cls):
        """Return the total count of free parameters."""
        pass
