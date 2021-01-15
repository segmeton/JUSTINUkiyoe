import socket

class SocketConnector:

    def __init__(self):
        self.HOST = '127.0.0.1'  # The server's hostname or IP address
        self.PORT = 13000        # The port used by the server

    def send(self, text, type):
        mark = "<UNK>"
        if type == "message":
            mark = "<EOF>"
        elif type == "command":
            mark = "<COM>"

        send_data = text + mark

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            s.sendall(send_data.encode())
            data = s.recv(1024)
        print('Received', repr(data))