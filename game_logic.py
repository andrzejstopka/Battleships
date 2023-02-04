import random


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
        if len(input) < 2 or len(input) > 5:
            return False

        if input[0] not in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
            return False

        if input[1] not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            return False

        if input[-1] not in ["h", "v", "i"]:
            return False

        return True

    def convert_user_input(self, input, shot):
        ### Converts the user input to a coordinate example. A1 -> 0, 0, B10 -> 1, 9 ###
        length = len(input)
        if shot:
            try:
                if length == 2:
                    return ord(input[0]) - 65, int(input[1])
                elif length == 3:
                    return ord(input[0]) - 65, int(input[1:3])
            except ValueError:
                return False, False       
        else:
            if length == 3 and input[2] in ["v", "h"]:
                return ord(input[0]) - 65, int(input[1]) - 1, input[2]
            elif length == 3 and input[2] == "i":
                return ord(input[0]) - 65, int(input[1]) - 1, input[2]
            elif length == 4 and input[3] in ["v", "h"]:
                number = input[1] + input[2]
                return ord(input[0]) - 65, int(number) - 1, input[3]
            elif length == 4 and input[3] == "i":
                number = input[1] + input[2]
                return ord(input[0]) - 65, int(number) - 1, input[3]

    def place_user_ship(self, ship, cord):
        cord = cord["row"] + cord["column"] + cord["horizon"]
        if self.check_user_input(cord) is False:
            return "Invalid cords, please try again"
        x, y, h = self.convert_user_input(cord, False)  # h - horizon
        ship_occupied_spaces = ship.occupied_spaces()
        ship.places = []
        # checked places, ship is not added when is checked because it would corrupt check_ship_surrounding function
        if h == "h":
            if y + ship_occupied_spaces > 10:   # check if ship crosses the border
                return "Invalid input (The ship crosses the border), try again"
            for space in range(ship_occupied_spaces):
                # when any piece of ship is wrong, ship is not addded.
                if self.check_ship_surrounding(x, y + space) is False:
                    return "Invalid cords, try again"
                ship.places.append((x, y + space))
        elif h == "v":
            if x + ship_occupied_spaces > 10:  # check if ship crosses the border
                return "Invalid input (The ship crosses the border), try again"
            for space in range(ship_occupied_spaces):
                # when any piece of ship is wrong, ship is not addded.
                if self.check_ship_surrounding(x + space, y) is False:
                    return "Invalid cords, try again"
                ship.places.append((x + space, y))
        elif h == "i":
            if self.check_ship_surrounding(x, y) is False:
                return "Space is already occupied, try again"
            ship.places.append((x, y))
        if len(ship.places) == ship_occupied_spaces:
            for place in ship.places:
                # if all spaces is correct, ship is added to the board
                self.board[place[0]][place[1]] = "0"
            return "Placed"

    def check_ship_surrounding(self, x, y):
        # check if any surrounding spaces are occupied
        positions = [self.board[x][y] for x, y in [(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x - 1, y - 1),
                                                   (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1)]
                     if x >= 0 and y >= 0 and x < len(self.board) and y < len(self.board[x])]
        for position in positions:
            try:
                if position != "~":
                    return False
            except IndexError:  # if x would be "J" or y would be 10, it mean that add ship is possible
                pass
        return True

    def locate_server_ships(self):
        # Automatically, randomly locate ships
        for ship in self.ships:
            ship_occupied_spaces = ship.occupied_spaces()
            possible_start_cord = []
            for x in self.board:
                # I do this way, because list.index(arg) doesn't work. It find first occurency but every element in the list is the same.
                y_index = 0
                x_index = self.board.index(x)
                for y in x:
                    if all(self.check_ship_surrounding(x_index + z, y_index) and x_index + z < 10 for z in range(0, ship_occupied_spaces)):
                        possible_start_cord.append((x_index, y_index, "v"))
                    if all(self.check_ship_surrounding(x_index, y_index + z) and y_index + z < 10 for z in range(0, ship_occupied_spaces)):
                        possible_start_cord.append((x_index, y_index, "h"))
                    # I do this way, because list.index(arg) doesn't work. It find first occurency but every element in the list is the same.
                    y_index += 1
            start_cord = random.choice(possible_start_cord)
            x, y, h = start_cord    # h - horizon
            if h == "v":
                for z in range(ship_occupied_spaces):
                    self.board[x + z][y] = "0"
                    ship.places.append((x + z, y))
            elif h == "h":
                for z in range(ship_occupied_spaces):
                    self.board[x][y + z] = "0"
                    ship.places.append((x + z, y))

    def count_ships_elements(self):
        return sum(row.count(1) for row in self.board)

    def check_shoot(self, cords):
        x, y = self.convert_user_input(cords, True)
        if x is False:
            return "Out of the board, try again"
        for ship in self.ships:
            if (x, y) in ship.places:
                self.board[x][y] = "X"
                ship.places.remove((x, y))
                if len(ship.places) == 0:
                    return "Sinking"
                else:
                    return "Hit"
            else:
                self.board[x][y] = "/"
                return "Miss"
        


class Ship:
    places = []
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
