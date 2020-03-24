'''
@author: mroch
'''

# Game representation and mechanics
import checkerboard

# tonto - Professor Roch's not too smart strategy
# You are not given source code to this, but compiled .pyc files
# are available for Python 3.7 and 3.8 (fails otherwise).
# This will let you test some of your game logic without having to worry
# about whether or not your AI is working and let you pit your player
# against another computer player.
#
# Decompilation is cheating, don't do it.  Big sister is watching you :-)

# Python cand load compiled modules using the imp module (deprecated)
# We'll format the path to the tonto module based on the
# release of Python.  Note that we provided tonto compilations for Python 3.7
# and 3.8.  If you're not using one of these, it won't work.
import imp
import sys
import ai
major = sys.version_info[0]
minor = sys.version_info[1]
modpath = "__pycache__/tonto.cpython-{}{}.pyc".format(major, minor)
tonto = imp.load_compiled("tonto", modpath)


# human - human player, prompts for input    
import human

import boardlibrary # might be useful for debugging

from timer import Timer
        

def Game(red=human.Strategy, black=tonto.Strategy, 
         maxplies=10, init=None, verbose=True, firstmove=0):
    """Game(red, black, maxplies, init, verbose, turn)
    Start a game of checkers
    red,black - Strategy classes (not instances)
    maxplies - # of turns to explore (default 10)
    init - Start with given board (default None uses a brand new game)
    verbose - Show messages (default True)
    firstmove - Player N starts 0 (red) or 1 (black).  Default 0. 
    """
    my_board = checkerboard.CheckerBoard() if (init is None) else init

    print("Initial state of the board:")
    print(my_board)

    red_player = red('r', checkerboard.CheckerBoard, maxplies)
    print(black)
    black_player = black.Strategy('b', checkerboard.CheckerBoard, maxplies)

    players = (red_player, black_player)
    i = 1
    game_over = False
    winner = None
    print("Game begins now!")
    current_board = my_board
    while not game_over:
        i += 1
        new_board, best_move = players[i % 2].play(current_board)
        print(new_board)
        print(best_move)
        (game_over, winner) = new_board.is_terminal()
        current_board = new_board

    # Output statement for the winner declarations
    if winner in ['r', 'R']:
        print("The winner is RED player")
    elif winner in ['b', 'B']:
        print("The winner is BLACK player")
    else:
        print("The game ended in a draw")
    
            
if __name__ == "__main__":
    #Game(init=boardlibrary.boards["multihop"])
    #Game(init=boardlibrary.boards["StrategyTest1"])
    #Game(init=boardlibrary.boards["EndGame1"], firstmove = 1)
    Game(ai.AI, tonto, 10)