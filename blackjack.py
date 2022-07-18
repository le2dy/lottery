import random
import os
import sys
from time import sleep

deck = []
numbers = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
signs = ['H', 'D', 'S', 'C']
commands = ['Hit', 'Stand', 'Double down', 'Split', 'Surrender', 'Set A', 'Help']
players = []
player_hands = []
dealers_hand = []
point_list = []
dealers_point = 0
chips = []
bet_chips = []
minimum_bet_price = 0
turn = 0
stage = 1
set_a = 1


def set_deck():
    for i in range(len(signs)):
        for j in range(len(numbers)):
            deck.append(numbers[j] + signs[i])


def shuffle():
    random.shuffle(deck)


def set_player():
    try:
        num = int(input('Insert the number of players(1~7)\n> '))

        if 1 > num or num > 7:
            print("Too many players.")
            set_player()
            return

        for i in range(num):
            players.append(input("Player " + str(i + 1) + "'s name: "))
            chips.append(500)
            player_hands.append([])
            point_list.append(0)
            bet_chips.append(0)
    except ValueError:
        set_player()


def start():
    os.system('clear')
    global minimum_bet_price

    try:
        minimum_bet_price = int(input("Insert the minimum of the bet price (0~500)\n> "))
        if minimum_bet_price < 0 or minimum_bet_price > 500:
            raise ValueError
    except ValueError:
        start()
    distribute()
    show_table('true')
    betting()


def betting():
    global bet_chips
    global dealers_point

    try:
        for i in range(len(players)):
            cost = int(input("Insert the betting price, " + players[i] + ". Minimum: " + str(
                minimum_bet_price) + ", chip left: " + str(chips[i]) + "\n> "))
            if cost < minimum_bet_price:
                raise ValueError
            if chips[i] - cost < 0:
                raise ValueError
            bet_chips[i] = cost
    except ValueError:
        print('You must bet more than minimum.')
        betting()

    player_action()


def distribute():
    global dealers_point

    for _ in range(2):
        for i in range(len(players)):
            player_hands[i].append(deck.pop())
            point_list[i] = count_point(player_hands[i])
    print(player_hands)
    dealers_hand.append(deck.pop())
    dealers_point = count_point(dealers_hand)


def show_table(isHide):
    os.system('clear')
    print("[Table] Round:" + str(stage) + " Cards left: " + str(len(deck)))

    emp = '          '
    length = int((len(emp) - len(str(dealers_point))) / 2)
    up = '⌜' + ' ' * length + str(dealers_point) + ' ' * length + '⌝'
    a = ''
    for i in dealers_hand:
        a += i + ' '
    a = a.strip()
    length = int((len(up) - len(a)) / 2)
    print(up)
    print(' ' * length + a + ' ' * length)
    print('⌞  dealer  ⌟')

    print()

    print(make_box(player_hands, players, isHide))


def player_action():
    global minimum_bet_price

    show_table('false')
    print()

    if chips[turn] == 0:
        print("You lost all chips. Bye, " + players[turn])
        sleep(2)
        set_turn()
    else:
        total = 0
        if players.count(players[turn]) >= 2:
            indices = [i for i, x in enumerate(players) if x == players[turn]]
            for i in indices:
                total += bet_chips[i]
        else:
            total = bet_chips[turn]
        print(players[turn] + "'s turn (chip left: " + str(chips[turn] - total) + ", Point: " + str(
            point_list[turn]) + ")")

    for i in range(len(commands)):
        if i < 3:
            emp = '                 '
            msg = str(i + 1) + '. ' + commands[i]
            msg2 = str(i + 5) + '. ' + commands[i + 4]
            print(msg + ' ' * (len(emp) - len(msg)) + msg2)
    print(str(4) + '. ' + commands[3])

    cmd = input('> ')

    if cmd.__eq__('1') or cmd.lower().__eq__('hit'):
        if str(point_list[turn]).__eq__('bust'):
            player_action()
            return
        add_card(turn)
    elif cmd.__eq__('2') or cmd.lower().__eq__('stand'):
        set_turn()
    elif cmd.__eq__('3') or cmd.lower().__eq__('double down'):
        if str(point_list[turn]).__eq__('bust'):
            player_action()
            return
        elif chips[turn] < bet_chips[turn] * 2:
            print("You don't have enough money.")
            player_action()
            return
        add_card(turn)
        bet_chips[turn] *= 2
    elif cmd.__eq__('4') or cmd.lower().__eq__('split'):
        if str(point_list[turn]).__eq__('bust'):
            player_action()
            return
        if chips[turn] - bet_chips[turn] < bet_chips[turn]:
            print("You don't have enough money.")
            player_action()
            return
        if len(player_hands[turn]) == 2 and player_hands[turn][0].__eq__(player_hands[turn][1]):
            split()
    elif cmd.__eq__('5') or cmd.lower().__eq__('surrender'):
        if stage == 0:
            print('coming soon')
        else:
            print("You can't surrender.")
    elif cmd.__eq__('6') or cmd.lower().__eq__('set a'):
        for i in player_hands[turn]:
            if i[0].__eq__('A'):
                set_A()
                return
        print("You don't have any A")
        sleep(1)
    elif cmd.__eq__('7') or cmd.lower().__eq__('help'):
        print('Hit: Take another card')
        print('Stand: Take no more cards')
        print('Double down: Increase the initial bet by 100% and take one more card')
        print('Split: Create two hands from a starting hand where both cards are the same value')
        print('Surrender: Forfeit half the bet and end the hand')
        print('Help: Show this message')
        print('This message will disappear in 3 seconds')
        sleep(3)

    player_action()


