import abstractstrategy
import checkerboard


class Minimax:
    """The Minimax class uses minimax algorithm for determining the best move for the AI player in checkers. Generic
    minimax algorithm is enhanced with alpha beta pruning (which does not change the decision of the minimax
    algorithm) and utility function is replaced by heuristic evaluation function (approximation) at the specified
    cutoff (we call this parameter max_plies). We use utility and heuristic evaluation function interchangeably in
    this code. """

    # the following variables are designed to be shared by all instances of Minimax class.
    pos_infinity = float("inf")
    neg_infinity = float("-inf")
    # actual utilities of terminal (leaf) nodes in search tree
    utility_win = 1000000  # actual utility of winning
    utility_lose = -1000000  # actual utility of losing
    utility_tie = 0  # actual utility of a draw

    def __init__(self, max_player, min_player, max_plies, strategy):
        """ the max_player - the player whose best move we are determining. the min_player - the other player. It is
        assumed that min_player plays a perfect game. max_plies - a parameter indicating where the cutoff should be
        applied strategy - an instance of the class containing heuristic evaluation function """

        self.max_player = max_player
        self.min_player = min_player
        self.max_plies = max_plies
        self.strategy = strategy

    def Game_Over_Utility(self, winner):
        """Game_Over_Utility returns the utility of the end of the game based on the winner: 'r', 'b' or None. None
        indicates a tie - there is no winner """
        if winner is None:  # tie
            return Minimax.utility_tie
        elif winner == self.max_player:  # win
            return Minimax.utility_win
        else:  # loss
            return Minimax.utility_lose

    def Cut_Off_Test(self, ply_counter):
        """This method checks if sufficient depth in the search tree has been reached to apply cutoff function"""
        return ply_counter >= self.max_plies

    def Alpha_Beta_Search(self, current_board_state):
        """This method uses alpha-beta search to determine the best move for MAX player based on the current
        configuration of the checkerboard. It returns the action which will result in the value v (the highest
        utility). This portion of the code is based on Figure 5.7 from our textbook (chp 5) with appropriate
        modifications introduced

        current_board_state - the representation of the current configuration of the checkerboard

        alpha - the value of the best (i.e., highest-value) choice we have found so far at any choice point along the
        path for MAX.
        beta - the value of the best (i.e., lowest-value) choice we have found so far at any choice point along the
        path for MIN. """

        alpha = self.neg_infinity
        beta = self.pos_infinity
        # variable ply_counter will keep count of how many plies "deep" the search goes
        # As suggested in out textbook, we keep a counter that is updated during every
        # recursive call
        ply_counter = 1

        maximum_utility, best_move = self.Max_Value(current_board_state, alpha, beta, ply_counter)
        return best_move

    def Max_Value(self, current_board_state, alpha, beta, ply_counter): # when does this return None ???
        """This method returns the utility value of the best action from the Max player's point of view and the
        action leading to that utility value

        alpha - the value of the best (i.e., highest-value) choice we have found so far at any choice point along the
        path for MAX.
        beta - the value of the best (i.e., lowest-value) choice we have found so far at any choice point along the
        path for MIN.
        """

        alpha_ = alpha
        beta_ = beta

        """this ply could be a terminal state, we can check that by using is_terminal() function implemented in 
        checkerboard.py. In case, the current ply is terminal we do not need to approximate utility by using 
        heuristic evaluation function, we can just return the utility of winning, losing, or a tie. """

        (game_over, winner) = current_board_state.is_terminal()
        if game_over:
            # return actual utility
            return self.Game_Over_Utility(winner), None
        elif self.Cut_Off_Test(ply_counter):
            # return approximation of the utility
            return self.strategy(current_board_state), None
        else:
            # go deeper down the search tree

            # v_maximum_utility is used as an index to retrieve best move from choices
            # v_maximum_utility will never stay negative infinity since even if the loss
            # of the game is encountered, it is marked by -1000000 > float("-inf")
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
                # this portion of the code heavily relies on algorithm outlined on Figure 5.7 on pg. 170 of our
                # textbook. We are borrowing from the pseudocode and translating
                resulting_child_node = current_board_state.move(action)
                current_utility, move = self.Min_Value(resulting_child_node, alpha_, beta_, ply_counter + 1)
                # add utility and action pair to choices
                choices.update({current_utility: action})
                v_maximum_utility = max(v_maximum_utility, current_utility)

                if v_maximum_utility >= beta_:
                    return v_maximum_utility, action
                alpha_ = max(alpha_, v_maximum_utility)
            return v_maximum_utility, choices.get(v_maximum_utility)

    def Min_Value(self, current_board_state, alpha, beta, ply_counter):
        """This method returns the utility value of the best action from the Min player's point of view, the worst
        action from the Max player's point of view, and the action leading to that utility value

        current_board_state - the representation of the current configuration of the checkerboard
        alpha - the value of the best (i.e., highest-value) choice we have found so far at any choice point along the
        path for MAX.
        beta - the value of the best (i.e., lowest-value) choice we have found so far at any choice point along the
        path for MIN."""

        _alpha = alpha
        _beta = beta

        """just like in Max_Value this ply could be a terminal state, we can check that by using is_terminal() function 
        implemented in checkerboard.py. In case, the current ply is terminal we do not need to approximate utility by 
        using heuristic evaluation function, we can just return the utility of winning, losing, or a tie. """

        (game_over, winner) = current_board_state.is_terminal()
        if game_over:
            # return actual utility
            return self.Game_Over_Utility(winner), None
        elif self.Cut_Off_Test(ply_counter):
            # return approximation of the utility
            return self.strategy.utility(current_board_state), None
        else:
            # go deeper down the search tree

            # v_minimum_utility is used as an index to retrieve best move (for min)
            # from choices
            # v_minimum_utility will never positive infinity since even if the win
            # of the game is encountered, it is marked by 1000000 < float("inf")
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
            return v_minimum_utility, choices.get(v_minimum_utility)


