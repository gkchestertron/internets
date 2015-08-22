import json

class Player(object):

	def move(self):
		self.print_pieces()
		piece = self.select_piece()
		spot = self.select_move(piece)
		piece.move(spot)

	def print_pieces(self):
		idx = 1
		for piece in self.pieces:
			if piece.spot and piece.possible_moves() == []:
				continue
			print u'{0}: {1}, {2}'.format(idx, unicode(piece), piece.spot)
			idx += 1

	def select_piece(self):
		poss_pieces = filter(lambda x: x.spot and x.possible_moves() != [], self.pieces)
		try: #catch any errors of any kind 
			select = int(raw_input('Please choose the number of which piece you would like to move: '))
			piece = poss_pieces[select-1]
			return piece
		except ValueError:
			select = int(raw_input('Please choose the NUMBER of which piece you would like to move: '))
			piece = self.pieces[select-1]
			return piece

	def select_move(self, piece):
		moves = piece.possible_moves()
		idx = 1
		for move in moves:
			print u'{0}: {1}'.format(idx, move)
			idx += 1
		try:
			select = int(raw_input('Please choose the number of which move you would like to make: '))
			return moves[select-1]
		except:
			select = int(raw_input('Please choose the NUMBER of which move you would like to make: '))
			return moves[select-1]

	def has_moves(self, piece): #MAKE THIS CHECKMATE
		for piece in self.pieces:
			if piece.spot and piece.possible_moves():
				return True

		return False

	#def pieces_off_board(self, piece):

'''class NetworkPlayer(Player):
	def __init__(self, conn):
		self.conn = conn

	def select_piece(self):
		poss_pieces = filter(lambda x: x.possible_moves() != [], self.pieces)
		try: #catch any errors of any kind 
			self.conn.send('Please choose the number of which piece you would like to move: ')
			select = int(self.conn.recv(1024))
			piece = poss_pieces[select-1]
			return piece
		except ValueError:
			self.conn.send('Please choose the NUMBER of which piece you would like to move: ')
			select = int(self.conn.recv(1024))
			piece = self.pieces[select-1]
			return piece

	def select_move(self, piece):
		moves = piece.possible_moves()
		idx = 1
		for move in moves:
			print u'{0}: {1}'.format(idx, move)
			idx += 1
		try:
			self.conn.send('Please choose the number of which move you would like to make: ')
			select = int(self.conn.recv(1024))
			return moves[select-1]
		except:
			self.conn.send('Please choose the NUMBER of which move you would like to make: ')
			select = int(self.conn.recv(1024))
			return moves[select-1]'''

class LocalNetworkPlayer(Player):
	def __init__(self, conn):
		self.conn = conn

	def select_piece(self):
		piece = super(LocalNetworkPlayer, self).select_piece()
		spot = json.dumps(piece.spot)
		self.conn.send(spot)
		return piece

	def select_move(self, piece):
		move = super(LocalNetworkPlayer, self).select_move(piece)
		serialized_move = json.dumps(move)
		self.conn.send(serialized_move)
		return move

class RemoteNetworkPlayer(Player):
	def __init__(self, conn):
		self.conn = conn

	def select_piece(self):
		coords = self.conn.recv(1024)
		coords = json.loads(coords)
		piece = self.board.grid[coords[0]][coords[1]]
		return piece

	def select_move(self, piece):
		move = self.conn.recv(1024)
		move = json.loads(move)
		return list(move)




