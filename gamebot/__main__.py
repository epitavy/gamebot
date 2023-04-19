import sys
import gamebot.games.tictactoe as tictactoe

GAMES = {"tictactoe": tictactoe}

if len(sys.argv) != 2:
    print(f"Usage:\n\t{sys.argv[0]} <game>\nGames:\n", end="", file=sys.stderr)
    for game in GAMES:
        print(f"\t{game.capitalize()}")
    exit(1)
else:
    if sys.argv[1] not in GAMES:
        print(f"The game {sys.argv[1]} is not available", file=sys.stderr)
        exit(1)

    game = GAMES[sys.argv[1]]
    game.run()
