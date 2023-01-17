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


    
server_board = Board()
server_shot_board = Board()
user_board = Board()
user_shot_board = Board()

