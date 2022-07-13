import os
import random
from time import sleep
from collections import Counter

dices = [1 for i in range(5)]
players = []
scores = [['X' for i in range(12)] for j in range(2)]
bulletins = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"]
bulletins_mission = ["Choice", "4 of a Kind", "Full House", "Little Straight", "Big Straight", "Yacht"]
chance = 3
isRoll = 0
isShowOptions = 0
turn = 0


# LS: 1,2,3,4,5 BS: 2,3,4,5,6 yacht 30pt

def set_dices():
    for i in range(len(dices)):
        dices[i] = 1


def set_bulletin_board():
    board = ''
    for i in range(len(bulletins)):
        board += bulletins[i] + " " + str(scores[0][i]) + " " + str(scores[1][i]) + "\n"

    for i in range(len(bulletins_mission)):
        board += bulletins_mission[i] + " " + str(scores[0][i + 6]) + " " + str(scores[1][i + 6]) + "\n"

    print(board)


def set_player():
    for i in range(2):
        print("Enter Player " + str(i + 1) + "'s name.")
        print(">", end=' ')
        players.append(str(input()))


def set_game():
    os.system('clear')
    set_bulletin_board()

    for i in range(5):
        print(dices[i], end=' ')
    print()

    CLI()


def CLI():
    global turn
    global isShowOptions

    print(players[turn] + ">", end=' ')
    cmd = str(input())

    if isShowOptions:
        try:
            choose_option(cmd)
        except ValueError:
            CLI()

    if cmd.__eq__('roll'):
        if chance == 0:
            print("You can't do that.")
            sleep(0.5)
            set_game()
            return
        roll_dice()
    elif cmd.__eq__('record'):
        if isRoll == 0:
            print("Roll the dices first.")
            sleep(0.5)
            set_game()
            return
        isShowOptions = 1
        show_options()

    set_game()


def choose_option(cmd):
    global scores
    global dices

    score = 0
    if 1 <= int(cmd) <= 6:
        for i in range(len(dices)):
            if int(dices[i]) == int(cmd):
                score += int(cmd)
    elif cmd.__eq__('7'):
        for i in range(len(dices)):
            score += int(dices[i])
    elif cmd.__eq__('8'):
        count = [key for key, _ in Counter(dices).most_common(1)]
        v = Counter(dices).get(count[0])
        if v >= 4:
            score = int(count[0]) * int(v)
    elif cmd.__eq__('9'):
        count = [key for key, _ in Counter(dices).most_common(2)]
        v = Counter(dices).get(count[0])
        v2 = Counter(dices).get(count[1])
        if v >= 3 or v2 >= 2:
            score = (int(count[0]) * int(v)) + (int(count[1]) * int(v2))
    elif cmd.__eq__('10'):
        print('a')
    elif cmd.__eq__('11'):
        print('a')
    elif cmd.__eq__('12'):
        print('a')
    elif cmd.__eq__('13'):
        print('b')

    scores[turn][int(cmd) - 1] = score


def set_turn():
    global isShowOptions
    global turn
    global chance

    set_dices()
    chance = 3
    isShowOptions = 0
    turn = 0 if turn == 1 else 1


def show_options():
    for i in range(6):
        print(str(i + 1) + ". " + bulletins[i], end=' ')
    for i in range(6):
        print(str(i + 7) + ". " + bulletins_mission[i], end=' ')

    print('13. hold')

    CLI()


def roll_dice():
    global chance
    global isRoll

    chance -= 1
    isRoll = 1
    for i in range(len(dices)):
        dices[i] = random.randint(1, 6)

    set_game()


if __name__ == '__main__':
    set_player()
    set_game()
