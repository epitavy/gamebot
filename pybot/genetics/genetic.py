from .base_algorithm import BaseAlgorithm
import numpy as np
import copy


class Genetic:
    """Class to execute training using a genetic algorithm.

    It's intent is to provided an API to train an algorithm with genetic
    algorithm without implementing it.
    The algorithm to tune should have free parameters.
    """

    DEFAULT_HYPER_PARAMETERS = {
        "crossover_point": 0.2,  # The point where the crossover between two algo is made
        "mutation_prob": 0.1,  # The probability of mutation of one parameter
        "mutation_variance": 0.4,  # The variance used in the normal distribution for the mutation
        "mutation_mean": 0.5,  # The mean used in the normal distribution for the mutation
        "log": None,  # If None, doesn't log, otherwise log to the given file
    }

    def __init__(self, Algorithm, *init_parameters, **hyper_parameters):
        """Initilize a Genetic object with the given Algorithm class.

        The provided algorithm class should inherit from BaseAlgorithm.
        """
        if not issubclass(Algorithm, BaseAlgorithm):
            raise Exception("The provided algorithm class should inherit from BaseAlgorithm.")

        self.Algorithm = Algorithm
        self.default_algo_params = init_parameters if init_parameters else [0, 0, 0, 0, 0]
        self.hyper_parameters = self.DEFAULT_HYPER_PARAMETERS.copy()
        self.hyper_parameters.update(hyper_parameters)

    def populate(self, size):
        """Initialize the population of algorithm to be trained."""
        self.size = size
        self.population = [
            self.Algorithm(params=self.default_algo_params) for _ in range(size)
        ]

    def train(self, n):
        """Train the population over n generations."""
        for i in range(n):
            print(f"\r.....Training generation {i+1}/{n}", end="\t")
            self._evaluate()
            self._sort()
            if self.hyper_parameters["log"] is not None:
                Genetic.log(self.hyper_parameters["log"], self.population, i)
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

        The population is crossed and mutated. The best algorithms
        are choosen to be crossed and mutated according to some parameters.
        """
        new_generation = []

        # This calculation is done here because of the big overhead if done in _select_algorithm
        indexes = np.arange(self.size)
        if self.population_score == 0:
            probabilities = np.full(self.size, 1 / self.size) # Every algo has the same proba
        else:
            probabilities = []
            for algo in self.population:
                probabilities.append(algo.score / self.population_score)

        for _ in range(self.size):
            parent1 = self._select_algorithm(indexes, probabilities)
            parent2 = self._select_algorithm(indexes, probabilities)
            evolved = self._cross_mutate(parent1, parent2)
            new_generation.append(evolved)

        self.population = new_generation

    def _select_algorithm(self, indexes, probabilities):
        """Return an algorithm of the population.

        The score of each algorithm can be see as a probability to be selected.
        """

        choosen = np.random.choice(indexes, p=probabilities)
        return self.population[choosen]

    def _cross_mutate(self, algo1, algo2):
        """Do a crossover of the two algorithms and mutate the resulting one"""
        child = copy.deepcopy(algo1)
        crossover_index = int(
            self.hyper_parameters["crossover_point"] * self.Algorithm.parameter_count()
        )
        child.parameters[crossover_index:] = algo2.parameters[crossover_index:]
        self._mutate(child)

        return child

    def _mutate(self, algo):
        """Mutate the parameters of the algorihm.

        By default, the parameters are expected to be in the interval [0, 1].
        The mutation is applied on a subpart of the parameters. Each mutation follows a normal
        distribution.
        """
        mutation_mean = self.hyper_parameters["mutation_mean"]
        mutation_variance = self.hyper_parameters["mutation_variance"]

        parameters = algo.parameters  # Uses the getter defined in the class Algorithm

        for param_i in range(self.Algorithm.parameter_count()):
            if np.random.ranf() < self.hyper_parameters["mutation_prob"]:
                mutation = np.random.normal(mutation_mean, mutation_variance)
                parameters[param_i] += mutation
                # This is because the mean (resp. variance) of the sum of two normal
                # distributed variables is the sum of the means (resp. variances).
                # Thus, to divide by two makes the mean (resp. variance) keep
                # stable over the mutations and the parameters stay in the range [0, 1]
                parameters[param_i] /= 2

        algo.parameters = parameters  # Uses the setter defined in the class Algorithm

    @staticmethod
    def log(path, population, generation):
        mode = "a"
        if generation == 0:
            mode = "w"

        content = " ".join((str(algo.score) for algo in population))
        with open(path + "-scores.log.raw", mode) as file:
            file.write(f"{generation} {content}\n")

        with open(path + "-params.log.raw", mode) as file:
            if generation == 0:
                file.write(f"{len(population)}\n")
            for algo in population:
                params = " ".join((str(p) for p in algo.parameters))
                file.write(f"{params}\n")
