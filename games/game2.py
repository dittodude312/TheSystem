from random import shuffle
from time import sleep

GUN = [" __--____________________/===}------|  ",
       "{ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~              \\ ",
       "{________________{-----------}       |]",
       "                 {===========}        /",
       "                 {-----------}       / ",
       "                      \\  L \\        |  ",
       "                       \\____|       |  ",
       "                            |       |  ",
       "                             \\      |  ",
       "                             |______|  "]


def display_sprite(sprite):
    for line in sprite:
        print(line)


def initialize():
    bullets = [0, 0, 0, 0, 0, 1]

    shuffle(bullets)
    return bullets


def player(bullets):
    input("PULL TRIGGER ")
    result = bullets.pop()

    print(".", end="", flush=True)
    sleep(1)
    print(".", end="", flush=True)
    sleep(1)
    print(".", flush=True)
    sleep(0.5)
    
    if result:
        print("Fired bullet.\nYou are dead.")
        return 1, bullets
    else:
        print("Fired blank.")
        return 0, bullets


def computer(bullets):
    result = bullets.pop()
    
    print(".", end="", flush=True)
    sleep(1)
    print(".", end="", flush=True)
    sleep(1)
    print(".", flush=True)
    sleep(0.5)

    if result:
        print("Fired bullet.\nYou win.")
        return 1, bullets
    else:
        print("Fired blank.")
        return 0, bullets
    

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


def main():
    rounds = 1
    wins = 0
    bullets = initialize()

    while True:
        print(f"ROUND {rounds}")
        print("*"*15)
        display_sprite(GUN)
        player_result, bullets = player(bullets)

        if player_result:
            print(f"You lasted {rounds - 1} rounds.")
            print(f"You won {wins} times.")
            exit()
        
        print("= = = = = =")
        input("Opponent's turn ")
        computer_result, bullets = computer(bullets)
        
        if computer_result:
            wins += 1
            if replay():
                rounds = 1
                continue
            else:
                print("Thank you for playing.")
                print(f"You won {wins} times.")
                exit()
        
        rounds += 1
        print()