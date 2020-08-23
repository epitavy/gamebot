from .engine import TictactoeEngine
from .board_evaluation import TictactoeMinimax


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


"""All of this should be put in a separate file which purpose is more or less "game cli"."""


def to_sign(cell):
    if cell == -1:
        return " "
    elif cell == 0:
        return "x"
    else:
        return "o"


def print_board(board):
    for line in board:
        print(f"|{to_sign(line[0])}|{to_sign(line[1])}|{to_sign(line[2])}|")
        print("-------")
