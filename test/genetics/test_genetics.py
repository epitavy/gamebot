from gamebot.genetics import Genetic
from conftest import DummyMaximazerAlgo


def test_easy_training(dummy_genetics):
    dummy_genetics.train(100)
    best_algo = dummy_genetics.bests(1)[0]
    param = best_algo.p

    expected = 8

    assert abs(param - expected) < 0.15


def avg(array):
    return sum(array) / len(array)


def test_easy_workflow():
    gen = Genetic(
        DummyMaximazerAlgo, 0, 4, 18, 10, 3, crossover_point=0.1, mutation_variance=0.2
    )
    gen.populate(200)

    # Verify that the score is globally growing
    last_avg = 0
    for i in range(100):
        gen.train(1)
        bests = gen.bests(100)
        curr_avg = avg((b.score for b in bests))
        assert curr_avg >= last_avg
        last_avg = avg
