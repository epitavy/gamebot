from .engine import TictactoeEngine, TictactoeState
from .board_evaluation import TictactoeMinimax


def run():
    # The import statement is done here because of circular import otherwise
    from gamebot.interface import TictactoeCLI

    print("\nHello! Welcome in Tictactoe!\n")
    TictactoeCLI.run_cli()
