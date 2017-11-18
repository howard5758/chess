# Author: Ping-Jung Liu
# Date: October 5th 2017
# COSC 76 Assignment 3: CHESS
# Acknowledgement: Professor Devin Balkom for providing the general structure 
import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from ChessGame import ChessGame
import sys

class AlphaBetaAI():
	def __init__(self, depth, side):

		# For testing purpose, change to False to disable transposition table
		self.t = True
		# Number of move, to perform hardcoded openings
		self.moveNum = 0
		# 1 -> white, bottom side   0 -> black, top side
		self.side = side
		# max searh depth
		self.maxDepth = depth
		# current ids depth
		self.currentDepth = 1
		# winning utility
		self.winU = sys.maxsize
		# losing utility
		self.lossU = -sys.maxsize - 1
		self.nodes_visited = 1
		# initialize transposition table
		self.transp = {}


	def choose_move(self, board):

		# opening
		self.moveNum = self.moveNum + 1
		if self.moveNum == 1:
			if self.side == 1:
				return chess.Move.from_uci("b1c3")
			else:
				return chess.Move.from_uci("g8f6")
		elif self.moveNum == 2:
			if self.side == 1:
				return chess.Move.from_uci("g1f3")
			else:
				return chess.Move.from_uci("b8c6")
		elif self.moveNum == 3:
			if self.side == 1:
				return chess.Move.from_uci("e2e4")
			else:
				return chess.Move.from_uci("e7e5")


		# ids
		for i in range(0, self.maxDepth):
 
			self.currentDepth = i

			(move, util) = self.alphabeta_decision(board)

			if util == self.winU:
				return move
		
		print("Move Util:")
		print(util)
		print("Nodes Visited:")
		print(self.nodes_visited)

		self.nodes_visited = 1
		self.currentDepth = 1
		return move

	def alphabeta_decision(self, board):

		bestMove = 0
		bestUtil = self.lossU

		# initialize alpha and beta
		alpha = self.lossU
		beta = self.winU

		for move in list(board.legal_moves): 
			
			board.push(move)

			moveUtil = self.min_value(board, 1, alpha, beta)
			if moveUtil >= bestUtil:
				bestUtil = moveUtil
				bestMove = move
			# find better alpha each time
			alpha = max(bestUtil, alpha) 

			board.pop()
			 

		return (bestMove, bestUtil)

	# alpha and beta as new min max inputs
	def min_value(self, board, depth, alpha, beta):
	
		self.nodes_visited = self.nodes_visited + 1

		minUtil = self.winU

		# transposition case, will be discussed in the report
		if str(board) in self.transp and self.t:
			if self.transp[str(board)][1] > self.currentDepth:
				util = self.transp[str(board)][0]

				if self.transp[str(board)][2] == "EXACT":
					return util
				elif self.transp[str(board)][2] == "LOW" and util <= alpha:
					return util
				elif self.transp[str(board)][2] == "UP" and util >= beta:
					return util

		# cutoff situation
		if self.cutoff(board, depth):

			util = self.get_utility(board)

			# again, will be further discussed in the report
			if self.t:
				if util <= alpha:
					self.transp[str(board)] = (util, depth, "LOW")
				elif util >= beta:
					self.transp[str(board)] = (util, depth, "UP")
				else:
					self.transp[str(board)] = (util, depth, "EXACT")

			return util

		# reorder the move list for better alphabeta 	
		new_list = self.reorder(board)
		new_list.reverse()
		for move in new_list:
		#list(board.legal_moves):

			board.push(move)
			minUtil = min(minUtil, self.max_value(board, depth + 1, alpha, beta))
			board.pop()

			# pruning
			if minUtil <= alpha:
				return minUtil
			# modify beta
			beta = min(minUtil, beta)


		return minUtil



	def max_value(self, board, depth, alpha, beta):
	
		self.nodes_visited = self.nodes_visited + 1

		maxUtil = self.lossU

		# transposition table
		if str(board) in self.transp and self.t:
			if self.transp[str(board)][1] > self.currentDepth:
				util = self.transp[str(board)][0]

				if self.transp[str(board)][2] == "EXACT":
					return util
				elif self.transp[str(board)][2] == "LOW" and util <= alpha:
					return util
				elif self.transp[str(board)][2] == "UP" and util >= beta:
					return util

		# cutoff situation
		if self.cutoff(board, depth):

			util = self.get_utility(board)

			if self.t:
				if util <= alpha:
					self.transp[str(board)] = (util, depth, "LOW")
				elif util >= beta:
					self.transp[str(board)] = (util, depth, "UP")
				else:
					self.transp[str(board)] = (util, depth, "EXACT")

			return self.get_utility(board)

		# reoreder move list for alphabeta
		new_list = self.reorder(board)
		for move in new_list:
		#list(board.legal_moves):

			board.push(move)
			maxUtil = max(maxUtil, self.min_value(board, depth + 1, alpha, beta))
			board.pop()

			# pruning
			if maxUtil >= beta:
				return maxUtil
			# modify alpha
			alpha = max(maxUtil, alpha)


		return maxUtil

	# given self, and board, sort the utilities of legal_moves
	def reorder(self, board):

		move_list = list(board.legal_moves)
		temp = []

		# loop through the list
		for move in move_list:

			board.push(move)
			# if visited, get the utility from transposition table
			if str(board) in self.transp:
				temp.append((self.transp[str(board)][0], move))
			# if not visited, calculate utility
			else:
				temp.append((self.get_utility(board), move))

			board.pop()

		# sort the the list based on utilities
		temp = sorted(temp, key=lambda util: util[0])
		# reverse it so it begins with the largest utility
		temp.reverse()
		
		# obtain a list of moves for convenience
		move_list = []
		for i in range(0, len(temp)):
			move_list.append(temp[i][1])
		return move_list
		
	# same utility function as minimax
	def get_utility(self, board):

		turn = int(board.turn)
		u = 0

		if board.is_game_over():
			if board.is_checkmate():
				if self.side == turn :
					return self.lossU
				else:
					return self.winU
			else:
				return 0
		else:
			for i in range(1, 7):
				u = u + i * len(board.pieces(i, self.side))
				u = u - 0.5 * i * len(board.pieces(i, (self.side + 1) % 2))
		
		return u

	def cutoff(self, board, depth):
		return depth > self.currentDepth or board.is_game_over()









