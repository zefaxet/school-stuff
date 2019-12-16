##############################################################################################################
# Name: Edward Auttonberry
# CWID: 102-48-286
# Date: 11/12/2018
# Assignment 3
# An implementation of the board game Othello designed for use with a mini-max algorithm acting as an opponent
##############################################################################################################

from logging import getLogger, INFO, ERROR
from math import inf
from numpy import array, intc
from copy import deepcopy


# Utility constants
MANUAL = False
PLAYERS = ["BLACK", "WHITE"]
MAP = {
	'A': 0,
	'B': 1,
	'C': 2,
	'D': 3,
	'E': 4,
	'F': 5,
	'G': 6,
	'H': 7,
	0: 'A',
	1: 'B',
	2: 'C',
	3: 'D',
	4: 'E',
	5: 'F',
	6: 'G',
	7: 'H',
}
COLORS = {  # ansi escape codes - these are not compatible with the windows command line
	'CLEAR': '\u001b[0m',
	'WHITE': '\u001b[47m\u001b[37;1m',
	'GRAY': '\u001b[48;5;8m\u001b[38;5;235m',
	'BLUE': '\033[94m'
}


# utility method for converting between ordered pairs for the board and string coordinate pairs such as A1 to [0, 0]
def pair_flip(pair):
	
	if type(pair) is str:
		return [int(pair[1]) - 1, MAP[pair[0]]]
	elif type(pair) is list:
		return MAP[pair[1]] + str(pair[0] + 1)


# Mini-max specific constants
MINI_MAX_PLY = 5
CORNER_CONST = 20
DEBUG = False
PRUNE = False


# This method encapsulates the entirety of the mini-max algorithm and alpha-beta pruning implementations
# They are implemented recursively, such that all information is passed around through method parameters
# The method is only called once outside of itself, and is done so without any values defined for alpha and beta
# 	because they are initialized to infinite extremes
# game_state is a game object containing the state of the board
# player is constant boolean value that the algorithm uses to determine which player it is
# dig is how much deeper the algorithm should search. The initial method call uses the ply constant as value for this
# 	parameter
# alpha and beta are the values used for pruning. They both default to their respective extrema, and are not specified
# 	in the initial method call
def mini_max(game_state, player, dig, alpha=-inf, beta=inf):

	# Static variables used for displaying program statistics later
	global checked_states
	global prunings

	checked_states += 1
	# hp is what will be returned. The heuristic value is recorded with it's associated move so that the best move comes
	# 	out at the top of the tree
	hp = [None, -inf if game_state.player == player else inf]

	# checks to see if we have reached our ply depth
	if not dig:
		# the fundamental heuristic is the difference between the number of the AI's pieces and the human's pieces
		# 	where the AI's pieces are weighed positively
		scores = game_state.count_pieces()
		score_sum = scores[player] - scores[not player]
		# this was done in an attempt to stress the value of the end game and suggest objective-based gameplay
		# it may not have any effect, however
		if game_state.end:
			if score_sum >= 0:
				hp[1] = inf
			else:
				hp[1] = -inf
		else:
			# This stresses the value of corner pieces, which are strategically the most valuable spaces
			if pair_flip(game_state.plays[-1]) in ["A1", "A8", "H1", "H8"]:
				score_sum += CORNER_CONST if game_state.player == player else -CORNER_CONST
			hp[1] = score_sum

		if DEBUG:
			print("Game state has reached max ply. h' = {}".format(hp[1]))
		return hp, alpha, beta
	if DEBUG:
		print("######### {} ON LAYER {} #########".format("MAXIMIZING" if game_state.player == player else "MINIMIZING",
																									MINI_MAX_PLY - dig))

		print("ALPHA CUTOFF:", alpha, "| BETA CUTOFF:", beta)

	# Every ply except the deepest comes here. This for loop is where the algorithm begins to search through each move
	# 	at a given level
	for move in game_state.moves:
		if DEBUG:
			print("Expanding into move {} for player {}.".format(move, PLAYERS[game_state.player]))
		# this is the recursive call
		result, alpha, beta = mini_max(game_state.play(move), player, dig - 1, alpha, beta)
		if DEBUG:
			print("Calculated heuristic for move {}: {}".format(move, result[1]))
		# record the move that was made
		result[0] = move

		# maximizing node
		if game_state.player == player and result[1] >= hp[1]:
			if DEBUG:
				print("Move {} has the current maximum heuristic, {} versus {}, for ply depth {}. Propagating..."
																			.format(result[0], result[1], hp[1],
																								MINI_MAX_PLY - dig))
			hp = result

			# check for possibility of pruning
			if result[1] > beta and PRUNE:
				if DEBUG:
					print("Child of maximizing node with move {}".format(result[0]) +
							" contains heuristic value {} which is greater than ".format(result[1]) +
							"the node's beta value {}. Pruning remaining children...".format(beta))
				prunings += 1
				break

		# minimizing node
		elif not game_state.player == player and result[1] <= hp[1]:
			if DEBUG:
				print("Move {} has the current minimum heuristic, {} versus {}, for ply depth {}. Propagating..."
																					.format(result[0], result[1], hp[1],
																									MINI_MAX_PLY - dig))
			hp = result

			# check for possibility of pruning
			if result[1] < alpha and PRUNE:
				if DEBUG:
					print("Child of minimizing node with move {}".format(result[0]) +
							" contains heuristic value {} which is less than ".format(result[1]) +
							"the node's alpha value {}. Pruning remaining children...".format(alpha))
				prunings += 1
				break

	else:  # no pruning was done so update either alpha or beta
		if game_state.player == player:
			beta = hp[1]
			if DEBUG:
				print("BETA:", beta)
		else:
			alpha = hp[1]
			if DEBUG:
				print("ALPHA:", alpha)

	if DEBUG:
		print("BEST MOVE FOR LAYER {}:".format(MINI_MAX_PLY - dig), hp)
		print("########## END LAYER {} ##########".format(MINI_MAX_PLY - dig))

	# return the heuristic of this node along with the associated best move and the alpha and beta values of this node
	# if this is the root node, just return the move string to play with
	return hp[0] if dig == MINI_MAX_PLY else (hp, alpha, beta)


