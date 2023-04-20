from gamebot.ai import BaseMinimaxMLP
from gamebot.genetics import Genetic
from gamebot.games.tictactoe import TictactoeEngine


class TictactoeMinimaxMLP(BaseMinimaxMLP):
    pass


def fight_function(player1, player2):
    # player1 is 0 and player2 is 1
    engine = TictactoeEngine(0)

    turns = 0

    while not engine.is_over():
        turns += 1
        if engine.current_player == 0:
            move = player1.run(engine.state)
        else:
            move = player2.run(engine.state)

        if not engine.algoPlay(move):
            raise ValueError("This is an invalid move, it should not happen")

    winner = engine.get_winner()
    if winner == -1:
        return 0, 0
    elif winner == 0:
        return 2 / turns, 0
    elif winner == 1:
        return 0, 2 / turns
    else:
        raise RuntimeError("WTF, check the code")


def run():
    genetic = Genetic(fight_function, TictactoeMinimaxMLP, (10, 5, 1), log="ttt-minimax.npy")
    genetic.populate(100)
    genetic.train(50)
