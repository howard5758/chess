# Author: Ping-Jung Liu
# Date: October 5th 2017
# COSC 76 Assignment 3: CHESS
# Acknowledgement: Professor Devin Balkom for providing the general structure 

###README###

Files in this directory:

- chess.pdf

- chess.md

- ChessGame.py

- RandomAI.py

- HumanPlayer.py

- MinimaxAI.py

- AlphaBetaAI.py

- test_chess.py

- gui_chess.py

I suggest not using gui_chess.py because it cannot work with human players, 
and there will be error when the game ends.

Of course feel free to run it and see two AI fight each other. 
######################################################
To play with Friend!
######################################################

- Open test_chess.py

- change both players to = HumanPlayer()

- run test_chess.py

- if one wants to move from a3 to b4, typle a3b4 as move command

######################################################
To play with AI!
######################################################

- Open test_chess.py

- pick a player and change it to = HumanPlayer()

- Change the other to one of the AI players:
  RandomAI(), MinimaxAI(), AlphaBetaAI()
  Please note that when setting up minimax and alphabeta,
  enter the search depth and its side as input parameters.

  A black minimaxAI with search depth 3 would be:
  MinimaxAI(3, 0)

  A white alphabetaAI with search depth 4 would be:
  AlphaBetaAI(4, 1)

- run test_chess.py

#######################################################
To watch AI fight each other!
#######################################################

- Change both players to AI players following the 
  same instructions as above

- run test_chess.py
