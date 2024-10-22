import socket
import select

port = 60003
sockL = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockL.bind(("", port))
sockL.listen(1)

listOfSockets = [sockL]

print("Listening on port {}".format(port))

def sendall(msg):
    for c in listOfSockets[1:]: #Send message to all clients
        c.send(msg)
            
while True:
    tup = select.select(listOfSockets, [], [])
    sock = tup[0][0]
    if sock==sockL:
        (sockClient, addr) = sockL.accept()
        msg = bytearray(f"[{addr}] (connected)","ASCII")
        sendall(msg)
        listOfSockets.append(sockClient)
    else:
        data = sock.recv(2048).decode()
        client = sock.getpeername()
        if not data:
            msg = bytearray(f"[{client}] (disconnected)","ASCII")
            sock.close()          
            listOfSockets.remove(sock)
            sendall(msg)
            
        else:
            msg = bytearray(f"[{client}] {data}","ASCII")
            sendall(msg)