import socket

#create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '127.0.0.1'
port = 60003

m_score = 0
o_score = 0

def server():
    s.bind((server_ip, port))    # Server stuff
    s.listen(1)
    c, _ = s.accept()
    rps_game(c)
    s.close()
             
def client(host):
    s.connect((host, port))
    rps_game(s)
    s.close()
    
def rps_game(socket):
    while m_score < 10 and o_score < 10:
        move = input(f"({m_score},{o_score}) Your move: ")
        if move in {"R", "P", "S"}:
            barr = bytearray(move, "ASCII")
            socket.send(barr)
            o_move = socket.recv(1028).decode()
            print(f"(opponents move: {o_move})")
            update_score(move, o_move)
        else:
            print("Invalid move")
    
def update_score(move, o_move):
    global m_score
    global o_score
    match move:
        case "R":
            if o_move == "P":
                o_score += 1
            elif o_move == "S":
                m_score += 1
        case "P":
            if o_move == "S":
                o_score += 1
            elif o_move == "R":
                m_score += 1
        case "S":
            if o_move == "R":
                o_score += 1
            elif o_move == "P":
                m_score += 1

ans = "?"
while ans not in {"C", "S"}:
    ans = input("Do you want to be server (S) or client (C): ")
    
if ans=="S":
    sock = server()
else:
    host = input("Enter the server's name or IP: ")
    sock = client(host)

if m_score == 10:
    print(f"You won 10 against {o_score}")
else:
    print(f"You lost with {m_score} against 10")
    