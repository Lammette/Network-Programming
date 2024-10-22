import socket

HOST, PORT = "localhost", 80

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    name = s.getpeername
    msg = bytearray(f"{name}", "ASCII")
    s.send(msg)
