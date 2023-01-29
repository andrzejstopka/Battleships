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
 
    def convert_user_input(self, input):
        ### Converts the user input to a coordinate example. A1 -> 0, 0, B10 -> 1, 9 ###
 
        length = len(input)
        if length == 3 and input[2] in ["v", "h"]:
            return ord(input[0]) - 65, int(input[1]) - 1, input[2]
        elif length == 4 and input[3] in ["v", "h"]:
            number = input[1] + input[2]
            return ord(input[0]) - 65, int(number) - 1, input[3]
    
    def convert_user_input_for_destroyer(self, input):
        ### It must be different from convert_user_input because it is not worth to get horizon for 1-place ship

        length = len(input)
        if length == 3:
            return ord(input[0]) - 65, int(input[1]) - 1
        elif length == 4:
            number = input[1] + input[2]
            return ord(input[0]) - 65, int(number) - 1
    
    def place_user_ships(self):
        # Game ships
        for ship in self.ships:
            self.show_board()
            if ship.name != "Destroyer":
                user_input = input(
                    f"Enter a start coordinates and horizon(h/v) for {ship.name}({ship.occupied_spaces()} spaces) (e.g. A1v): ").capitalize()
                if self.check_user_input(user_input) is False:
                    print("Invalid input")
                    continue
                x, y, h = self.convert_user_input(user_input)   # h - horizon
                places = []  # checked places, ship is not added when is checked because it would corrupt check_ship_surrounding function
                ship_occupied_spaces = ship.occupied_spaces()
                if h == "h":
                    if y + ship_occupied_spaces > 10:  # check if ship crosses the border 
                        print("Invalid input (The ship crosses the border)")
                        continue
                    for space in range(ship_occupied_spaces):
                        if self.check_ship_surrounding(x, y + space) is False: # when any piece of ship is wrong, ship is not addded.
                            print("Invalid space")
                            break
                        places.append((x, y + space)) 
                elif h == "v":
                    if x + ship_occupied_spaces > 10:   # check if ship crosses the border 
                        print("Invalid input (The ship crosses the border)")
                        continue
                    for space in range(ship_occupied_spaces):
                        if self.check_ship_surrounding(x + space, y) is False: # when any piece of ship is wrong, ship is not addded.
                            print("Invalid space")
                            break
                        places.append((x + space, y))
                if len(places) == ship_occupied_spaces:
                    for place in places:
                            self.board[place[0]][place[1]] = "0"   # if all spaces is correct, ship is added to the board
            elif ship.name == "Destroyer":
                user_input = input(
                    f"Enter a coordinates for {ship.name}(e.g. A1): ").capitalize() + "i" # "i" means indifferent to use check_user_input
                if self.check_user_input(user_input) is False:
                    print("Invalid input")
                    continue
                x, y = self.convert_user_input_for_destroyer(user_input)
                if self.check_ship_surrounding(x, y):
                    self.board[x][y] = "0"
                else:
                    print("Space is already occupied!")
            
 
    def check_ship_surrounding(self, x, y):
        # check if any surrounding spaces are occupied
        positions = [self.board[x][y] for x, y in [(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x - 1, y - 1), \
                        (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1)] \
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
                y_index = 0     # I do this way, because list.index(arg) doesn't work. It find first occurency but every element in the list is the same.
                x_index = self.board.index(x)
                for y in x:
                    if all(self.check_ship_surrounding(x_index + z, y_index) and x_index + z < 10 for z in range(0, ship_occupied_spaces)):
                        possible_start_cord.append((x_index, y_index, "v"))
                    if all(self.check_ship_surrounding(x_index, y_index + z) and y_index + z < 10 for z in range(0, ship_occupied_spaces)): 
                        possible_start_cord.append((x_index, y_index, "h"))
                    y_index += 1  # I do this way, because list.index(arg) doesn't work. It find first occurency but every element in the list is the same.
            start_cord = random.choice(possible_start_cord)
            x, y, h = start_cord    # h - horizon
            if h == "v":
                for z in range(ship_occupied_spaces):
                    self.board[x + z][y] = "0"
            elif h == "h":
                for z in range(ship_occupied_spaces):
                    self.board[x][y + z] = "0"
        self.show_board()

            
 
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
 
def main():
    server_board = Board()
    server_shot_board = Board()
    user_board = Board()
    user_shot_board = Board()
    server_board.locate_server_ships()
    user_board.place_user_ships()

        
 
if __name__ == "__main__":
    main()