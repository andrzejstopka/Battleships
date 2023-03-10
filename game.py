class Board():
    def __init__(self):
        self.board = [["~"] * 10 for _ in range(10)]
        self.ships = [Ship("Battleship"), Ship("Cruiser"), Ship("Cruiser"), Ship("Submarine"),
                      Ship("Submarine"), Ship("Submarine"), Ship("Destroyer"), Ship("Destroyer"), Ship("Destroyer"), Ship("Destroyer")]
 
    def show_board(self):
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        board_row = 0
        print("    1    2    3    4    5    6    7    8    9    10")
        for x in letters:
            print(x, self.board[board_row])
            board_row += 1
 
    def check_user_input(self, input):
        ### Checks if the user input is valid ###
        if len(input) < 3 or len(input) > 5:
            return False
 
        if input[0] not in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
            return False
 
        if input[1] not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            return False
 
        return True
 
    def convert_user_input(self, input):
        ### Converts the user input to a coordinate example. A1 -> 0, 0, B10 -> 1, 9 ###
 
        length = len(input)
        if length == 3 and input[2] in ["v", "h"]:
            return ord(input[0]) - 65, int(input[1]) - 1, input[2]
        elif length == 4 and input[3] in ["v", "h"]:
            number = input[1] + input[2]
            return ord(input[0]) - 65, int(number) - 1, input[3]
 
    def place_user_ships(self):
        # Game ships
        for ship in self.ships:
            user_input = input(
                f"Enter a start coordinates and horizon(h/v) for {ship.name}({ship.occupied_spaces()} spaces) (e.g. A1v): ")
            if self.check_user_input(user_input) is False:
                print("Invalid input")
                continue
            x, y, h = self.convert_user_input(user_input)   # h - horizon
            if h == "h":
                for space in range(ship.occupied_spaces()):
                    self.board[x][y + space] = "0"
            elif h == "v":
                for space in range(ship.occupied_spaces()):
                    self.board[x + space][y] = "0"
 
    def ship_surrounding(self, ship, board, column, row, direction):
        for space in range(3):
            if direction == 'h':
                if column != 0 and board[column-1][row+space-1] == '0':
                    return False
                if column != 9 and board[column+ship.occupied_spaces()][row+space-1] == '0':
                    return False
                if row != 0 and board[column+space-1][row-1] == '0':
                    return False
                if row != 9 and board[column+space-1][row+1] == '0':
                    return False
            elif direction == 'v':
                if row != 0 and board[column+space-1][row-1] == '0':
                    return False
                if row != 9 and board[column+space-1][row+ship.occupied_spaces()] == '0':
                    return False
                if column != 0 and board[column-1][row+space-1] == '0':
                    return False
                if column != 9 and board[column+1][row+space-1] == '0':
                    return False
        return True
 
class Ship:
    def __init__(self, name):
        self.name = name
 
    def occupied_spaces(self):
        if self.name == "Battleship":
            return 4
        elif self.name == "Cruiser":
            return 3
        elif self.name == "Submarine":
            return 2
        elif self.name == "Destroyer":
            return 1
 
#############################################################
#                      Main Game                            #
#############################################################
 
 
server_board = Board()
server_shot_board = Board()
user_board = Board()
user_shot_board = Board()
 
 
def main():
    quit = False
    while quit == False:
        user_board.place_user_ships()
        user_board.show_board()
 
 
if __name__ == "__main__":
    main()