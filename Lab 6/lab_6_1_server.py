import socket

HOST, PORT = "localhost", 80

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST,PORT))
    server.listen(5)
    while True:
        c, _ = server.accept()
        data = c.recv(1024).decode()
        print(data)
        c.close()