# this class represents the board at a particular point in play
# it does NOT represent the game from start to finish, but rather a specific turn in the course of the game
class Game:

	# this is called only in the case of a new game
	def __init__(self):

		self.player = False  # False is black
		self.end = False  # Game runs while false
		self.board = array([[-1 for x in range(0, 8)] for y in range(0, 8)], intc)  # empty board, no pieces down
		self.board[3, 4], self.board[4, 3] = 0, 0  # Set starting blacks
		self.board[3, 3], self.board[4, 4] = 1, 1  # Set starting whites
		self.plays = [[3, 3], [3, 4], [4, 3], [4, 4]]  # register the set tokens
		self.moves = {}
		self.gen_moves()  # generate the opening set of moves

	#  This just returns an ascii visualization of the state of the board at the current turn
	def __str__(self):

		string = "  A B C D E F G H"

		for y in range(0, 8):

			string = string + "\n{} ".format(y+1)

			for x in range(0, 8):

				slot = self.board[y, x]
				if pair_flip([y, x]) in self.moves.keys():  # shows valid moves
					token = "."
				elif slot == -1:  	# empty space, no move
					token = " "
				elif slot == 0:  	# black token
					token = "B"
				else:				# white token
					token = "W"

				string += token + " "

		return string

	# returns the counts of the black and white pieces on the board in a 2-element list
	def count_pieces(self):
		
		pieces = [0, 0]
		for row in self.board:
			for space in row:
				if space == -1:
					continue
				elif space == 0:
					pieces[0] += 1
				elif space == 1:
					pieces[1] += 1
		
		return pieces
		
	# this method takes in a string representation of a move, e.g. A1, and attempts to play it
	# invalid moves, and any junk, will not be considered, and the game will not update
	# in the case of a valid move, the move and all consequences are applied
	# this method returns a deep copied instance of this class wherein the update is canon
	def play(self, pair):

		if pair in self.moves:
			new = deepcopy(self)
			coords = pair_flip(pair)  # need to convert the string coords into an ordered pair
			new.board[coords[0], coords[1]] = self.player  # place the token
			new.plays.append(coords)  # register the move in game history
			for token in new.moves[pair]:  # flip all of the affected pieces
				new.board[token[0], token[1]] = int(new.player)
			new.player = not self.player  # next player's turn
			new.gen_moves()  # generate new moves
			if not len(new.moves):  # check if player can make moves, and end game if no moves can be made by either player
				new.player = not new.player
				new.gen_moves()
				if not len(new.moves):
					new.end = True
			return new
		else:
			print("Invalid move:", pair)
			
	# Starts at all existing pieces for this player, and searches in any direction for that piece as long as the piece
	# 	is the opposite player's piece, and terminates when it sees a -1, the edge of the board, or another piece
	# 	belonging to the current player
	# The valid moves found by this method are used as keys to a list of affected pieces should that move be made
	def gen_moves(self):
	
		self.moves = {}
		for move in self.plays:
			if self.board[move[0], move[1]] == self.player:  # start at existing tokens owned by current player
				for shift in [[1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1]]:  # go around in a square
					candidate_y = move[0] + shift[0]  # |
					candidate_x = move[1] + shift[1]  # go in a straight line until an end is reached
					if candidate_x in range(0, 8) and candidate_y in range(0, 8)\
						and self.board[candidate_y, candidate_x] == (not self.player):
						path = []
						while candidate_y in range(0, 8) and candidate_x in range(0, 8):
							token = self.board[candidate_y, candidate_x]
							if token == self.player:  # end if another token owned by current player is found
								break
							elif token == -1:  # end if no more whites and empty space is found, indicating valid move
								move_string = MAP[candidate_x] + str(candidate_y + 1)
								try:
									self.moves[move_string] += path
								except KeyError:
									self.moves[move_string] = path
								break
							path.append([candidate_y, candidate_x])
							candidate_y += shift[0]
							candidate_x += shift[1]


