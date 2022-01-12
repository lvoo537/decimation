import socket
import pickle
import sys
import time

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "139.177.193.4"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            # time.sleep(10)
            p = pickle.loads(self.client.recv(2048))
            # while p == None:
            #     p = pickle.loads(self.client.recv(2048))
            print(p)
            return p
        except Exception as e:
            print(e)
            print("yikes")

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
