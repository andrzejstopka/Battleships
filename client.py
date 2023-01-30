import socket
import json

from messages import *

def send_cord(cord_request):
    cords = input(cord_request)
    if cords[1:3] == "10":
        cords = (cords[0], cords[1:3], cords[-1])
    else:
        cords = (cords[0], cords[1], cords[2])
    return cords
    

HOST = "127.0.0.1" 
PORT = 65432


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        input("You are now connected to the Battleship server, press any key to continue")
        s.send(bytes(game_invitation, encoding="UTF-8"))
        acceptance = json.loads(s.recv(1024))
        if acceptance["status"] == 0:
            while True:
                cord_request = s.recv(1024)
                cord_request = json.loads(cord_request)
                if cord_request["message"] == "Done":
                    break
                cords = send_cord(cord_request["message"])
                cords = json.dumps(send_ships_cords(cords[0], cords[1], cords[2]))
                s.send(bytes(cords, encoding="utf-8"))
                acceptance = json.loads(s.recv(1024))

if __name__ == "__main__":
    main()