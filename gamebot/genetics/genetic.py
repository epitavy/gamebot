from copy import deepcopy

from .base_algorithm import BaseAlgorithm
import numpy as np
from numpy.random import default_rng


rng = default_rng()


class Genetic:
    """Class to execute training using a genetic algorithm.

    It's intent is to provided an API to train an algorithm with genetic
    algorithm without implementing it.
    The algorithm to tune should have free parameters, the expected bounds
    are [-1, 1] for each of them
    """

    DEFAULT_HYPER_PARAMETERS = {
        "crossover_alpha": 0.5,  # BLX-alpha crossover param, exploration parameter
        "NUM_b": 2,  # Non-Uniform Mutation b param, design parameter
        "mutation_prob": 0.5,  # The probability of mutation of one parameter
        "crossover_prob": 0.25,  # The probability of crossover for one chromosome
        "log": None,  # If None, doesn't log, otherwise log to the given file
    }

    def __init__(self, Algorithm, *init_parameters, **hyper_parameters):
        """Initilize a Genetic object with the given Algorithm class.

        The provided algorithm class should inherit from BaseAlgorithm.
        """
        if not issubclass(Algorithm, BaseAlgorithm):
            raise Exception(
                "The provided algorithm class should inherit from BaseAlgorithm."
            )

        self.Algorithm = Algorithm
        self.init_parameters = init_parameters
        self.hyper_parameters = self.DEFAULT_HYPER_PARAMETERS.copy()
        self.hyper_parameters.update(hyper_parameters)
        self.size = 0

    def populate(self, size):
        """Initialize the population of algorithm to be trained."""
        self.size = size
        self.population = [self.Algorithm(*self.init_parameters) for _ in range(size)]

    def train(self, n):
        """Train the population over n generations."""

        self.max_gen = n
        self.current_gen = 0
        self.log_data = {"scores": [], "params": []}

        for i in range(n):
            self.current_gen = i
            print(f"\r.....Training generation {i+1}/{n}", end="\t")
            self._evaluate()
            self._sort()
            if self.hyper_parameters["log"] is not None:
                self.log(self.population, i)
            self._evolve()

    def bests(self, n):
        """Return the n best algorithms."""
        self._sort()
        return self.population[:n]

    def _sort(self):
        """Sort the population according to the score of each algorithm."""
        self.population.sort(key=lambda al: al.score, reverse=True)

    def _evaluate(self):
        """Evaluate all the population.

            Update the total score of the population in order to be used later.
        """
        total_score = 0
        for algo in self.population:
            algo.evaluate()
            total_score += algo.score

        self.population_score = total_score

    def _evolve(self):
        """Make the whole population evolve.

        The population is crossed and mutated using the best algorithms.
        """
        new_generation = []

        # Elitism, keep 1% of bests without crossover and mutation
        elites_size = self.size // 100
        new_generation.extend(self.bests(elites_size))

        indexes = np.arange(self.size)
        if self.population_score == 0:
            probabilities = np.full(self.size, 1 / self.size)
        else:
            probabilities = []
            for algo in self.population:
                probabilities.append(algo.score / self.population_score)

        for _ in range(self.size - elites_size):
            parent1 = self._select_algorithm(indexes, probabilities)
            parent2 = self._select_algorithm(indexes, probabilities)

            if rng.random() < self.hyper_parameters["crossover_prob"]:
                child = self._crossover(parent1, parent2)
            else:
                if parent1.score > parent2.score:
                    child = deepcopy(parent1)
                else:
                    child = deepcopy(parent2)

            self._mutate(child)
            new_generation.append(child)

        self.population = new_generation

    def _select_algorithm(self, indexes, probabilities):
        """Return an algorithm of the population.

        The score of each algorithm can be see as a probability to be selected.
        """

        choosen = rng.choice(indexes, p=probabilities)
        return self.population[choosen]

    def _crossover(self, parent1, parent2):
        """Do a crossover of the two algorithms.

        Implement the BLX-alpha crossover.
        """
        child = self.Algorithm()

        alpha = self.hyper_parameters["crossover_alpha"]
        cmin = np.minimum(parent1.parameters, parent2.parameters)
        cmax = np.maximum(parent1.parameters, parent2.parameters)
        low = (1 + alpha) * cmin - alpha * cmax
        high = (1 + alpha) * cmax - alpha * cmin
        child.parameters = rng.uniform(low, high)

        return child

    def _mutate(self, algo):
        """Mutate the parameters of the algorihm  using non uniform mutation

        The mutation is applied on a subpart of the parameters..
        """
        parameters = algo.parameters  # Uses the getter defined in the class Algorithm
        power = (1 - self.current_gen / self.max_gen)

        for param_i in range(self.Algorithm.parameter_count):
            if rng.random() < self.hyper_parameters["mutation_prob"]:
                y = 1 - parameters[param_i] if rng.random() < 0.5 else -(parameters[param_i] + 1)
                u = rng.random()
                mutation = (1 - u ** power) ** self.hyper_parameters["NUM_b"]
                parameters[param_i] += y * mutation

        algo.parameters = parameters  # Uses the setter defined in the class Algorithm

    def log(self, population, generation):
        if generation % 5 != 0:
            # Allow periodoc log without big overhead
            return

        scores = [algo.score for algo in population]
        params = [algo.parameters for algo in population]

        self.log_data["scores"].append(scores)
        self.log_data["params"].append(params)

        np.save(self.hyper_parameters["log"], self.log_data)
