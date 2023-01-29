import socket
import json

from messages import *
# def main_menu():






HOST = "127.0.0.1" 
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

input("You are now connected to the Battleship server, press any key to continue")

invite = json.dumps({"type":"GAME_INVITATION", "service": None})

s.send(game_invitation)