import socketserver

HOST, PORT = "localhost", 80

class TCP(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip().decode()
        self.request.sendall(bytearray(f"HTTP/1.1 200 ok\n\n<html>\n<h1>Your browser sent the following request:</h1>\n<pre>\n{self.data}</pre>\n</html>\n", "ASCII") )
    def finish(self):
        print(self.client_address)
        print("Request made")
        
with socketserver.TCPServer((HOST, PORT), TCP) as server:
    server.serve_forever()