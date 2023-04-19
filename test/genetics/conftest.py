import pytest
from gamebot.genetics import BaseAlgorithm

import numpy as np


@pytest.fixture
def algo_one_param():
    return DummyAlgoOneParam


@pytest.fixture
def algo_five_params():
    return DummyMaximizerAlgoFiveParams


@pytest.fixture
def algo_sixhump_camelback():
    return SixHumpCamelBackAlgo


@pytest.fixture
def algo_stepwise():
    return StepwiseAlgo


class AlgoTemplate(BaseAlgorithm):

    parameter_count = 0
    bounds = (0, 1)
    clip_bounds = True

    def __init__(self):
        self._score = 0
        self._parameters = np.random.uniform(*self.bounds, self.parameter_count)

    def run(self, input_state=None):
        pass

    @property
    def parameters(self):
        old_range = self.bounds[1] - self.bounds[0]
        new_range = 2
        params = np.array(self._parameters)
        return (params - self.bounds[0]) * new_range / old_range - 1

    @parameters.setter
    def parameters(self, parameters):
        old_range = 2
        new_range = self.bounds[1] - self.bounds[0]
        params = np.array(parameters)
        params = (params + 1) * new_range / old_range + self.bounds[0]

        if self.clip_bounds:
            params = np.clip(params, *self.bounds)
        self._parameters = list(params)

    @property
    def score(self):
        return self._score


class DummyAlgoOneParam(AlgoTemplate):
    """Dummy class for testing.

    We suppose that the parameter can vary between -10 and 10 and that 8 is the optimal value.
    """

    parameter_count = 1
    bounds = (-10, 10)

    def evaluate(self):
        self._score = 20 - abs(8 - self._parameters[0])

    def run(self, input_state=None):
        return np.sum(self._parameters)

    @property
    def score(self):
        return self._score if self._score > 0 else 0


class DummyMaximizerAlgoFiveParams(AlgoTemplate):
    """Dummy class for testing.

    It has five parameters and returns the sum of the five when run.
    We suppose the parameters all positive bounded to 100
    """

    parameter_count = 5
    bounds = (0, 100)

    def evaluate(self):
        self._score = np.sum(self._parameters)

    def run(self, input_state=None):
        return np.sum(self._parameters)


class SixHumpCamelBackAlgo(AlgoTemplate):
    """Testing minimization of the six-hump camel-back function.

    Parameter x1 is in [-2, 2] and x2 in [-1, 1].
    """

    parameter_count = 2

    @staticmethod
    def _sixhump_camelback(x1, x2):
        return (4 - 2.1 * x1**2 + x1**4 / 3) * x1**2 + x1*x2 + (-4 + 4*x2**2) * x2**2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        x1 = np.random.uniform(-2, 2, 1)[0]
        x2 = np.random.uniform(-1, 1, 1)[0]
        self._parameters = [x1, x2]

    def evaluate(self):
        self._score = 10 - self._sixhump_camelback(*self._parameters) - 1.0316

    @property
    def parameters(self):
        x1 = self._parameters[0] / 2
        x2 = self._parameters[1]

        return np.array([x1, x2])

    @parameters.setter
    def parameters(self, parameters):
        x1, x2 = parameters
        x1 = np.clip(x1 * 2, -2, 2)
        x2 = np.clip(x2, -1, 1)
        self._parameters = [x1, x2]


class StepwiseAlgo(AlgoTemplate):
    """Testing minimization of a stepwise continuous function."""

    parameter_count = 5
    bounds = (-512, 512)

    @staticmethod
    def _stepwise(x):
        return np.sum(np.floor(x))

    def evaluate(self):
        self._score = 512 * 5 - self._stepwise(self._parameters)
