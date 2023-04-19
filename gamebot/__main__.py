import argparse
import gamebot.games.tictactoe as tictactoe

GAMES = {"tictactoe": tictactoe}

parser = argparse.ArgumentParser()
parser.add_argument("game", choices=list(GAMES.keys()))
args = parser.parse_args()

game = GAMES[args.game]
game.run()
