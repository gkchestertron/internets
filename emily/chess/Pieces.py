from copy import copy

class Piece(object):
	def __init__(self, color, spot, board): 
		self.color = color
		self.spot = spot
		self.board = board
		self.first_move = True 

		if self.color == 'white':
			self.char = self.white
			self.reverse_char = self.black
		else:
			self.char = self.black
			self.reverse_char = self.white

	def __unicode__(self):
		return self.char

	def move(self, next_spot):
		if self.valid_move(next_spot):
			piece = self.board.grid[next_spot[0]][next_spot[1]]
			if isinstance(piece, Piece):
				piece.spot = None
			self.board.grid[self.spot[0]][self.spot[1]] = ' ' # 0 = row, 1 = col
			self.spot = next_spot
			self.board.grid[self.spot[0]][self.spot[1]] = self
			self.first_move = False

	def valid_move(self, next_spot):
		if next_spot in self.possible_moves():
			return True
		else:
			return False

	def get_spot(self, diff):
		if self.color == 'black':
			diff[0] *= -1
		new_row = diff[0] + self.spot[0]
		new_col = diff[1] + self.spot[1]

		return [new_row, new_col]

	def check_spot(self, spot, check_king=True):
		if self.board.in_bounds(spot):
			if check_king and self.king_is_in_check(spot):
				return False
			if self.board.spot_empty(spot):
				return True# poss.append(spot)
			other_piece = self.board.grid[spot[0]][spot[1]]
			if isinstance(other_piece, Piece) and other_piece.color != self.color:
				return True# poss.append(spot)
		return False

	def test_move(self, spot, function):
		if not self.board.in_bounds(spot):
			return False
		original_spot = copy(self.spot)
		test_spot = self.board.grid[spot[0]][spot[1]]

		self.board.grid[self.spot[0]][self.spot[1]] = ' ' # 0 = row, 1 = col
		self.spot = spot
		self.board.grid[self.spot[0]][self.spot[1]] = self

		result = function(spot)

		self.board.grid[self.spot[0]][self.spot[1]] = test_spot # 0 = row, 1 = col
		self.spot = original_spot
		self.board.grid[self.spot[0]][self.spot[1]] = self

		return result

	def king_is_in_check(self, spot):
		return self.test_move(spot, self.king_is_in_check_helper)

	def king_is_in_check_helper(self, spot):
		king = self.get_king()
		if not king:
			return False
		return king.is_in_check(king.spot)


	def get_king(self):
		king_list = filter(lambda x: isinstance(x, King) and x.color == self.color, self.board.flatten())
		if len(king_list) == 0:
			return False
		return king_list[0]

	def possible_moves(self, check_king=True):
		return self.get_sliding_moves(check_king=check_king)

	def get_sliding_moves(self, check_king=True):
		poss = []
		for diff in self.dir_diffs:
			spot = self.get_spot(diff)
			new_diff = copy(diff)
			while self.check_spot(spot, check_king=check_king):
				poss.append(spot)
				if self.board.in_bounds(spot) and not self.board.spot_empty(spot):
					break
				new_diff[0] += diff[0]
				new_diff[1] += diff[1]
				spot = self.get_spot(new_diff)

		return poss		

class King(Piece):
	black = u'\u2654' #colors inverted for black background
	white = u'\u265A'
	diffs = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1],[1, -1], [-1, -1], [-1, 1]]

	def possible_moves(self):
		poss = []
		for diff in self.diffs:
			spot = self.get_spot(diff)
			if not self.is_in_check(spot) and self.check_spot(spot):
				poss.append(spot)

		return poss

	def is_in_check(self, spot):
		return self.test_move(spot, self.is_in_check_helper)
		

	def is_in_check_helper(self, spot):
		pieces = filter(lambda x: isinstance(x, Piece) and x.color != self.color and not isinstance(x, King), self.board.flatten())

		for piece in pieces:
			if self.spot in piece.possible_moves(check_king=False):
				return True

		return False

class Queen(Piece):
	black = u'\u2655' #colors inverted for black background
	white = u'\u265B'
	dir_diffs = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1],[1, -1], [-1, -1], [-1, 1]] #direction of the diffs

class Bishop(Piece):
	black = u'\u2657' #colors inverted for black background
	white = u'\u265D'
	dir_diffs = [[1, 1],[1, -1], [-1, -1], [-1, 1]]

class Knight(Piece):
	black = u'\u2658' #colors inverted for black background
	white = u'\u265E'
	# poss_jumps = map(self.get_spot, [2, -1], [2, 1], [-2, -1], [-2, 1], [1, -2], [1, 2], [-1, -2], [-1, 2])

	def possible_moves(self, check_king=True):
		diffs = [[2, -1], [2, 1], [-2, -1], [-2, 1], [1, -2], [1, 2], [-1, -2], [-1, 2]]
		poss = []

		for diff in diffs:
			spot = self.get_spot(diff)
			if self.check_spot(spot, check_king=check_king):
				poss.append(spot)

		return poss

class Rook(Piece):
	black = u'\u2656' #colors inverted for black background
	white = u'\u265C'
	dir_diffs = [[1, 0], [-1, 0], [0, 1], [0, -1]] # direction of the diffs.

class Pawn(Piece):
	black = u'\u2659' #colors inverted for black background
	white = u'\u265F'

	def possible_moves(self, check_king=True):

		if self.first_move:
			poss_empty = map(self.get_spot, [[-1, 0], [-2, 0]])
		else:
			poss_empty = map(self.get_spot, [[-1, 0]])

		poss_taken = map(self.get_spot, [[-1, -1], [-1, 1]]) #taken by opponent color
		poss = []

		for spot in poss_empty:
			if self.board.in_bounds(spot) and self.board.spot_empty(spot):
				if check_king and self.king_is_in_check(spot):
					continue
				poss.append(spot)

		for spot in poss_taken:
			if self.board.in_bounds(spot):
				if check_king and self.king_is_in_check(spot):
					continue
				other_piece = self.board.grid[spot[0]][spot[1]]
				if isinstance(other_piece, Piece) and other_piece.color != self.color:
					poss.append(spot)

		return poss
		