# This method simply shows the board and important game details
def show_board(turn_num, game):
	#print(chr(27)+"[2J")
	print("TURN:", turn_num)
	print("\nTurn for player " + PLAYERS[game.player])
	print(game)


""" MAIN """


#  Player is either 0 or 1
human = min(max(int(input("Which player is the human? 1 is Black and 2 is White.\n")), 1), 2) - 1
game = Game()
turn_number = 1
show_board(turn_number, game)

# game loop
while 1:

	turn_number += 1
	if game.end:
		print("Game Over")
		
		score = game.count_pieces()
		
		print("Number of BLACK tokens:", score[0])
		print("Number of WHITE tokens:", score[1])
		# determine winner
		if score[0] == score[1]:
			print("Its a tie!")
		else:
			print("The winner is {}!".format("BLACK" if score[0] > score[1] else "WHITE"))

		print("Transcript:")
		transcript = ""
		for play in game.plays:
			transcript += pair_flip(play)
		print(transcript)  # this is the chronological order of moves made for this game

		break
	elif False and (game.player == human or MANUAL):  # take human input if human's turn of it manual control is on
		while 1:
			play = input("Enter move (ex 'A1'): ").capitalize()  # make move
			if "Debug" in play:  # toggle debug command
				DEBUG = not DEBUG * 2
				print("DEBUG mode", "ON" if DEBUG else "OFF")
				continue
			elif "Prune" in play:  # toggle alpha-beta pruning command
				PRUNE = not PRUNE
				print("Alpha-Beta pruning is now", "ON" if PRUNE else "OFF")
				continue
			turn = game.play(play)  # apply move to game
			if turn:  # show new board
				game = turn
				show_board(turn_number, game)
				break
	else:  # AI takes over
		checked_states = 0
		prunings = 0
		print("Searching for optimal move...")
		decision = mini_max(game, not human, MINI_MAX_PLY)  # begin search for move
		game = game.play(decision)  # play move
		if DEBUG:
			input()
		show_board(turn_number, game)
		print("Decision:", decision)
		print("Number of checked states:", checked_states)
		if PRUNE:
			print("Number of pruned states:", prunings)

exit(1)
