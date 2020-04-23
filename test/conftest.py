import pytest
from pybot.genetics.BaseAlgorithm import BaseAlgorithm
from pybot.genetics.Genetic import Genetic


class DummyAlgo(BaseAlgorithm):
    """Dummy class for testing.

    We suppose that the parameter can vary between -10 and 10 and that 5 is the optimal value.
    """

    def __init__(self, params=None):
        self.p = 0
        self._score = 0

    def run(self, input_state=None):
        pass

    def evaluate(self):
        self._score = 20 - abs(5 - self.p)
        return self._score

    @property
    def score(self):
        return self._score if self._score > 0 else 0

    @property
    def parameters(self):
        return [(10 + self.p) / 20]

    @parameters.setter
    def parameters(self, parameters):
        self.p = parameters[0] * 20 - 10

    @classmethod
    def parameter_count(cls):
        return 1


@pytest.fixture
def dummy_genetics():
    """Genetic object created and initialized with dummy algo."""
    gen = Genetic(DummyAlgo)
    gen.populate(100)

    return gen
