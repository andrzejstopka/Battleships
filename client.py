import json
import socket

from messages import *


def enter_cord(cord_request):
    cords = input(cord_request).capitalize()
    if cords[1:3] == "10":
        if "Destroyer" in cord_request:
            cords = (cords[0], cords[1:3], "i")
        else:
            cords = (cords[0], cords[1:3], cords[-1])
    else:
        if "Destroyer" in cord_request:
            cords = (cords[0], cords[1], "i")
        else:
            cords = (cords[0], cords[1], cords[2])
    return cords


def show_board(arrangement):
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    board_row = 0
    print("    1    2    3    4    5    6    7    8    9    10")
    for x in letters:
        print(x, arrangement[board_row])
        board_row += 1


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
                board_arrangement = json.loads(s.recv(1024))
                show_board(board_arrangement["body"])
                cord_request = json.loads(s.recv(1024))
                cords = enter_cord(cord_request["message"])
                cords = json.dumps(ships_cords(cords[0], cords[1], cords[2]))
                s.send(bytes(cords, encoding="utf-8"))
                acceptance = json.loads(s.recv(1024))



if __name__ == "__main__":
    main()
