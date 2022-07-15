import os
import random
from time import sleep

deck = []
turn = 0
cards = []
signs = ['♠', '♣', '♥', '♦']
numbers = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
player = []
banker = []
pair = ''
pPoint = 0
bPoint = 0
account = 1000
bet_cost = 0
bet_kind = 0
two = "     caaaaaaard0z          caaaaaaard1z       "
three = "caaaaaaard0z     caaaaaaard1z     caaaaaaard2z"

empty = ''',----------.
|//////////|
|\\\\\\\\\\\\\\\\\\\\|
|//////////|
|\\\\\\\\\\\\\\\\\\\\|
|//////////|
'----------'
'''

template = ''',----------.
| num     num|
|          |
|    sign     |
|          |
| num     num|
'----------'
'''


def set_deck():
    for _ in range(6):
        for i in range(len(signs)):
            for j in range(len(numbers)):
                deck.append(numbers[j] + signs[i])
    shuffle()


def shuffle():
    i = 0
    while i < 6:
        os.system('clear')
        print('Deck shuffling' + '.' * (i % 3 + 1))
        i += 1
        sleep(0.5)
    random.shuffle(deck)


def set_table():
    global cards

    os.system('clear')
    table = ''',-------------------------Player-------------------------,-------------------------Banker-------------------------.
|                                                        |                                                        |
|                                                        |                                                        |
|                                                        |                                                        |
|                                                        |                                                        |
|                                                        |                                                        |
|     middle00     |     middle10     |
|     middle01     |     middle11     |
|     middle02     |     middle12     |
|     middle03     |     middle13     |
|     middle04     |     middle14     |
|     middle05     |     middle15     |
|     middle06     |     middle16     |
|                                                        |                                                        |
|                                                        |                                                        |
|                                                        |                                                        |
|                                                        |                                                        |
'--------------------------------------------------------'--------------------------------------------------------'
'''

    cards = player + banker

    if len(cards) < 4:
        for _ in range(4 - len(cards)):
            cards.append(empty)

    m1 = two if len(player) <= 2 else three
    m2 = two if len(banker) <= 2 else three

    for i in range(2):
        hand = player if i == 0 else banker
        for j in range(7):
            mid = "middle" + str(i) + str(j)
            table = table.replace(mid, m1 if i == 0 else m2)
            table = table.replace('z', str(j))
        for j in range(len(cards)):
            if j < len(hand):
                card = convert(hand[j]).split('\n')
            else:
                card = empty.split('\n')
            for k in range(len(card)):
                table = table.replace("caaaaaaard" + str(j) + str(k), card[k])

    print(table)
    print("Deck left: " + str(len(deck)))
    print("Account: $" + str(account - bet_cost))
    print("Player " + str(pPoint) + "   Banker " + str(bPoint))
    print()


def convert(card):
    try:
        if int(card[:len(card) - 1]) == 10:
            num = '10'
        else:
            num = str(card[:len(card) - 1]) + ' '
    except ValueError:
        num = str(card[:len(card) - 1]) + ' '
    return set_card(card[len(card) - 1], num)


def set_card(sign, num):
    card = template.replace('num', num).replace('sign', sign)

    return card


def bet():
    global bet_cost
    global bet_kind
    global turn
    global pair

    cmd = input("1. Banker(5% commission)  2. Player  3. Tie  4. Pair\n> ")

    c = cmd.split(' ')

    try:
        if len(c) != 2:
            raise ValueError
        if not (4 >= int(c[0]) >= 1):
            print("Wrong number")
            bet()
            return

        if int(c[0]) == 4:
            b = input("Banker(b) or Player(p)?\n> ")
            if not b.__eq__('b') or b.__eq__('p'):
                raise NotImplementedError
            pair = b

        bet_kind = int(c[0]) - 1
        bet_cost = int(c[1])
    except ValueError:
        print("Enter like [No] [cost]")
        bet()
        sleep(.5)
    except NotImplementedError:
        print("Enter 'b' or 'p'")
        bet()
        sleep(0.5)

    distribute(player, 2)
    distribute(banker, 2)


def distribute(hand, num):
    for _ in range(num):
        card = deck.pop()
        hand.append(card)

        calc_point(hand)

        set_table()
        sleep(1)


def player_action():
    calc_point(player)

    if len(player) == 3:
        calc_point(banker)
        result()
        return

    if 0 <= pPoint < 6:
        distribute(player, 1)
        player_action()
    elif pPoint == 6 or pPoint == 7:
        banker_action()
    else:
        calc_point(banker)
        result()


def banker_action():
    calc_point(banker)
    flag = False

    if len(banker):
        result()
        return

    if 0 <= bPoint < 3 or (bPoint == 3 and pPoint != 8) or (bPoint == 4 and 1 < pPoint < 8) or (
            bPoint == 5 and 3 < pPoint < 8) or (bPoint == 6 and 5 < pPoint < 8):
        flag = True

    if flag:
        distribute(banker, 1)
        banker_action()
    else:
        result()


def result():
    global account

    winner = ''
    if pPoint > bPoint:
        winner = 'p'
    elif pPoint == bPoint:
        winner = 'd'
    else:
        winner = 'b'

    print(winner, bet_kind)

    if bet_kind == 0:
        if winner.__eq__('b'):
            if bPoint == 6:
                account += int(bet_cost * 0.5)
            else:
                account += int(bet_cost * 0.95)
            print("You win!")
        else:
            account -= bet_cost
            print("You lose...")
    elif bet_kind == 1:
        if winner.__eq__('p'):
            account += bet_cost
            print("You win!")
        else:
            account -= bet_cost
            print("You lose...")
    elif bet_kind == 2:
        if winner.__eq__('d'):
            account += bet_cost * 7
            print("You win!")
        else:
            print("Draw!")
    else:
        print(player[0][:len(player[0]) - 1],player[1][:len(player[1]) - 1])
        if player[0][:len(player[0]) - 1].__eq__(player[1][:len(player[1]) - 1]) or banker[0][
                                                                                    :len(banker[0]) - 1].__eq__(banker[
                                                                                                                    1][
                                                                                                                :len(
                                                                                                                    banker[
                                                                                                                        1]) - 1]):
            account += bet_cost * 10
            print("You win!")
        else:
            account -= bet_cost
            print("You lose...")

    yn = input("Do you want to play again? (Y/N)\n> ")
    if yn.lower().__eq__('y'):
        start()


def calc_point(hand):
    global pPoint
    global bPoint

    point = 0
    for i in hand:

        num = str(i[:len(i) - 1])
        if num.__eq__('A'):
            point += 1
        elif num.__eq__('K') or num.__eq__('Q') or num.__eq__('J'):
            point += 0
        else:
            point += int(num) % 10
    if hand == player:
        pPoint = point % 10
    else:
        bPoint = point % 10


def start():
    global pair
    global bet_cost
    global pPoint
    global bPoint

    if len(deck) < 10:
        shuffle()

    player.clear()
    banker.clear()
    pair = ''
    bet_cost = pPoint = bPoint = 0

    set_table()
    bet()
    player_action()


if __name__ == '__main__':
    set_deck()
    start()
