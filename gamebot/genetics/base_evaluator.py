from abc import ABC, abstractmethod


class BaseEvaluator(ABC):
    """Base class for every algorithm's evaluator."""

    @abstractmethod
    def evaluate(self, algorithm):
        """Run the algorithm on the evaluator and return a score."""
        pass

    @abstractmethod
    def reset(self):
        """Reset the evaluator to an initial state."""
        pass

    @property
    @abstractmethod
    def state(self):
        """Provide the evaluator state in order to be used by an algorithm."""
        pass


class BaseGameEvaluator(BaseEvaluator):
    """Base class for game evaluator. It subclasses BasEvaluator to provide a richer API."""

    def evaluate(self, algorithm, n=1):
        """Use the algorithm to play until the game is over. Return the score.

        The parameter n is used to evaluate the algorithm multiple time, in order to be more accurate.
        """
        score = 0
        for _ in range(n):
            self.reset()

            while not self.is_over():
                move = algorithm.run(self.state)
                self.algoPlay(move)

            score += self.scoring()
        return score // n

    @abstractmethod
    def reset(self):
        """After a reset, scoring should return 0."""
        pass

    @abstractmethod
    def algoPlay(self, move):
        """Play the given move for the algorithm.

        It is called by the genetic mechanic, it can be usefull if special treatment should
        be done before or after the AI plays.
        """
        pass

    @abstractmethod
    def play(self, move):
        """Play the given move. This move can be from any player."""
        pass

    @abstractmethod
    def scoring(self):
        """Get the score for the algorithm player."""
        pass

    @abstractmethod
    def is_over(self):
        """Return True is the game is over, i.e. no move can be played."""
        pass

    @abstractmethod
    def get_winner(self):
        """Return the player that won, -1 if it is a tie or None if it cannot be deduced yet."""
        pass

    @property
    @abstractmethod
    def state(self):
        """Return the current state of the game. It may be normalized for the algorithm input."""
        pass
