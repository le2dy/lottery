import os
import random
from time import sleep

deck = []
signs = ['♠', '♣', '♥', '♦']
numbers = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
players = []
players_hand = []
players_bet = []
min_bet_cost = 0
SB = 0
BB = 0
turn = 0
indicator = 0
stage = 0


def set_deck():
    for i in range(len(signs)):
        for j in range(len(numbers)):
            deck.append(numbers[j] + signs[i])
    random.shuffle(deck)


def set_player():
    os.system('clear')
    try:
        num = int(input("Insert the number of player plays Texas hold'em.(2~10)\n> "))
        if not (10 >= num >= 2):
            raise ValueError
        for _ in range(num):
            players.append(input("Insert the name: "))
            players_hand.append([])
            players_bet.append(0)
    except ValueError:
        print("Wrong number")
        sleep(1)
        set_player()


def distribute(num):
    for _ in range(num):
        for i in range(len(players_hand)):
            players_hand[i].append(deck.pop())
    print(players_hand)


def start():
    global min_bet_cost

    set_role()
    distribute(1)
    os.system('clear')
    try:
        min_bet_cost = int(input("Insert the minimum bet price.(default: 100)"));
    except ValueError:
        min_bet_cost = 100
    print("Bet price is " + str(min_bet_cost))
    print(players[SB] + " is the Small Blind.\nYou bet first.")
    bet(SB)
    print(players[BB] + " is the Big Blind.\nYou bet second.")
    bet(BB)
    distribute(1)
    action()


def action():
    print('a')


def set_role():
    global SB
    global BB
    global indicator

    os.system('clear')

    SB = random.randrange(0, len(players))
    if SB == 0:
        BB = len(players) - 1
    else:
        BB = SB - 1
    indicator = SB


def bet(num):
    try:
        cost = int(input("How much will you bet?\n> "))
        if num == SB and cost != int(min_bet_cost / 2):
            print('Small Blind must bet half of minimum bet price.')
            raise ValueError
        elif num == BB and cost != min_bet_cost:
            print('Big Blind must bet minimum bet price.')
            raise ValueError
        players_bet[num] = cost
        set_turn()
    except ValueError:
        bet(num)


def set_turn():
    global turn
    global stage

    if turn == len(players) - 1:
        turn = 0
        stage += 1
    else:
        turn += 1


if __name__ == '__main__':
    set_deck()
    set_player()
    start()
