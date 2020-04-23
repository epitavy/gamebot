from pybot.genetics import Genetic


def test_easy_training(dummy_genetics):
    dummy_genetics.train(100)
    best_algo = dummy_genetics.bests(1)[0]
    param = best_algo.p

    expected = 5

    assert abs(param - expected) < 0.1
