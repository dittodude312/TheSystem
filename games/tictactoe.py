from random import choice

def display(sprite):
    for line in sprite:
        for char in line:
            print(char, end="")
        print()


def put(spot, board, char):
    col = {"a":1, "b":2, "c":3}[spot[0]]
    row = int(spot[1])

    tmpc =  4 * col - 1
    tmpr =  2 * row - 1

    if board[tmpr][tmpc] != " ":
        return board
    
    board[tmpr][tmpc] = char

    return board


def player(board):
    while True:
        spot = input("Enter place (ex. a1): ")
        if len(spot) != 2:
            print("Invalid input.")
            continue
        if spot[0] not in ("a", "b", "c") or spot[1] not in ("1", "2", "3"):
            print("Invalid input.")
            continue

        tmp = [layer.copy() for layer in board]

        tmp = put(spot, tmp, "X")
        if board == tmp:
            print("Already placed there.")
            continue
    
        board = tmp
        break

    return board, spot


def computer(board):
    while True:
        spot = choice(("a", "b", "c")) + choice(("1", "2", "3"))
        tmp = [layer.copy() for layer in board]
        
        tmp = put(spot, tmp, "O")
        if tmp == board:
            continue

        board = tmp
        break
    return board, spot


def check_win(board, prev_spot):
    _ = {"a":1, "b":2, "c":3}[prev_spot[0]]
    col = 4 * _ - 1
    row = 2 * int(prev_spot[1]) - 1

    row_indices = (1, 3, 5)
    col_indices = (3, 7, 11)
    chars = []
    for row_index in row_indices:
        chars.append(board[row_index][col])
    if chars == ["X", "X", "X"] or chars == ["O", "O", "O"]:
        return True
    
    chars = []
    for col_index in col_indices:
        chars.append(board[row][col_index])
    if chars == ["X", "X", "X"] or chars == ["O", "O", "O"]:
        return True
    
    chars = []
    chars.append(board[1][3])
    chars.append(board[3][7])
    chars.append(board[5][11])
    if chars == ["X", "X", "X"] or chars == ["O", "O", "O"]:
        return True
    
    chars = []
    chars.append(board[1][11])
    chars.append(board[3][7])
    chars.append(board[5][3])
    if chars == ["X", "X", "X"] or chars == ["O", "O", "O"]:
        return True

    return False


def replay():
    while True:
        selection = input("Do you want to play again (y/n): ")

        if selection == "y":
            return 1
        elif selection == "n":
            return 0
        else:
            print("Invalid selection.")
            continue


def game_loop(board, wins, losses):
    turns = 0
    while True:
        print("PLAYER TURN")
        display(board)
        board, last_spot = player(board)
        print()
        display(board)

        if check_win(board, last_spot):
            print("You win.")
            wins += 1
            if replay(): return 1, wins, losses
            else: return 0, wins, losses

        turns += 1
        if turns == 5:
            if replay(): return 1, wins, losses
            else: return 0, wins, losses

        print()
        print("COMPUTER TURN")
        board, last_spot = computer(board)
        display(board)
        
        if check_win(board, last_spot):
            print("You lose.")
            losses += 1
            if replay(): return 1, wins, losses
            else: return 0, wins, losses


def main():
    wins = 0
    losses = 0
    running = 1

    while True:    
        board = ["   a   b   c ",
                 "1    |   |   ",
                 "  ---+---+---",
                 "2    |   |   ",
                 "  ---+---+---",
                 "3    |   |   "]
        board = [list(x) for x in board]

        running, wins, losses = game_loop(board, wins, losses)

        if not running:
            break
        else:
            print("-----------------------")
            print()

    print("Thank you for playing.")
    print(f"You won {wins} times.")
    print(f"You lost {losses} times.")