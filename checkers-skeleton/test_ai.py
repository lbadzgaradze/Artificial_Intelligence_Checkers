import unittest
import ai
import boardlibrary
import checkerboard


class TestAI(unittest.TestCase):

    def setUp(self):
        boardlibrary.init_boards()
        self.Pristine = boardlibrary.boards["Pristine"]
        # initial board
        self.SingleHopsRed = boardlibrary.boards["SingleHopsRed"]
        # Set up for two red single hops
        #           0  1  2  3  4  5  6  7
        #        0  .  b  .  b  .  b  .  b
        #        1  b  .  b  .  b  .  b  .
        #        2  .  b  .  .  .  .  .  b
        #        3  .  .  .  .  .  .  b  .
        #        4  .  .  .  b  .  .  .  r
        #        5  r  .  r  .  r  .  .  .
        #        6  .  r  .  r  .  r  .  r
        #        7  r  .  r  .  r  .  r  .
        self.SingleHopsBlack = boardlibrary.boards["SingleHopsBlack"]
        # Set up for black single hops
        #     0  1  2  3  4  5  6  7
        #  0  .  b  .  b  .  b  .  b
        #  1  b  .  b  .  b  .  b  .
        #  2  .  b  .  .  .  .  .  b
        #  3  .  .  .  .  .  .  r  .
        #  4  .  .  .  b  .  .  .  r
        #  5  r  .  r  .  r  .  .  .
        #  6  .  .  .  r  .  r  .  r
        #  7  r  .  r  .  r  .  r  .
        self.multihop = boardlibrary.boards["multihop"]
        # multihop
        #     0  1  2  3  4  5  6  7
        #  0  .  b  .  b  .  b  .  b
        #  1  b  .  r  .  b  .  .  .
        #  2  .  r  .  .  .  b  .  b
        #  3  .  .  .  .  .  .  .  .
        #  4  .  .  .  r  .  b  .  .
        #  5  .  .  .  .  .  .  r  .
        #  6  .  r  .  r  .  r  .  r
        #  7  r  .  .  .  r  .  .  .
        self.KingBlack = boardlibrary.boards["KingBlack"]
        # KingBlack
        # Black can move to become a King but should
        # not be able to move after being kinged
        #    0  1  2  3  4  5  6  7
        #    0  .  .  .  .  .  .  .  .
        #    1  .  .  .  .  .  .  .  .
        #    2  .  .  .  .  .  .  .  .
        #    3  .  .  .  .  b  .  .  .
        #    4  .  .  .  r  .  r  .  .
        #    5  .  .  .  .  .  .  .  .
        #    6  .  .  .  r  .  r  .  .
        #    7  .  .  .  .  .  .  .  .
        self.BlackKingTour = boardlibrary.boards["BlackKingTour"]
        # BlackKingTour
        #    0  1  2  3  4  5  6  7
        #    0  .  .  .  .  .  .  .  .
        #    1  .  .  .  .  .  .  .  .
        #    2  .  .  .  .  .  .  .  .
        #    3  .  .  .  .  B  .  .  .
        #    4  .  .  .  r  .  r  .  .
        #    5  .  .  .  .  .  .  .  .
        #    6  .  .  .  r  .  r  .  .
        #    7  .  .  .  .  .  .  .  .
        self.RedKingTour = boardlibrary.boards["RedKingTour"]
        # RedKingTour
        # Probably don't need to test this one as rules similar, but...
        #    0  1  2  3  4  5  6  7
        #    0  .  .  .  .  .  .  .  .
        #    1  .  .  .  .  .  .  .  .
        #    2  .  .  .  .  .  .  .  .
        #    3  .  .  .  .  R  .  .  .
        #    4  .  .  .  b  .  b  .  .
        #    5  .  .  .  .  .  .  .  .
        #    6  .  .  .  b  .  b  .  .
        #    7  .  .  .  .  .  .  .  .
        self.StrategyTest1 = boardlibrary.boards["StrategyTest1"]
        # ???
        self.EndGame1 = boardlibrary.boards["EndGame1"]
        # EndGame 1 - Red can easily win
        #       0  1  2  3  4  5  6  7
        #    0     .     .     R     b
        #    1  .     .     .     .
        #    2     .     .     .     .
        #    3  .     .     .     .
        #    4     .     .     .     .
        #    5  .     .     .     .
        #    6     .     .     .     R
        #    7  .     .     .     .

        self.my_checkerboard = checkerboard.CheckerBoard()
        self.my_ai_red = ai.AI('r', self.my_checkerboard, 10)
        self.my_ai_black = ai.AI('b', self.my_checkerboard, 10)

    def tearDown(self):
        pass

    def test_pawn_perc_diff(self):
        # Pristine and SingleHopsRed
        for board in [self.Pristine, self.SingleHopsRed]:
            pawn_difference_red, king_difference_red = self.my_ai_red.Pawn_Perc_Diff(board)
            pawn_difference_black, king_difference_black = self.my_ai_black.Pawn_Perc_Diff(board)
            pawn_difference_red_expected, king_difference_red_expected = 0, 0

            self.assert_lines(pawn_difference_red, pawn_difference_black,
                              king_difference_red, king_difference_black,
                              pawn_difference_red_expected, king_difference_red_expected)

        # SingleHopsBlack
        pawn_difference_red, king_difference_red = self.my_ai_red.Pawn_Perc_Diff(self.SingleHopsBlack)
        pawn_difference_black, king_difference_black = self.my_ai_black.Pawn_Perc_Diff(self.SingleHopsBlack)
        pawn_difference_red_expected, king_difference_red_expected = 8, 0

        self.assert_lines(pawn_difference_red, pawn_difference_black,
                          king_difference_red, king_difference_black,
                          pawn_difference_red_expected, king_difference_red_expected)

        # multihop
        pawn_difference_red, king_difference_red = self.my_ai_red.Pawn_Perc_Diff(self.multihop)
        pawn_difference_black, king_difference_black = self.my_ai_black.Pawn_Perc_Diff(self.multihop)
        pawn_difference_red_expected, king_difference_red_expected = 10, 0

        self.assert_lines(pawn_difference_red, pawn_difference_black,
                          king_difference_red, king_difference_black,
                          pawn_difference_red_expected, king_difference_red_expected)

        # KingBlack
        pawn_difference_red, king_difference_red = self.my_ai_red.Pawn_Perc_Diff(self.KingBlack)
        pawn_difference_black, king_difference_black = self.my_ai_black.Pawn_Perc_Diff(self.KingBlack)
        pawn_difference_red_expected, king_difference_red_expected = 120, 0

        self.assert_lines(pawn_difference_red, pawn_difference_black,
                          king_difference_red, king_difference_black,
                          pawn_difference_red_expected, king_difference_red_expected)

        # BlackKingTour
        pawn_difference_red, king_difference_red = self.my_ai_red.Pawn_Perc_Diff(self.BlackKingTour)
        pawn_difference_black, king_difference_black = self.my_ai_black.Pawn_Perc_Diff(self.BlackKingTour)
        pawn_difference_red_expected, king_difference_red_expected = 200, -200

        self.assert_lines(pawn_difference_red, pawn_difference_black,
                          king_difference_red, king_difference_black,
                          pawn_difference_red_expected, king_difference_red_expected)

        # RedKingTour
        pawn_difference_red, king_difference_red = self.my_ai_red.Pawn_Perc_Diff(self.RedKingTour)
        pawn_difference_black, king_difference_black = self.my_ai_black.Pawn_Perc_Diff(self.RedKingTour)
        pawn_difference_red_expected, king_difference_red_expected = -200, 200

        self.assert_lines(pawn_difference_red, pawn_difference_black,
                          king_difference_red, king_difference_black,
                          pawn_difference_red_expected, king_difference_red_expected)

        # EndGame1
        pawn_difference_red, king_difference_red = self.my_ai_red.Pawn_Perc_Diff(self.EndGame1)
        pawn_difference_black, king_difference_black = self.my_ai_black.Pawn_Perc_Diff(self.EndGame1)
        pawn_difference_red_expected, king_difference_red_expected = -200, 200

        self.assert_lines(pawn_difference_red, pawn_difference_black,
                          king_difference_red, king_difference_black,
                          pawn_difference_red_expected, king_difference_red_expected)

    def assert_lines(self, red_pawn, black_pawn, red_king, black_king, red_pawn_expected, red_king_expected):
        # print(red_pawn, black_pawn, red_king, black_king, red_pawn_expected, red_king_expected)
        self.assertEqual(red_pawn, red_pawn_expected)
        self.assertEqual(red_king, red_king_expected)
        self.assertEqual(black_pawn, -red_pawn_expected)
        self.assertEqual(black_king, -red_king_expected)

    def test_home_row_pieaces(self):
        for board in [self.Pristine, self.SingleHopsRed, self.SingleHopsBlack, self.KingBlack, self.BlackKingTour, self.RedKingTour]:
            difference_red = self.my_ai_red.Home_Row_Pieces(board)
            difference_black = self.my_ai_black.Home_Row_Pieces(board)
            expected_red = 0
            self.assertEqual(difference_red, expected_red)
            self.assertEqual(difference_black, -expected_red)

        # multihop
        difference_red = self.my_ai_red.Home_Row_Pieces(self.multihop)
        difference_black = self.my_ai_black.Home_Row_Pieces(self.multihop)
        expected_red = -2
        self.assertEqual(difference_red, expected_red)
        self.assertEqual(difference_black, -expected_red)

        # EndGame1
        difference_red = self.my_ai_red.Home_Row_Pieces(self.EndGame1)
        difference_black = self.my_ai_black.Home_Row_Pieces(self.EndGame1)
        expected_red = -1
        self.assertEqual(difference_red, expected_red)
        self.assertEqual(difference_black, -expected_red)



if __name__ == '__main__':
    unittest.main()
