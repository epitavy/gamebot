if __name__ == "__main__":
    import sys
    import pybot

    if len(sys.argv) != 2:
        print(f"Usage:\n\t{sys.argv[0]} <game>\nGames:\n\ttictactoe", file=sys.stderr)
        exit(1)
    else:
        if sys.argv[1] not in games:
            print(f"The game {sys.argv[1]} is not available", file=sys.stderr)
            exit(1)

        games = {"tictactoe": "import pybot.games.tictactoe as game"}
        exec(games[sys.argv[1]])
        game.run()
