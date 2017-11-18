# Author: Ping-Jung Liu
# Date: October 5th 2017
# COSC 76 Assignment 3: CHESS
# Acknowledgement: Professor Devin Balkom for providing the general structure 
import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from ChessGame import ChessGame
import sys

class MinimaxAI():
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
		# perform openings
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
		
			(move, util) = self.minimax_decision(board)

			# if encounter winning utility, return
			if util == self.winU:
				print(util)
				return move

		print("Move Util:")
		print(util)
		print("Nodes Visited")
		print(self.nodes_visited)

		self.nodes_visited = 1
		self.currentDepth = 1
		return move

	def minimax_decision(self, board):

		# 0 as space holder
		bestMove = 0
		# set the best utility to loss utility for future comparison
		bestUtil = self.lossU

		# loop through all legal moves
		for move in list(board.legal_moves):

			board.push(move)

			# find the best move in min nodes
			moveUtil = self.min_value(board, 1)
			if moveUtil >= bestUtil:
				bestUtil = moveUtil
				bestMove = move

			board.pop()

		return (bestMove, bestUtil)

	def min_value(self, board, depth):
		# increment nodes visited
		self.nodes_visited = self.nodes_visited + 1
		# set minimum utility to winning utility for future comparison 
		minUtil = self.winU

		# will be further discussed in the report
		if str(board) in self.transp and self.t:
			if self.transp[str(board)][1] > self.currentDepth:
				return self.transp[str(board)][0]

		# cutoff situation
		if self.cutoff(board, depth):
			util = self.get_utility(board)
			# modify transposition table
			if self.t and (not str(board) in self.transp or depth > self.transp[str(board)][1]):
				self.transp[str(board)] = (util, depth)

			return util
		# loop through max nodes to find minimum
		for move in list(board.legal_moves):

			board.push(move)
			minUtil = min(minUtil, self.max_value(board, depth + 1))
			board.pop()

		return minUtil



	def max_value(self, board, depth):
	
		self.nodes_visited = self.nodes_visited + 1
		
		maxUtil = self.lossU

		if str(board) in self.transp and self.t:
			if self.transp[str(board)][1] > self.currentDepth:
				return self.transp[str(board)][0]

		if self.cutoff(board, depth):
			util = self.get_utility(board)
			# modify transposition table
			if self.t and (not str(board) in self.transp or depth > self.transp[str(board)][1]):
				self.transp[str(board)] = (util, depth)

			return util

		for move in list(board.legal_moves):

			board.push(move)
			maxUtil = max(maxUtil, self.min_value(board, depth + 1))
			board.pop()

		return maxUtil

	# my utility function, will be further discussed in the report
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
				# board.pieces return the positions of a piece of one player
				u = u + i * len(board.pieces(i, self.side))
				u = u - 0.5 * i * len(board.pieces(i, (self.side + 1) % 2))
		#print(u)
		return u

	# cutoff if exceed search depth, or game over
	def cutoff(self, board, depth):
		return depth > self.currentDepth or board.is_game_over()