class AI(abstractstrategy.Strategy):
    """AI is a checker playing strategy class using Minimax with alpha-beta pruning algorithm as a searching strategy
    to play checkers and heuristic evaluation function - utility function to evaluate current state of the
    checkerboard """

    def __init__(self, player, game, max_plies):
        # calls abstractstrategy.Strategy's constructor
        super(AI, self).__init__(player, game, max_plies)
        # instantiating a searching methodology class Minimax defined above
        self.searching_strategy = Minimax(self.maxplayer, self.minplayer, self.maxplies, self)

    def play(self, board):
        """"play - Make a move. Given a board, play returns (newboard, action) where newboard is the result of having
        applied action to board and action is determined via a game tree search (e.g. minimax with alpha-beta pruning).
        """
        print("Levan's AI player's alpha beta search In progress...")
        # find a best move using alpha-beta pruning
        best_move = self.searching_strategy.Alpha_Beta_Search(board)
        # if move exists, move
        new_board = board.move(best_move) if (best_move is not None) else board
        return new_board, best_move

    def utility(self, board):
        """utility is heuristic evaluation function (namely, a weighted linear function) - it
        approximates utility of the given checkerboard from the MAX player's viewpoint, in other words
        determines strength of the current checkerboard configuration relative to the MAX player.

        The following function computes several features known to be an important predictor
        of checkers game outcome. This analysis heavily relies on the article "Basic Strategies
        for Winning at Checkers" Written by Seth Brow available here:
        https://www.thesprucecrafts.com/how-to-win-at-checkers-411170  """

        # index of max player
        self.maxplayer_index = board.playeridx(self.maxplayer)

        # feature 1: Percentage difference of the amount of player's pawns and enemy's pawns
        # feature 2: Percentage difference of the amount of player's kings and enemy's kings
        pawn_p_difference, king_p_difference = self.Pawn_Perc_Diff(board)

        # feature 3: the difference between the amount of pieces on the home row for MAX player and the amount of
        # enemy pieces on the enemy home row
        relative_home_row_count = self.Home_Row_Pieces(board)

        # feature 4: how close are the pawns to becoming the king relative to enemy
        relative_getting_kinged = self.Distance_From_Kinged(board)

        # w_{i} is the weight for the ith feature weights here are simply chosen based on our intuition. Machine
        # learning would be the best way to determine these weights
        w_1, w_2, w_3, w_4 = 2, 3, 5, 5

        utility = int(
            w_1 * pawn_p_difference + w_2 * king_p_difference + w_3 * relative_home_row_count + w_4 * relative_getting_kinged)

        return utility if (utility is not None) else 0

    def Pawn_Perc_Diff(self, board):
        """Pawn_Diff returns Percentage difference of the amount of player's pawns and enemy's pawns and Percentage
        difference of the amount of player's kings and enemy's kings.

        Percentage difference here is calculated to equal the change in value, divided by the average of the 2
        numbers, all multiplied by 100. We retain + or - sign, since we want to evaluate from MAX player's point of
        view.

        The reasoning behind using percentage difference instead of the simple difference is to account for the fact
        that advantage of number of pieces is far more important when the total amount of pieces on the board is
        small. "With only 12 pieces on the board, to begin with, you may quickly end up with an 8-7 piece advantage.
        This may not seem like a big deal, but if you can trade four pieces, you suddenly have a 4-3 advantage,
        which is a tremendous amount of power." """

        # this does not need to be recomputed every time (just once in Utility function), it is recomputed here for
        # testing purposes only
        self.maxplayer_index = board.playeridx(self.maxplayer)

        board.recount_pieces()  # just to make sure pieces are correctly counted
        # the following lists contain number of pieces indexed by playerindex
        pawns = board.get_pawnsN()
        kings = board.get_kingsN()

        # player indices
        max_player_index = self.maxplayer_index
        min_player_index = (max_player_index + 1) % 2

        # number of pieces (pawns and king) for each player
        player_pawns = pawns[max_player_index]
        player_kings = kings[max_player_index]
        enemy_pawns = pawns[min_player_index]
        enemy_kings = kings[min_player_index]

        # calculations of Percentage difference for each piece type
        pawn_difference = int((player_pawns - enemy_pawns) / (
                (player_pawns + enemy_pawns) / 2.0) * 100) if player_pawns + enemy_pawns > 0 else 0
        king_difference = int((player_kings - enemy_kings) / (
                (player_kings + enemy_kings) / 2.0) * 100) if player_kings + enemy_kings > 0 else 0

        return pawn_difference, king_difference

    def Home_Row_Pieces(self, board):
        """Home_Row_Pieces return the difference between the amount of pieces on the home   row for maxplayer and
        enemy. Keeping pieces on the home row is a good strategy since it will prevent enemy from getting their
        pieces kinged.

        reasoning: "Your opponent cannot get any kinged checkers without advancing into one of your four home spaces.
        Keeping these spaces occupied guarantees that your opponent will get no kings until your checkers move.
        Generally speaking, you probably won't move these checkers until you are forced to capture an opposing piece,
        or if you are running low on checkers."

        board - current board state"""

        # this does not need to be recomputed every time (just once in Utility function), it is recomputed here for
        # testing purposes only
        self.maxplayer_index = board.playeridx(self.maxplayer)

        # figure out what is the legal direction for the max player
        direction = board.pawnmoves[self.maxplayer][0][0]
        # according to the direction, assign home and enemy's home rows accordingly
        home_row, enemy_home_row = (7, 0) if direction < 0 else (0, 7)

        home_row_piece_count = 0
        # traverse home row
        for c in range(board.coloffset[home_row], board.cols, board.step):
            # there is a piece and piece belongs to the MAX player, then increment count
            if board.board[home_row][c] and \
                    board.board[home_row][c] in board.players[self.maxplayer_index]:
                home_row_piece_count += 1

        enemy_home_piece_count = 0
        # traverse enemy home row
        for c in range(board.coloffset[enemy_home_row], board.cols, board.step):
            # there is a piece and piece belongs to the enemy, then increment count
            if board.board[enemy_home_row][c] and \
                    board.board[enemy_home_row][c] in board.players[(self.maxplayer_index + 1) % 2]:
                enemy_home_piece_count += 1

        return home_row_piece_count - enemy_home_piece_count

    def Distance_From_Kinged(self, board):
        """Distance_From_Kinged return the total distances of enemy's pawns from getting kinged (the bigger this
        number is the better for MAX player) minus the total distances of MAX player's pawns from getting kinged (the
        smaller this number is the better for the MAX player)

        reasoning: "A kinged piece is incredibly powerful, and generally speaking, the player who kings more checkers
        will win. While capturing opposing checkers is generally a good thing, your biggest concern should always be
        kinging your own checkers."

        board - current board state"""

        # this does not need to be recomputed every time (just once in Utility function), it is recomputed here for
        # testing purposes only
        self.maxplayer_index = board.playeridx(self.maxplayer)

        max_player_total = 0
        enemy_total = 0

        # for each existing piece on the board
        for (row, column, piece) in board:
            # figure out index of the owner of the pieces and whether piece is king or a pawn
            player_index, is_king = checkerboard.CheckerBoard.identifypiece(piece)
            # if piece is pawn
            if not is_king:
                # count distances using disttoking() method provided in checkerboard.py
                distance_to_kinged = board.disttoking(board.pawns[player_index], row)
                if player_index == self.maxplayer_index:
                    max_player_total += distance_to_kinged
                else:
                    enemy_total += distance_to_kinged
        return enemy_total - max_player_total















    # feature 5: difference between the amount of maxplayer and enemy pieces on the edge columns
    # relative_edge_count = self.Edge_Piece_Count(board)

    def Edge_Piece_Count(self, board):
        """Edge_Piece_Count returns the difference between the amount of maxplayer and enemy pieces on the edge
        columns.
        "For beginners, the first strategy one often figures out is to place your checkers on the edge of
        the board. This seems like a reasonable Checkers strategy because your pieces on the edge cannot be captured.
        But as it turns out, while this may be a tempting strategy in your first games, pushing your checkers to the
        edges is a mistake as it limits the moves you can make." """
        pieces_on_edge = 0
        # STOPPED HERE
        raise Exception("Not implemented yet")
