import pytest
import numpy as np

from gamebot.genetics import Genetic

# DISCLAIMER: The tests here are subject to failure due to the inherent random nature of the
# genetic algorithm. The tests are designed to minimize as much as possible the risk of failure.
# Rerunning the test ONLY ONCE should be sufficient, otherwise something is possibly broken.


def test_genetics_setup(algo_one_param):

    genetic = Genetic(algo_one_param)
    assert genetic.size == 0

    genetic.populate(66)
    assert genetic.size == 66
    assert len(genetic.population) == 66
    assert isinstance(genetic.population[0], algo_one_param)


def test_dummy_one_free_param(algo_one_param):
    genetic = Genetic(algo_one_param, mutation_prob=0.25)
    genetic.populate(100)
    genetic.train(200)

    best_algo = genetic.bests(1)[0]
    assert best_algo.parameters == pytest.approx([0.8], abs=1e-3)
    assert best_algo.score == pytest.approx(20, abs=1e-2)


def test_dummy_five_params(algo_five_params):
    genetic = Genetic(algo_five_params, mutation_prob=0.25)
    genetic.populate(100)
    genetic.train(200)

    best_algo = genetic.bests(1)[0]
    assert np.sum(best_algo.parameters) == pytest.approx(5, abs=1e-1)


def test_minimization_sixhump_camelback(algo_sixhump_camelback):
    genetic = Genetic(algo_sixhump_camelback, mutation_prob=0.25)
    genetic.populate(100)
    genetic.train(200)

    best_algo = genetic.bests(1)[0]
    assert best_algo.score == pytest.approx(10, abs=1e-2)


def test_minimization_stepwise(algo_stepwise):
    genetic = Genetic(algo_stepwise, mutation_prob=0.25)
    genetic.populate(100)
    genetic.train(200)

    best_algo = genetic.bests(1)[0]
    assert best_algo.score == pytest.approx(5120, abs=1)
