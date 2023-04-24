from abc import ABC, abstractmethod


class BaseGameCLI(ABC):
    """This class provide a skeleton for cli based game.

    We suppose that the user input is a list of integer, it may change in future implementation
    but for now it fits all needs.
    """

    @classmethod
    @abstractmethod
    def parse_input(cls, player_input):
        """Parse input to engine format."""
        pass

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

    def _human_play(self):
        """Ask the user a move and plays it on the engine."""
        while True:
            try:
                player_sign = self.player_to_sign(self.engine.current_player)
                move = input(f"Player {player_sign}, enter your move:")
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
                if not self.engine.play(self.parse_input(move)):
                    print("Invalid move!")
                else:
                    self.print_board(self.engine.board)
                    break
            except Exception:
                continue

    def _bot_play(self):
        """Run the bot and play his move."""
        print(f"It is the bot turn ({self.player_to_sign(self.engine.current_player)})")
        move = self.bot.run(self.engine.state)

        if not self.engine.play(move):
            print("Error: The AI generates an invalid move!")
            exit(1)

        self.print_board(self.engine.board)

    def _end(self):
        """Display an end message on stdout."""
        print("Finished!")
        winner = self.engine.get_winner()
        if winner == -1:
            print("No player win, it's a tie!")
        else:
            print("Player", self.player_to_sign(winner), "won")

    def _ask_players_kind(self):
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
                        player1 = self._bot_play
                        break
                    elif asw[0].lower() == "h":
                        player1 = self._human_play
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
                        player2 = self._bot_play
                        break
                    elif asw[0].lower() == "h":
                        player2 = self._human_play
                        break
                    else:
                        print(
                            "Cannot understand which one of human or bot you choose, type again."
                        )
                break
            except EOFError:
                asw = input("\nDo you want to exit the game? y/n ")
                if asw[0].lower() == "y":
                    exit(0)
                else:
                    continue
            except Exception:
                print("Invalid input, start again.")

        return (player1, player2)

    def run_cli(self):
        """Run a game cli with the given engine and bot defined, as class attributes, until the game stops."""

        p0, p1 = self._ask_players_kind()

        while not self.engine.is_over():
            if self.engine.current_player == 0:
                p0()
            elif self.engine.current_player == 1:
                p1()
            else:
                raise NotImplementedError(
                    "Humm, the engine uses an unknown player... Sorry"
                )

        self._end()
