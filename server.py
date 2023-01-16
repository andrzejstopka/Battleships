import socket

class BattleshipServer:
    def __init__(self, host='localhost', port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print("Server is listening...")
        self.board = [['-' for i in range(10)] for j in range(10)]
        self.ships = {
            'A': 5,
            'B': 4,
            'S': 3,
            'D': 3,
            'P': 2
        }

    def start_game(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print("Client connected:", client_address)
            client_socket.sendall(b"Welcome to the battleship game! Please place your ships.")
            self.get_client_ships(client_socket)
            print("Client ships placed.")
            client_socket.sendall(b"All ships placed. Game starts.")
            while True:
                client_socket.sendall(b'Enter your guess (e.g. A1):')
                guess = client_socket.recv(1024).decode().strip()
                if not guess:
                    break
                x = ord(guess[0]) - ord('A')
                y = int(guess[1]) - 1
                if self.board[y][x] == '-':
                    client_socket.sendall(b'Miss!')
                else:
                    client_socket.sendall(b'Hit!')
                    self.ships[self.board[y][x]] -= 1
                    if self.ships[self.board[y][x]] == 0:
                        client_socket.sendall(b'You sunk my ' + self.board[y][x].encode() + b'!')
                        del self.ships[self.board[y][x]]
                    if not self.ships:
                        client_socket.sendall(b'You won!')
                        break
            client_socket.close()

    def get_client_ships(self, client_socket):
        for ship, size in self.ships.items():
            placed = False
            while not placed:
                client_socket.sendall(f"Place your {ship} (size {size}):".encode())
                position = client_socket.recv(1024).decode().strip()
                x = ord(position[0]) - ord('A')
                y = int(position[1]) - 1
                orientation = position[2]
                if orientation == 'h':
                    if x + size > 9:
                        client_socket.sendall(b"Invalid position. Try again.")
                        continue
                    if all(self.board[y][i] == '-' for i in range(x, x + size)):
                        for i in range(x, x + size):
                            self.board[y][i] = ship
                        placed = True
                        client_socket.sendall(f"{ship} placed!".encode())
                    else:
                        client_socket.sendall(b"Invalid position. Try again.")
                elif orientation == 'v':
                    if y + size > 9:
                        client_socket.sendall(b"Invalid position. Try again.")
                        continue
                    if all(self.board[i][x] == '-' for i in range(y, y + size)):
                        for i in range(y, y + size):
                            self.board[i][x] = ship
                        placed = True
                        client_socket.sendall(f"{ship} placed!".encode())
                    else:
                        client_socket.sendall(b"Invalid position. Try again.")
                else:
                    client_socket.sendall(b"Invalid orientation. Try again.")

server = BattleshipServer()
server.start_game()