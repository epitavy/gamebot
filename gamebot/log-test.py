from genetics import BaseGameEvaluator, BaseAlgorithm, Genetic


class DummyEvaluator(BaseGameEvaluator):
    """Dummy class for testing.

    It implements only the core workflow of an evaluator."""

    def __init(self):
        self.reset()

    def reset(self):
        self.score = 0
        self.turn_count = 0
        self.point_count = 0

    @property
    def is_over(self):
        return self.turn_count >= 10

    @property
    def state(self):
        return [self.turn_count]

    def algoPlay(self, move):
        self.play(move)
        self.turn_count += 1

    def play(self, move):
        self.point_count += move

    def scoring(self):
        score = self.point_count // self.turn_count
        return score if score > 0 else 0


class DummyMaximazerAlgo(BaseAlgorithm):
    """Dummy class for testing.

    It has five parameters and returns the sum of the five when run.
    We suppose the parameters all positive bounded to 100
    """

    _evaluator = None

    def __init__(self, params=None):
        self.p = 0
        self._score = 0
        if not params or len(params) != 5:
            raise ValueError("The Maximazer should be initialized with 5 parameters.")
        self._params = list(params)

    def run(self, input_state=None):
        return sum(self._params)  # - 2 * self._params[0]

    def evaluate(self):
        self._score = self.evaluator.evaluate(self)

    @property
    def score(self):
        return self._score

    @property
    def parameters(self):
        return [p / 100 for p in self._params]

    @parameters.setter
    def parameters(self, parameters):
        for i in range(5):
            p = parameters[i] * 100
            if p < 0:
                p = 0
            elif p > 100:
                p = 100
            self._params[i] = p

    @property
    def evaluator(self):
        if self._evaluator is None:
            self._evaluator = DummyEvaluator()

        return self._evaluator

    @classmethod
    def parameter_count(cls):
        return 5


class DummyAlgo(BaseAlgorithm):
    """Dummy class for testing.

    We suppose that the parameter can vary between -10 and 10 and that 8 is the optimal value.
    """

    def __init__(self, params=None):
        self.p = 0
        self._score = 0

    def run(self, input_state=None):
        pass  # It won't work with real class

    def evaluate(self):
        self._score = 20 - abs(-10 - self.p)

    @property
    def score(self):
        return self._score if self._score > 0 else 0

    @property
    def parameters(self):
        return [self.evaluator(self)]

    @parameters.setter
    def parameters(self, parameters):
        self.p = parameters[0] * 20 - 10

    @property
    def evaluator(self):
        return lambda x: (10 + x.p) / 20  # It won't work with real class

    @classmethod
    def parameter_count(cls):
        return 1


data = {"crossover_point": 0.1, "mutation_variance": 0.2, "log": "test_one_param"}

gen = Genetic(DummyAlgo, **data)
gen.populate(200)
gen.train(400)
