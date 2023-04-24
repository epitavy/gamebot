import argparse
import gamebot.games.tictactoe as tictactoe
import gamebot.games.connect4 as connect4

GAMES = {"tictactoe": tictactoe,
         "connect4": connect4}

parser = argparse.ArgumentParser()
parser.add_argument("game", choices=list(GAMES.keys()))
parser.add_argument("--training", action="store_true")
parser.add_argument("--benchmark", help="File to benchmark")
args = parser.parse_args()

game = GAMES[args.game]

if args.training:
    game.training.run()
elif args.benchmark:
    game.benchmark.run(args.benchmark)
else:
    game.run()
