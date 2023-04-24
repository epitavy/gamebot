import pathlib

import matplotlib.pyplot as plt
import numpy as np

from .training import fight_function, TictactoeMinimaxMLP

def run(filepath):
    reference = pathlib.Path(__file__).parent.resolve() / 'ref_training.npy'
    ref_data = np.load(reference, allow_pickle=True).item()
    ref_generations_score = np.array(ref_data['fitnesses'])
    ref_bests_params = np.array(ref_data['params_of_the_best_one'])


    bench_data = np.load(filepath, allow_pickle=True).item()
    bench_generations_score = np.array(bench_data['fitnesses'])
    bench_bests_params = np.array(bench_data['params_of_the_best_one'])


    plt.figure()
    plt.title("Fitness difference")
    plt.xlabel("Generation")
    plt.plot(abs(ref_generations_score[:,0] - bench_generations_score[:,0]))
    plt.show(block=False)

    ref_algos = [TictactoeMinimaxMLP((10, 5, 1), 1, weights=p) for p in ref_bests_params]
    bench_algos = [TictactoeMinimaxMLP((10, 5, 1), 1, weights=p) for p in bench_bests_params]

    bench_scores = []

    for i, algo in enumerate(bench_algos):
        print(f"\rFighting algo n°{i+1}", end="")
        score = 0
        for opponent in ref_algos:
            s, _ = fight_function(algo, opponent, turn_normalization=False)
            score += s

        bench_scores.append(score)
    print()

    plt.figure()
    plt.title("Score against reference")
    plt.xlabel("Generation")
    ax1 = plt.gca()
    ax2.tick_params(colors="tab:blue", which="both")
    ax1.plot(bench_scores, label="Number of wins", color="tab:blue")

    ax2 = plt.twinx()
    ax2.tick_params(colors="orange", which="both")
    ax2.plot(bench_generations_score[:, 0], label="Fitness", color="orange")

    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")
    plt.show()
