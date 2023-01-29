import socket
import json

from game import Board, Ship, main
from messages import *

class Server:
    host = "127.0.0.1"
    port = 65432
    playing = False

    def get_client(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            conn, addr = s.accept()
            return conn, addr

    # def wait_for_invitation(self, msg):
    #     if msg["type"] == "GAME_INVITATION":
    #         if self.playing:
    #             return socket.error


    # def main(self):
    #     conn = server.get_client()[0]
    #     invitation = json.loads(conn.recv(1024))
    #     response = self.wait_for_invitation(invitation)


        


server = Server()


    
