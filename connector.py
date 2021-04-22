# for testing purpose

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 13000        # The port used by the server

text = "a swordman fighting with two ghost"
type = "message"

# text = "clear"
# type = "command"

mark = "<UNK>"
if type == "message":
    mark = "<EOF>"
elif type == "command":
    mark = "<COM>"

send_data = text + mark

print(send_data)

for i in range(10):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(send_data.encode())
        data = s.recv(1024)

    print('Received', repr(data))


# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(send_data.encode())
#     data = s.recv(1024)
#
# print('Received', repr(data))
