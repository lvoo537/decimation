import socket
from _thread import *
from player_interim import PlayerInterim
import pickle

local_ip = socket.gethostname()
server = socket.gethostbyname(local_ip)
print(server)
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


players = [PlayerInterim(200,100,0,[],0,True,False,True,0,'player','Idle','0',False,400,100), PlayerInterim(200,100,0,[],0,True,False,True,0,'enemy','Idle','0',False,300,200)]
bullet_interims = [[], []]

def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data[0]
            bullet_interims[player] = data[1]

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = (players[0],bullet_interims[0])
                else:
                    reply = (players[1],bullet_interims[1])

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
