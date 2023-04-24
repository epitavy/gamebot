from .engine import Connect4Engine, Connect4State
from . import training


def run():
    # The import statement is done here because of circular import otherwise
    from gamebot.interface import Connect4CLI

    print("\nHello! Welcome in Connect4!\n")
    Connect4CLI().run_cli()

