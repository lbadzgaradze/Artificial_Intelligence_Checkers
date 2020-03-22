import abstractstrategy
import checkerboard


class Minimax:
    """ Created by Levan
    The Minimax class uses minimax algorithm for determining the best move for the
    AI player in checkers. Generic minimax algorithm is enhanced with alpha beta pruning (which
    does not change the decision of the minimax algorithm) and utility function is replaced by
    heuristic evaluation function (approximation) at the the specified cutoff (we call this
    parameter max_plies). We use utility and heuristic evaluation function interchangeably
    in this code."""

    """the following variables are designed to be shared by all instances of Minimax class."""
    pos_infinity = float("inf")
    neg_infinity = float("-inf")

    """ actual utilities of terminal (leaf) nodes in search tree"""
    utility_win = 1000  # actual utility of winning
    utility_lose = -1000  # actual utility of losing
    utility_tie = 0  # actual utility of a draw

    def __init__(self, max_player, min_player, max_plies, strategy):
        """ the max_player - the player whose best move we are determining.
            the min_player - the other player. It is assumed that min_player plays
                a perfect game.
            max_plies - a parameter indicating where the cutoff should be applied
            strategy - an instance of the class containing heuristic evaluation function"""
        self.max_player = max_player
        self.min_player = min_player
        self.max_plies = max_plies
        self.strategy = strategy

    def Game_Over_Utility(self, winner):
        """Game_Over_Utility returns the utility of the end of the game based on the winner:
        'r', 'b' or None. None indicates a tie - there is no winner"""
        if winner is None:  # tie
            return Minimax.utility_tie
        elif winner == self.max_player:  # win
            return Minimax.utility_win
        else:  # loss
            return Minimax.utility_lose

    def Cut_Off_Test(self, ply_counter):
        """This method checks if sufficient depth in the search tree
        has been reached to apply cutoff function"""
        return ply_counter >= self.max_plies

    def Alpha_Beta_Search(self, current_board_state):
        """This method uses alpha-beta search to determine the best move for MAX
        player based on the current configuration of the checkerboard. It returns
        the action which will result in the value v (the highest utility). This
        portion of the code is based on Figure 5.7 from our textbook (chp 5)
        with appropriate modifications introduced

        current_board_state - the representation of the current configuration
        of the checkerboard"""

        """ alpha - the value of the best (i.e., highest-value) choice we have 
                found so far at any choice point along the path for MAX.
            Beta - the value of the best (i.e., lowest-value) choice we have 
            found so far at any choice point along the path for MIN."""

        alpha = self.neg_infinity
        beta = self.pos_infinity
        # variable ply_counter will keep count of how many plies "deep" the search goes
        # As suggested in out textbook, we keep a counter that is updated during every
        # recursive call
        ply_counter = 1

        maximum_utility, best_move = self.Max_Value(current_board_state, alpha, beta, ply_counter)
        return best_move

    def Max_Value(self, current_board_state, alpha, beta, ply_counter):
        """This method returns the utility value of the best
        action from the Max player's point of view and the action
        leading to that utility value

        current_board_state - the representation of the current configuration
        of the checkerboard
        alpha - the value of the best (i.e., highest-value) choice we have
        found so far at any choice point along the path for MAX.
        Beta - the value of the best (i.e., lowest-value) choice we have
        found so far at any choice point along the path for MIN.
        """

        alpha_ = alpha
        beta_ = beta

        """this ply could be a terminal state, we can check that by using
        is_terminal() function implemented in checkerboard.py. In case,
        the current ply is terminal we do not need to approximate utility by
        using heuristic evaluation function, we can just return the utility
        of winning, losing, or a tie."""

        (game_over, winner) = current_board_state.is_terminal()
        if game_over:
            # return actual utility
            return self.Game_Over_Utility(winner)
        elif self.Cut_Off_Test(ply_counter):
            # return approximation of the utility
            return self.strategy(current_board_state)
        else:
            # go deeper down the search tree

            # v_maximum_utility is used as an index to retrieve best move from choices
            # v_maximum_utility will never stay negative infinity since even if the loss
            # of the game is encountered, it is marked by -1000 > float("-inf")
            v_maximum_utility = float("-inf")
            # 'choices' dictionary will hold all the possible moves indexed by utility
            # associated with the move. If there are multiple moves resulting in the
            # same utility, then the last one encountered will be saved and selected later.
            choices = {}
            # actions is the list of valid actions actions should not be an empty
            # list since we have already checked if state was terminal. If player does
            # not have any moves then state is terminal
            actions = current_board_state.get_actions(self.max_player)

            for action in actions:
                resulting_child_node = current_board_state.move(action)
                current_utility, move = self.Min_Value(resulting_child_node, alpha_, beta_, ply_counter + 1)
                choices.update({current_utility: action})
                v_maximum_utility = max(v_maximum_utility, current_utility)

                if v_maximum_utility >= beta_:
                    return v_maximum_utility, action
                alpha_ = max(alpha_, v_maximum_utility)
            return v_maximum_utility, choices[v_maximum_utility]

    def Min_Value(self, current_board_state, alpha, beta, ply_counter):
        """This method returns the utility value of the best
        action from the Min player's point of view, the worst
        action from the Max player's point of view, and the action
        leading to that utility value

        current_board_state - the representation of the current configuration
        of the checkerboard
        alpha - the value of the best (i.e., highest-value) choice we have
        found so far at any choice point along the path for MAX.
        Beta - the value of the best (i.e., lowest-value) choice we have
        found so far at any choice point along the path for MIN."""

        _alpha = alpha
        _beta = beta

        """this ply could be a terminal state, we can check that by using
        is_terminal() function implemented in checkerboard.py. In case,
        the current ply is terminal we do not need to approximate utility by
        using heuristic evaluation function, we can just return the utility
        of winning, losing, or a tie."""

        (game_over, winner) = current_board_state.is_terminal()
        if game_over:
            # return actual utility
            return self.Game_Over_Utility(winner)
        elif self.Cut_Off_Test(ply_counter):
            # return approximation of the utility
            return self.strategy(current_board_state)
        else:
            # go deeper down the search tree

            # v_minimum_utility is used as an index to retrieve best move (for min)
            # from choices
            # v_minimum_utility will never positive infinity since even if the win
            # of the game is encountered, it is marked by 1000 < float("inf")
            v_minimum_utility = float("inf")
            # 'choices' dictionary will hold all the possible moves indexed by utility
            # associated with the move. If there are multiple moves resulting in the
            # same utility, then the last one encountered will be saved and selected.
            choices = {}
            # actions is the list of valid actions actions should not be an empty
            # list since we have already checked if state was terminal. If player does
            # not have any moves then state is terminal
            actions = current_board_state.get_actions(self.min_player)

            for action in actions:
                resulting_child_node = current_board_state.move(action)
                current_utility, move = self.Max_Value(resulting_child_node, _alpha, _beta, ply_counter + 1)
                choices.update({current_utility: action})
                v_minimum_utility = min(v_minimum_utility, current_utility)
                if v_minimum_utility <= _alpha:
                    return v_minimum_utility, action
                _beta = min(_beta, v_minimum_utility)
            return v_minimum_utility, choices[v_minimum_utility]


class AI(abstractstrategy.Strategy):
    """AI player using Minimax with alpha-beta pruning algorithm to play checkers"""

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

    """ The utility function is a subclass of Strategy, and
    the alpha-beta search is a separate function or class. Both must be contained within AI.py"""

    def utility(self, board):
        "Return the utility of the specified board"

        raise NotImplementedError("Subclass must implement")

# class Alpha_beta():
