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
                # this portion of the code heavily relies on algorithm outlined
                # on Figure 5.7 on pg. 170 of our textbook. We are borrowing
                # from the pseudocode and translating
                resulting_child_node = current_board_state.move(action)
                current_utility, move = self.Min_Value(resulting_child_node, alpha_, beta_, ply_counter + 1)
                # add utility and action pair to choices
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
                # this portion of the code heavily relies on algorithm outlined
                # on Figure 5.7 on pg. 170 of our textbook. We are borrowing
                # from the pseudocode and translating
                resulting_child_node = current_board_state.move(action)
                current_utility, move = self.Max_Value(resulting_child_node, _alpha, _beta, ply_counter + 1)
                # add utility and action pair to choices
                choices.update({current_utility: action})
                v_minimum_utility = min(v_minimum_utility, current_utility)
                if v_minimum_utility <= _alpha:
                    return v_minimum_utility, action
                _beta = min(_beta, v_minimum_utility)
            return v_minimum_utility, choices[v_minimum_utility]


class AI(abstractstrategy.Strategy):
    """ Created by Levan
    AI is a checker playing strategy class using Minimax with alpha-beta pruning algorithm
    to play checkers and heuristic evaluation function - utility function to evaluate current
    state of the checkerboard"""

    def __init__(self, player, game, max_plies):
        # calls abstractstrategy.Strategy's constructor
        super(AI, self).__init__(player, game, max_plies)
        # instantiating a searching methodology class Minimax defined above
        self.searching_strategy = Minimax(self.maxplayer, self.minplayer, self.maxplies, self)

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
        """utility is heuristic evaluation function (a weighted linear function, to be precise) - it
        approximates utility of the given checkerboard from the MAX player's viewpoint, in other words
        determines strength of the current checkerboard configuration relative to the MAX player.

        The following function computes several features known to be an important predictor
        of checks game outcome. This analysis heavily relies on the article "Basic Strategies
        for Winning at Checkers" Written by Seth Brow available here:
        https://www.thesprucecrafts.com/how-to-win-at-checkers-411170  """

        # total utility that this method will return
        utility = 0

        # index of max player
        self.maxplayer_index = board.playeridx(self.maxplayer)

        # feature 1: Percentage difference of the amount of player's pawns and enemy's pawns
        # feature 2: Percentage difference of the amount of player's kings and enemy's kings
        pawn_p_difference, king_p_difference = self.Pawn_Perc_Diff(board)

        # feature 3: the difference between the amount of pieces on the home row for maxplayer
        # and the amount of enemy pieces on the enemy home row
        relative_home_row_count = self.Home_Row_Pieces(board)

        # feature 4: difference between the amount of maxplayer and enemy pieces on the edge columns
        relative_edge_count = self.Edge_Piece_Count(board)

        # w_{i} is the weight for the ith feature
        w_1, w_2, w_3 = 1, 2, 5

        utility = int(
            w_1 * pawn_p_difference + w_2 * king_p_difference + w_3 * relative_home_row_count)

        return utility

    def Pawn_Perc_Diff(self, board):
        """Pawn_Diff returns Percentage difference of the amount of player's pawns and enemy's pawns and
        Percentage difference of the amount of player's kings and enemy's kings.

        Percentage difference here is calculated to equal the change in value, divided by the average of
        the 2 numbers, all multiplied by 100. We retain + or - sign, since we want to evaluate from MAX
        player's point of view.

        The reasoning behind using percentage difference instead of the simple difference is to account
        for the fact that advantage of number of pieces is far more important when the total amount of pieces
        on the board is small. "With only 12 pieces on the board, to begin with, you may quickly end up with
        an 8-7 piece advantage. This may not seem like a big deal, but if you can trade four pieces, you
        suddenly have a 4-3 advantage, which is a tremendous amount of power." """

        board.recount_pieces()  # this will probably slow it down ???
        self.maxplayer_index = board.playeridx(self.maxplayer)
        # the following lists contain number of pieces indexed by playerindex
        pawns = board.get_pawnsN()
        kings = board.get_kingsN()

        max_player_index = self.maxplayer_index
        min_player_index = (max_player_index + 1) % 2

        player_pawns = pawns[max_player_index]
        player_kings = kings[max_player_index]
        enemy_pawns = pawns[min_player_index]
        enemy_kings = kings[min_player_index]

        pawn_difference = int((player_pawns - enemy_pawns) / (
                    (player_pawns + enemy_pawns) / 2.0) * 100) if player_pawns + enemy_pawns > 0 else 0
        king_difference = int((player_kings - enemy_kings) / (
                (player_kings + enemy_kings) / 2.0) * 100) if player_kings + enemy_kings > 0 else 0

        return pawn_difference, king_difference

    def Home_Row_Pieces(self, board):
        """Home_Row_Pieces return the difference between the amount of pieces on the home
        row for maxplayer and enemy. Keeping pieces on the home row is a good strategy since
        it will prevent enemy from getting their pieces kinged"""
        self.maxplayer_index = board.playeridx(self.maxplayer)

        direction = board.pawnmoves[self.maxplayer][0][0]
        home_row, enemy_home_row = (7, 0) if direction < 0 else (0, 7)

        home_row_piece_count = 0
        for c in range(board.coloffset[home_row], board.cols, board.step):
            # there is a piece and piece belongs to the "home owner"
            if board.board[home_row][c] and \
                    board.board[home_row][c] in board.players[self.maxplayer_index]:
                home_row_piece_count += 1

        enemy_home_piece_count = 0
        for c in range(board.coloffset[enemy_home_row], board.cols, board.step):
            # there is a piece and piece belongs to the enemy
            if board.board[enemy_home_row][c] and \
                    board.board[enemy_home_row][c] in board.players[(self.maxplayer_index + 1) % 2]:
                enemy_home_piece_count += 1

        return home_row_piece_count - enemy_home_piece_count

    def Edge_Piece_Count(self, board):
        """Edge_Piece_Count returns the difference between the amount of maxplayer and enemy pieces on the edge
        columns.
        "For beginners, the first strategy one often figures out is to place your checkers on the edge of
        the board. This seems like a reasonable Checkers strategy because your pieces on the edge cannot be captured.
        But as it turns out, while this may be a tempting strategy in your first games, pushing your checkers to the
        edges is a mistake." """
        pieces_on_edge = 0
        # STOPPED HERE
