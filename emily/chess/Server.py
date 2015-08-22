import socket
import thread
from Game import *

HOST = ''
PORT = 5150

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #makes a socket
sock.bind((HOST, PORT))
sock.listen(1)

def serve_chess(conn, address):
	player1 = LocalNetworkPlayer(conn)
	player2 = RemoteNetworkPlayer(conn)
	game = Game(player1, player2)
	game.play()


while True:
	conn, address = sock.accept()
	thread.start_new_thread(serve_chess, (conn, address))

