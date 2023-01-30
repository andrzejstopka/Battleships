import socket
import json

from game_logic import Board, Ship
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

    def locate_ships(self, conn):
        server_board = Board()
        user_board = Board()
        server_board.locate_server_ships()
        for ship in user_board.ships:
            while True:
                arrangement = board_arrangement(user_board.board)
                conn.send(bytes(json.dumps(arrangement), encoding="utf-8"))
                request = cord_request(ship.name, ship.occupied_spaces())
                conn.send(bytes(json.dumps(request), encoding="utf-8"))
                cord = json.loads(conn.recv(1024))
                cord = cord["body"]
                result = user_board.place_user_ship(ship, cord)
                server_acceptance = cord_answer(result)
                conn.send(bytes(json.dumps(server_acceptance), encoding="utf-8"))
                if result == "Placed":
                    break
        # conn.send(bytes(json.dumps(locating_done()), encoding="utf-8"))

    def main(self):
        conn = server.get_client()[0]
        invitation = json.loads(conn.recv(1024))
        response = server_game_invitation(self.playing)
        conn.send(bytes(json.dumps(response), encoding="utf-8"))
        if response["status"] == 0:
            self.locate_ships(conn)


if __name__ == "__main__":
    server = Server()
    server.main()
