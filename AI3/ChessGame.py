# Author: Professor Devin Balkom
# Modified By: Ping-Jung Liu
# Date: October 5th 2017
# COSC 76 Assignment 3: CHESS
# Acknowledgement: Professor Devin Balkom for providing the general structure 
import chess


class ChessGame:
    def __init__(self, player1, player2):
        self.board = chess.Board()
        self.players = [player1, player2]

    def make_move(self):

        player = self.players[1 - int(self.board.turn)]
        move = player.choose_move(self.board)
        print("Move:")
        print(move)
        self.board.push(move)  # Make the move

    def is_game_over(self):
        return self.board.is_game_over()

    def __str__(self):

        column_labels = "\n----------------\na b c d e f g h\n"
        board_str =  str(self.board) + column_labels

        # did you know python had a ternary conditional operator?
        if self.is_game_over():
            if self.board.can_claim_draw():
                move_str = "DRAW!"
            else:
                move_str = "Black Won" if self.board.turn else "White Won"
        else:
            move_str = "White to move" if self.board.turn else "Black to move"

        return board_str + "\n" + move_str + "\n"


