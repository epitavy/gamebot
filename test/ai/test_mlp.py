import pytest

from gamebot.ai.mlp import MLP


def test_mpl_dummy1():
    mlp = MLP((1, 1))
    mlp.layers[0] = ([1, 0])

    assert mlp.forward_propagation([1]) == [1]


def test_mpl_dummy2():
    mlp = MLP((2, 2, 1))
    mlp.layers[0] = ([[5, 2], [-0.2, -4.3]], [0.9, 1])
    mlp.layers[1] = ([[0.46, 0.44]], [-0.3])

    assert mlp.forward_propagation([1, 1]) == pytest.approx([3.334])


def test_mpl_dummy3():
    mlp = MLP((2, 2, 1))
    mlp.layers[0] = ([[5, 2], [-0.2, -4.3]], [0.9, 1])
    mlp.layers[1] = ([[0.46, 0.44]], [-0.3])

    assert mlp.forward_propagation([-0.45, 0.79]) == pytest.approx([-0.1941999])
