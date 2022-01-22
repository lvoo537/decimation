import socket
from _thread import *
from player_interim import PlayerInterim
import pickle
import  time

# local_ip = socket.gethostname()
# server = 'socket.gethostbyname(local_ip)'
server = ''
print(server)
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")




def threaded_client(conn, player):
    global currentPlayer
    try:
        conn.send(pickle.dumps(players[player]))
    except :
        pass
    reply = ""
    if currentPlayer>=1:
        while True:
            if currentPlayer <1:
                print("other player disconnected, restarting game")
                break
            try:
                data = pickle.loads(conn.recv(2048))
                players[player] = data[0]
                bullet_interims[player] = data[1]
                if currentPlayer <1:
                    print("other player disconnected, restarting game")
                    print("Disconnected")
                    break
                elif not data:
                    print("Disconnected")
                    break
                else:
                    if player == 1:
                        reply = (players[0],bullet_interims[0])
                    else:
                        reply = (players[1],bullet_interims[1])

                    # print("Received: ", data)
                    # print("Sending : ", reply)
                conn.sendall(pickle.dumps(reply))
                if currentPlayer <1:
                    print("other player disconnected, restarting game")
                    print("Disconnected")
                    break
            except:
                break

    print("Lost connection")
    conn.close()
    if currentPlayer == 1:
        currentPlayer -= 1
    elif currentPlayer == 2:
        currentPlayer -= 2




players = [PlayerInterim(200,100,0,[],0,True,False,True,0,'player','Idle','0',False,100,100), PlayerInterim(200,100,0,[],0,True,False,True,0,'enemy','Idle','0',False,1850,100)]
bullet_interims = [[], []]
currentPlayer = 0
run = True
while run:
    if currentPlayer <= 1:
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #
        # try:
        #     s.bind((server, port))
        # except socket.error as e:
        #     str(e)
        #
        # s.listen()
        # print("Waiting for a connection, Server Started")
        # print(s)
        print(currentPlayer)
        players = [PlayerInterim(200,100,0,[],0,True,False,True,0,'player','Idle','0',False,100,100), PlayerInterim(200,100,0,[],0,True,False,True,0,'enemy','Idle','0',False,1850,100)]
        conn, addr = s.accept()
        print("Connected to:", addr)

        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1
        print(currentPlayer)
    else:
        # print("THERE ARE ALREADY 2 PLAYERS PLAYING")
        run = False
        while run == False:
            if currentPlayer <=1:
                time.sleep(5)
                run = True

