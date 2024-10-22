import socketserver

HOST, PORT = "localhost", 80

s = socketserver.TCPServer((HOST, PORT))
s.serve_forever()