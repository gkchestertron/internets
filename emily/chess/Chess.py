class Game(object):
	def __init__(self):


class Player(object):
	def __init__(self):


class Board(object):
	def __init__(self):



class Piece(object):
	def __init__(self, color):
		self.color = color

	def move(self):
		pass


class King(Piece):
	white = u'\u2654'
	black = u'\u265A'

	def possible_moves(self):
		pass


class Queen(Piece):
	white = u'\u2655'
	black = u'\u265B'

	def possible_moves(self):
		pass


class Bishop(Piece):
	white = u'\u2657'
	black = u'\u265D'

	def possible_moves(self):
		pass

class Knight(Piece):
	white = u'\u2658'
	black = u'\u265E'

	def possible_moves(self):
		pass

class Rook(Piece):
	white = u'\u2656'
	black = u'\u265C'

	def possible_moves(self):
		pass

class Pawn(Piece):
	white = u'\u2659'
	black = u'\u265F'

	def possible_moves(self):
		pass

