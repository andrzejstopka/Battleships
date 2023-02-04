import socket
import json

from game_logic import Board
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
 
    def locate_ships(self, conn, user_board):
        ## It get inputs from a client to locate him ships 
        for ship in user_board.ships:
            while True:
                arrangement = board_arrangement(user_board.board)       # convert user board to message
                conn.send(bytes(json.dumps(arrangement), encoding="utf-8"))
                accept_arrangement = conn.recv(1024)
                request = cord_request(ship.name, ship.occupied_spaces())       # convert ship info to message
                conn.send(bytes(json.dumps(request), encoding="utf-8"))
                cord = json.loads(conn.recv(1024))          # get user info
                cord = cord["body"]         # cords in message body
                result = user_board.place_user_ship(ship, cord)  
                # insert cords to function to place ship on the board if input is valid
                if ship is user_board.ships[-1]:
                    result = "Done"
                server_acceptance = cord_answer(result)    # convert to message if input is valid
                conn.send(bytes(json.dumps(server_acceptance), encoding="utf-8"))
                if result == "Placed" or result == "Done":          # if input is valid, go to the next ship
                    break

    def player_shoot(self, conn, server_board):
        while True:
            conn.send(bytes(json.dumps(shot_request()), encoding="utf-8"))
            shoot_result = json.loads(conn.recv(1024))
            cords = shoot_result["body"]["row"] + shoot_result["body"]["column"]
            result = server_board.check_shoot(cords)
            shot_response = shot_answer(result)
            conn.send(bytes(json.dumps(shot_response), encoding="utf-8"))
            if result == "Miss":
                break
            

    def main(self):
        conn = server.get_client()[0]       # get_client return connection and address, we need only connection
        invitation = json.loads(conn.recv(1024))        # when server receive invitation, it return right answer:
        response = server_game_invitation(self.playing)         # convert to message, if self.playing is True it refuse a game
        conn.send(bytes(json.dumps(response), encoding="utf-8"))
        if response["status"] == 0:         # status 0 means all is right
            self.playing = True
            server_board = Board()
            user_board = Board()
            server_board.locate_server_ships()
            self.locate_ships(conn, user_board)
            while True:
                self.player_shoot(conn, server_board)
                break
            


if __name__ == "__main__":
    server = Server()
    server.main()