def split():
    players.insert(turn + 1, players[turn])
    player_hands.insert(turn + 1, [])
    player_hands[turn + 1].append(player_hands[turn].pop())
    bet_chips.insert(turn + 1, bet_chips[turn])
    point_list.insert(turn + 1, 0)
    chips.insert(turn + 1, chips[turn])
    add_card(turn)
    add_card(turn + 1)


def set_A():
    global set_a

    choose = int(input('Set A as\n1. 1  2. 11\n> '))
    if choose == 1:
        point_list[turn] += -10 if set_a == 11 else 0
        set_a = 1
    elif choose == 2:
        point_list[turn] += 0 if set_a == 11 else 10
        set_a = 11
    player_action()


def add_card(hand):
    player_hands[hand].append(deck.pop())

    point_list[hand] = count_point(player_hands[hand])


def count_point(hand):
    point = 0

    for card in hand:
        if card[:len(card) - 1].__eq__('A'):
            point += 1
        elif card[:len(card) - 1].__eq__('J') or card[:len(card) - 1].__eq__('Q') or card[:len(card) - 1].__eq__('K'):
            point += 10
        else:
            point += int(card[:len(card) - 1])

    if point > 21:
        calculated_point = 'bust'
    else:
        calculated_point = point

    return calculated_point


def set_turn():
    global turn
    global stage
    global set_a

    set_a = 1
    if turn == len(players) - 1:

        stage += 1
        turn = 0
        dealer_action()
        round_end()
    else:
        turn += 1

    show_table('true')
    player_action()


def dealer_action():
    global dealers_point

    pt = count_point(dealers_hand)

    if isinstance(pt, str) and pt.__eq__('bust'):
        round_end()
    elif pt <= 16:
        dealers_hand.append(deck.pop())
        dealers_point = count_point(dealers_hand)
        show_table('false')
        sleep(1)
        dealer_action()
    else:
        round_end()


def round_end():
    for i in player_hands:
        for _ in range(len(i)):
            deck.append(i.pop())

    for i in range(len(dealers_hand)):
        deck.append(dealers_hand.pop())

    shuffle()

    origin_chips = chips.copy()

    idx = 0
    result = ''
    dealer = 0 if str(dealers_point).__eq__('bust') else dealers_point
    for i in point_list:
        if str(i).__eq__('bust'):
            result += players[idx] + ' is busted '
            chips[idx] -= bet_chips[idx]
        elif i == 21:
            result += players[idx] + ' blackjack! '
            chips[idx] += int(bet_chips[idx] * 1.5)
        elif 22 > i > dealer:
            result += players[idx] + ' is win '
            chips[idx] += bet_chips[idx]
        elif i == dealer:
            result += players[idx] + ' is draw '
        else:
            result += players[idx] + ' is lose '
            chips[idx] -= bet_chips[idx]
        idx += 1

    for p in players:
        if players.count(p) >= 2:
            indices = [i for i, x in enumerate(players) if x == p]
            chips[indices[1]] -= origin_chips[indices[0]]
            chips[indices[0]] += chips[indices[1]]
            del chips[indices[1]]
            del players[indices[1]]
            del player_hands[indices[1]]
            del bet_chips[indices[1]]
            del point_list[indices[1]]

    print(result)
    sleep(3)
    for i in range(len(players)):
        bet_chips[i] = 0
        point_list[i] = 0

    cnt = 0
    for i in chips:

        if i == 0:
            cnt += 1
    if cnt == len(players):
        os.system('clear')
        print("All players are lost their chips.")
        print("The gamble is end.")
        print("Good bye.")
        sleep(.5)
        sys.exit(0)

    start()


def make_box(hand, name, visible):
    upside = ''
    middle = ''
    downside = ''
    chip = ''

    for j in range(len(hand)):
        box = ''
        for i in hand[j]:
            if visible.__eq__('true'):
                box += '* '
            else:
                box += i + " "
        box = box.strip()

        upside += '⌜' + ' ' * len(box) + '⌝  '
        middle += ' ' + box + '   '

        if len(box) > len(name[j]):
            empty = len(box) - len(name[j])
            r = empty - int(empty / 2)
            label = ' ' * int(empty / 2) + name[j] + ' ' * r
        elif len(box) < len(name[j]):
            label = name[j][:len(box) - 3] + '...'
        else:
            label = name[j]

        downside += '⌞' + label + '⌟  '
        d = '⌞' + label + '⌟'
        length = int((len(d) - len(str(bet_chips[j]))) / 2)
        chip += ' ' * length + str(bet_chips[j]) + ' ' * length + '  '

    package = upside + '\n' + middle + '\n' + downside + '\n' + chip

    return package


if __name__.__eq__('__main__'):
    set_deck()
    shuffle()
    set_player()
    start()
