import socket

class BattleshipClient:
    def __init__(self, host='localhost', port=12345):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.board = [['-' for i in range(10)] for j in range(10)]
        self.ships = {
            'A': 5,
            'B': 4,
            'S': 3,
            'D': 3,
            'P': 2
        }

    def start_game(self):
        print(self.client_socket.recv(1024).decode())
        self.place_ships()
        print("Ships placed.")
        print(self.client_socket.recv(1024).decode())
        while True:
            guess = input("Enter your guess (e.g. A1): ").strip()
            self.client_socket.sendall(guess.encode())
            result = self.client_socket.recv(1024).decode()
            print(result)
            if 'You won' in result:
                break

    def place_ships(self):
        for ship, size in self.ships.items():
            placed = False
            while not placed:
                print(f"Place your {ship} (size {size}): (e.g. A1 h)")
                position = input().strip()
                x = ord(position[0]) - ord('A')
                y = int(position[1]) - 1
                orientation = position[2]
                if orientation == 'h':
                    if x + size > 9:
                        print("Invalid position. Try again.")
                        continue
                    if all(self.board[y][i] == '-' for i in range(x, x + size)):
                        for i in range(x, x + size):
                            self.board[y][i] = ship
                        placed = True
                        print(f"{ship} placed!")
                    else:
                        print("Invalid position. Try again.")
                elif orientation == 'v':
                    if y + size > 9:
                        print("Invalid position. Try again.")
                        continue
                    if all(self.board[i][x] == '-' for i in range(y, y + size)):
                        for i in range(y, y + size):
                            self.board[i][x] = ship
                        placed = True
                        print(f"{ship} placed!")
                    else:
                        print("Invalid position. Try again.")
                else:
                    print("Invalid orientation. Try again.")

client = BattleshipClient()
client.start_game()