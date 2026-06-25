class Player:
    def __init__(self, char = "O", x = 1, y = 6):
        self.char = char
        self.x = x
        self.y = y

    def move(self, direction):
        match direction.lower():
            case "w":
                self.y -= 1
            case "a":
                self.x -= 1
            case "s":
                self.y += 1
            case "d":
                self.x += 1
        
        if self.x < 1: self.x = 1
        if self.x > 10: self.x = 10
        if self.y > 6: self.y = 6
        if self.y < 1: self.y = 1


def display_board(board):
    for layer in board:
        for char in layer:
            print(char, end="")
        print()

def main():
    START_POS = (1, 6)
    player = Player()

    board = ["+----------+",
            "|          |",
            "|          |",
            "|          |",
            "|          |",
            "|          |",
            f"|{player.char}         |",
            "+----------+"]
    board = [list(x) for x in board]
    display_board(board)

    board[START_POS[1]][START_POS[0]] = " "

    while True:
        move = input("Enter move: ")
        if move.lower() not in ("w", "a", "s", "d"):
            print("Invalid input.")
            continue

        player.move(move)
        print(f"{player.x},{player.y}")
        board[player.y][player.x] = player.char
        
        print()
        display_board(board)
        board[player.y][player.x] = " "

if __name__ == "__main__":
    main()