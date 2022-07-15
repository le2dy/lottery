import random
import os
from time import sleep

signs = ["H", "S", "C", "D"]
cardNum = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
deck = [[] for _ in range(52)]
dummy = []
players = []
dealer = []
cards = []
chips = []
turn = 0
unveiled = 2


def setting():
    deck_setting()
    distribute()
    show_table()


def deck_setting():
    for i in range(4):
        for j in range(13):
            deck[j + (i * 13)] = cardNum[j] + signs[i]
    random.shuffle(deck)


def distribute():
    global cards
    global deck
    global dealer

    for i in range(5):
        dealer.append(deck.pop())

    cnt = 0
    while cards[len(players) - 1][4] == 0:
        for i in range(len(players)):
            cards[i][cnt] = deck.pop()
        cnt += 1


def show_table():
    os.system('clear')
    show_turn()
    for i in range(5):
        if i < unveiled:
            print(dealer[i], end=' ')
        else:
            print("*", end=' ')
    print()
    CLI()


def show_turn():
    print("Player "+players[turn]+"'s turn.")
    print()


def show_hand():
    global turn

    os.system('clear')
    show_turn()
    print(cards[turn])
    CLI()


def CLI():
    print(">", end='')
    command = input()

    if command.__eq__('back') or command.__eq__('hand'):
        show_hand()
    elif command.__eq__('table'):
        show_table()
    elif command.__eq__('help'):
        print('back: show your hand.')
        print('hand: show your hand.')
        print('table: show table.')
    else:
        print("Wrong command.")
    CLI()


def set_player():
    global cards
    global chips
    global players

    os.system('clear')
    players.clear()
    try:
        print("Enter the number of players.")
        print(">", end=' ')
        num = int(input())
        if num < 2:
            print("Poker needs least 2 person")
            set_player()
            return

        for i in range(num):
            print("Enter player" + str(i) + "'s name.")
            print("Name: ", end='')
            name = input()
            players.append(name)
            cards = [[0 for i in range(5)] for j in range(num)]
            chips = [500 for i in range(num)]

    except ValueError:
        set_player()

    for i in range(3, 0, -1):
        os.system('clear')
        print("Game start in... " + str(i))
        sleep(1)
    setting()


if __name__ == '__main__':
    set_player()


'''

⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏
| 1        1 |
|            |
|            |
|     ♠     |
|            |
|            |
| 1        1 |
‾‾‾‾‾‾‾‾‾‾‾‾‾‾

⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏
| 2        2 |
|     ♠     |
|            |
|            |
|            |
|     ♠     |
| 2        2 |
‾‾‾‾‾‾‾‾‾‾‾‾‾‾

⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏
| 3        3 |
|     ♠     |
|            |
|     ♠     |
|            |
|     ♠     |
| 3        3 |
‾‾‾‾‾‾‾‾‾‾‾‾‾‾

⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏
| 4        4 |
|   ♠   ♠   |
|            |
|            |
|            |
|   ♠   ♠   |
| 4        4 |
‾‾‾‾‾‾‾‾‾‾‾‾‾‾

⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏
| 5        5 |
|   ♠   ♠   |
|            |
|     ♠     |
|            |
|   ♠   ♠   |
| 5        5 |
‾‾‾‾‾‾‾‾‾‾‾‾‾‾


⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏
| 6        6 |
|   ♠   ♠   |
|            |
|   ♠   ♠   |
|            |
|   ♠   ♠   |
| 6        6 |
‾‾‾‾‾‾‾‾‾‾‾‾‾‾



⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏
| 7        7 |
|   ♠   ♠   |
|     ♠      |
|   ♠   ♠   |
|            |
|   ♠   ♠   |
| 7        7 |
‾‾‾‾‾‾‾‾‾‾‾‾‾‾




⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏
| 8        8 |
|   ♠   ♠   |
|     ♠      |
|   ♠   ♠   |
|     ♠      |
|   ♠   ♠   |
| 8        8 |
‾‾‾‾‾‾‾‾‾‾‾‾‾‾



⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏
| 9        9 |
|   ♠   ♠   |
|   ♠   ♠   |
|     ♠     |
|   ♠   ♠   |
|   ♠   ♠   |
| 9        9 |
‾‾‾‾‾‾‾‾‾‾‾‾‾‾



⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏⸏
| 9        9 |
|   ♠   ♠   |
|   ♠   ♠   |
|            |
|   ♠   ♠   |
|   ♠   ♠   |
| 9        9 |
‾‾‾‾‾‾‾‾‾‾‾‾‾‾
̶̰♠♣♥♦⸏——————————————
'''
