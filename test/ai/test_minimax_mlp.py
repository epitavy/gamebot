import numpy as np

from gamebot.ai import BaseMinimaxMLP


def test_parameters_property():
    mmlp = DummyMinimaxMLP((10, 10, 10, 1))

    assert len(mmlp.parameters) == 231

    save = np.array(mmlp.mlp.layers, dtype=object)

    # Ensure no modification happens
    for _ in range(10):
        params = mmlp.parameters
        mmlp.parameters = params

    for layer_save, layer in zip(save, mmlp.mlp.layers):
        assert np.all(layer_save[0] == layer[0])
        assert np.all(layer_save[1] == layer[1])


class DummyMinimaxMLP(BaseMinimaxMLP):
     def evaluator(self):
        pass
