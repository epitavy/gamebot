def to_sign(cell):
    if cell == -1:
        return " "
    elif cell == 0:
        return "x"
    else:
        return "o"


def print_board(board):
    for line in board:
        print(f"|{to_sign(line[0])}|{to_sign(line[1])}|{to_sign(line[2])}|")
        print("-------")
