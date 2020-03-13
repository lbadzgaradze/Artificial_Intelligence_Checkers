

import abstractstrategy
import checkerboard

class Strategy(abstractstrategy.Strategy):
    """ The utility function is a subclass of Strategy, and
    the alpha-beta search is a separate function or class. Both must be contained within AI.py"""


    def utility(self, board):
        "Return the utility of the specified board"



        raise NotImplementedError("Subclass must implement")

    def play(self, board):
        """"play - Make a move
        Given a board, return (newboard, action) where newboard is
        the result of having applied action to board and action is
        determined via a game tree search (e.g. minimax with alpha-beta
        pruning).
        """

        """ alpha-beta pruning - Levan """
        """ treat everything modularity. Implement things and make sure it works first - Levan"""

        raise NotImplementedError("Subclass must implement")


#class Alpha_beta():