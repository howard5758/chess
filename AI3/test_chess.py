# pip3 install python-chess


import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from ChessGame import ChessGame
import sys


player1 = HumanPlayer()
player2 = MinimaxAI(3, 0)

game = ChessGame(player1, player2)


#print(str(game.board))
#print(game)
#print(player2.get_utility(game.board))


print(int(game.board.turn))

while not game.is_game_over():                    
    print(game)
    game.make_move()
print(game)


