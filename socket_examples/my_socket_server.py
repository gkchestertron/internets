import socket
import thread

HOST = ''
PORT = 8888

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(5)

def client_thread(conn, addr):
    conn.send('You have connected.\n')

    while True:
        data = conn.recv(1024)
        print 'them: ' + data
        response = raw_input('Please respond to {0}: '.format(addr))
        conn.sendall(response + '\n')
        if not data:
            break

    conn.close()

while True:
    conn, addr = sock.accept()

    print str(addr[0]) + ':' + str(addr[1])

    thread.start_new_thread(client_thread, (conn, addr))

sock.close()
    
