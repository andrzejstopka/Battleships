class Board():
    def __init__(self):
        self.board = [["~"] * 10 for _ in range(10)]

    def show_board(self):
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        board_row = 0
        print("    1    2    3    4    5    6    7    8    9    10")
        for x in letters:
            print(x, self.board[board_row])
            board_row += 1


def check_user_input(input):
    ### Checks if the user input is valid ###

    if input[0] not in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
        return False

    if input[1] not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
        return False

    return True


def convert_user_input(input):
    ### Converts the user input to a coordinate example. A1 -> 0, 0, B10 -> 1, 9 ###

    length = len(input)
    if length == 2:
        return ord(input[0]) - 65, int(input[1]) - 1
    elif length == 3:
        number = input[1] + input[2]
        return ord(input[0]) - 65, int(number) - 1


def place_ships(board):
    # Game ships
    ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    for ship in ships:
        for x in range(ship):
            user_input = input("Enter a coordinate: ")
            if check_user_input(user_input) == False:
                print("Invalid input")
                continue
            x, y = convert_user_input(user_input)
            board.board[x][y] = "0"


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
        place_ships(user_board)
        print(user_board.show_board())


if __name__ == "__main__":
    main()
