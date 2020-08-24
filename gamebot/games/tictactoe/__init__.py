from .engine import TictactoeEngine, TictactoeState
from .board_evaluation import TictactoeMinimax
from gamebot.interface.tictactoe_cli import *


def run():
    game = TictactoeEngine(1)
    bot = TictactoeMinimax()
    bot.max_depth = 7

    print_board(game.board)
    while not game.is_over():
        if game.current_player == 0:  # AI plays
            move = bot.run(game.state)

            print(move)
            if not game.algoPlay(move):
                print("Error: The AI generates an invalid move!")
                exit(1)

            print_board(game.board)
            continue

        try:
            x, y = input(f"Move {to_sign(game.current_player)}: ").split(" ")
        except EOFError:
            asw = input("\rDo you want to exit the game? y/n ")
            if asw[0].lower() == "y":
                exit(0)
            else:
                continue
        except Exception:
            print("Bad input, try again")
            continue

        if not game.play((int(x), int(y))):
            print("Invalid move!")
        else:
            print_board(game.board)

    print("Finished!")
    winner = game.get_winner()
    if winner == -1:
        print("No player win, it's a tie!")
    else:
        print("Player", to_sign(winner), "win")
