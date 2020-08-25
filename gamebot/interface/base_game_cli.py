from abc import ABC, abstractmethod


class BaseGameCLI(ABC):
    """This class provide a skeleton for cli based game.

    We suppose that the user input is a list of integer, it may change in future implementation
    but for now it fits all needs.
    """

    @property
    def engine(self):
        """Class attribute that should be defined in sub classes and be a sub class of BaseGameEvaluator."""
        raise NotImplemented(
            "You should define the engine class attribute in sub classes"
        )

    @property
    def bot(self):
        """Class attribute that should be defined in sub classes and be a sub class of BaseAlgorithm."""
        raise NotImplemented("You should define the bot class attribute in sub classes")

    @classmethod
    @abstractmethod
    def player_to_sign(cls, cell):
        """Convert the given cell into a nice symbol for the player.

        It can be a single char, used in `print_board`.
        """
        pass

    @classmethod
    @abstractmethod
    def print_board(cls, board):
        """Print the given board on stdout."""
        pass

    @classmethod
    def _human_play(cls):
        """Ask the user a move and plays it on the engine."""
        while True:
            try:
                move = input(
                    f"Move {cls.player_to_sign(cls.engine.current_player)}: "
                ).split(" ")
            except EOFError:
                asw = input("\rDo you want to exit the game? y/n ")
                if asw[0].lower() == "y":
                    exit(0)
                else:
                    continue
            except Exception:
                print("Bad input, try again")
                continue

            try:
                # We suppose the move is a tuple of integers
                if not cls.engine.play(tuple((int(x) for x in move))):
                    print("Invalid move!")
                else:
                    cls.print_board(cls.engine.board)
                    break
            except ValueError:
                print("You should use only numbers!")
                continue

    @classmethod
    def _bot_play(cls):
        """Run the bot and play his move."""
        print("It is the bot turn")
        move = cls.bot.run(cls.engine.state)

        if not cls.engine.algoPlay(move):
            print("Error: The AI generates an invalid move!")
            exit(1)

        cls.print_board(cls.engine.board)

    @classmethod
    def _end(cls):
        """Display an end message on stdout."""
        print("Finished!")
        winner = cls.engine.get_winner()
        if winner == -1:
            print("No player win, it's a tie!")
        else:
            print("Player", cls.player_to_sign(winner), "win")

    @classmethod
    def _ask_players_kind(cls):
        """Ask the user which of human or bot should the players be.

        Return in a tuple the function to call for player 1 and 2.
        """
        while True:
            try:
                while True:
                    asw = input(
                        "Should the FIRST player be a human or a bot? human/bot "
                    )
                    if asw[0].lower() == "b":
                        player1 = cls._bot_play
                        break
                    elif asw[0].lower() == "h":
                        player1 = cls._human_play
                        break
                    else:
                        print(
                            "Cannot understand which one of human or bot you choose, type again."
                        )
                while True:
                    asw = input(
                        "Should the SECOND player be a human or a bot? human/bot "
                    )
                    if asw[0].lower() == "b":
                        player2 = cls._bot_play
                        break
                    elif asw[0].lower() == "h":
                        player2 = cls._human_play
                        break
                    else:
                        print(
                            "Cannot understand which one of human or bot you choose, type again."
                        )
            except EOFError:
                asw = input("\nDo you want to exit the game? y/n ")
                if asw[0].lower() == "y":
                    exit(0)
                else:
                    continue
            except Exception:
                print("Invalid input, start again.")

            return (player1, player2)

    @classmethod
    def run_cli(cls):
        """Run a game cli with the given engine and bot defined, as class attributes, until the game stops."""

        p0, p1 = cls._ask_players_kind()

        cls.print_board(cls.engine.board)
        while not cls.engine.is_over():
            if cls.engine.current_player == 0:
                p0()
            elif cls.engine.current_player == 1:
                p1()
            else:
                raise NotImplemented(
                    "Humm, the engine uses an unknowed player... Sorry"
                )

        cls._end()
