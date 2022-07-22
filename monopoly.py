import os
import random
from time import sleep
import re

EMPTY = '\u25A1'
BUY = '\u25A0'
HOUSE1 = '\u25A3'
HOUSE2 = '\u25A6'
HOUSE3 = '\u25A9'
BUILDING = '\u25D9'
START = '\u25B7'
CHANCE = '\u26EF'
TRAIN = '\u26B4'
WATER = '\u26B6'
POWER = '\u26A1'
JAIL = '\u27F0'
PARKING = '\u26FE'
POLICE = '\u260D'
PUBLIC = '\u25EB'
LUXURY = '\u0416'
TAX = '$'
TO_START = 'To Start'
FREE_BAIL = "Free bail"
TO_BANK = ' to Bank'
FROM_BANK = ' from Bank'
board = []
map_data = {}
map_temp = [[' ' for _ in range(11)] for _ in range(11)]
players = []
player_icon = ['\u25E7', '\u25E8', '\u25E9', '\u25EA']
players_current_location = []
players_account = []
players_building = []
players_inventory = []
special_places = {0: 'Start', 2: 'Public', 4: 'Tax', 5: 'Honam Line', 7: 'Chance', 10: 'Jail', 12: 'PowerPlant',
                  15: 'GB Line', 17: 'Public', 20: 'Parking', 22: 'Chance', 25: 'GU Line', 28: 'WaterPlant',
                  30: 'Police', 33: 'Public', 35: 'Jungang Line', 36: 'Chance', 38: 'LuxuryTax'}
lines = [['Start', 'Suwon', 'Public', 'YongIn', 'Tax', 'Honam Line', 'Gunsan', 'Chance', 'Iksan', 'Jeonju', 'Jail'],
         ['Jail', 'Gyoengju', 'PowerPlant', 'Pohang', 'Daegu', 'GB Line', 'Changwon', 'Public', 'Ulsan', 'Busan',
          'Parking'],
         ['Parking', 'Jeju', 'Chance', 'Yeosu', 'Gwangju', 'GU Line', 'Chuncheon', 'Gangneung', 'WaterPlant', 'Wonju',
          'Police'],
         ['Police', 'Cheongju', 'Cheonan', 'Public', 'Daejeon', 'Jungang Line', 'Chance', 'Incheon', 'LuxuryTax',
          'Seoul', 'Start']]
line_data = {}
# key: city number, value:house;building;owner
location_data = {0: 0, 1: 60, 2: 0, 3: 60, 4: 200, 5: 200, 6: 100, 7: 0, 8: 100, 9: 120, 10: 0, 11: 140, 12: 150,
                 13: 140, 14: 160, 15: 200, 16: 180, 17: 0, 18: 180, 19: 200, 20: 0, 21: 220, 22: 0, 23: 220, 24: 240,
                 25: 200, 26: 260, 27: 260, 28: 150, 29: 280, 30: 0, 31: 300, 32: 300, 33: 0, 34: 320, 35: 200, 36: 0,
                 37: 350, 38: 100, 39: 400}
# key: city number, value: price
chance_cards = ["To Suwon", TO_START, 'To Changwon', 'To Gyeongju', 'To Honam Line', "To nearest Line",
                "To nearest Line", 'To nearest plant', '+150 from Bank', '+50 from Bank', '-15 to Bank',
                '-100/B, -25/H to Bank', '-50 to other players', 'Move -3', 'To Jail', 'Free bail']
public_cards = [TO_START, '+200 from Bank', '+100 from Bank', '+100 from Bank', '+50 from Bank', '+25 from Bank',
                '+20 from Bank', '+10 from Bank', '+10 from Bank', '-150 to Bank', '-100 to Bank', '-50 to Bank',
                '-115/B, -40/H to Bank', '+10 from other players', "To Jail", FREE_BAIL]
dices = [1, 1]
turn = 0
distance = 0
inJail = 0
isBuild = False
isMove = False
isRoll = False
crime_value = 0


class Icon:
    HOUSE = '\u2302'
    BUILDING = '\u2338'


class Color:
    BLUE = '\033[94m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    WHITE = '\033[0m'
    BOLD = '\033[1m'
    END = '\033[0m'


def set_icon(kind):
    if kind.__eq__('Chance'):
        icon = CHANCE
    elif kind.__eq__('PowerPlant'):
        icon = POWER
    elif kind.__eq__('WaterPlant'):
        icon = WATER
    elif kind.find('Line') != -1:
        icon = TRAIN
    elif kind.__eq__('Public'):
        icon = PUBLIC
    elif kind.__eq__('Jail'):
        icon = JAIL
    elif kind.__eq__('Police'):
        icon = POLICE
    elif kind.__eq__('Parking'):
        icon = PARKING
    elif kind.__eq__('Tax'):
        icon = TAX
    elif kind.__eq__('LuxuryTax'):
        icon = LUXURY
    else:
        icon = START
    return icon


def set_map():
    board.clear()
    for i in range(40):
        board.append(EMPTY)
        if i in map_data.keys():
            board[i] = map_data[i]
        else:
            map_data[i] = EMPTY
        if i in special_places.keys():
            board[i] = set_icon(special_places[i])
        if i in players_current_location:
            board[i] = player_icon[players_current_location.index(i)]


def set_color(i, j):
    col = ' '
    if i == 0:
        col = Color.BLUE + board[j] + Color.END
    elif j == 10 and i != 0:
        col = Color.RED + board[j + i] + Color.END
    elif i == 10 and j != 10:
        col = Color.GREEN + board[30 - j] + Color.END
    elif j == 0 and i != 0 and i != 10:
        col = Color.YELLOW + board[40 - i] + Color.END
    return col


def show_map():
    for i in range(11):
        for j in range(11):
            map_temp[i][j] = set_color(i, j)

    map_temp[0][0] = Color.WHITE + board[0] + Color.END
    map_temp[0][10] = Color.WHITE + board[10] + Color.END
    map_temp[10][10] = Color.WHITE + board[20] + Color.END
    map_temp[10][0] = Color.WHITE + board[30] + Color.END

    for i in map_temp:
        for j in i:
            print(j, end=' ')
        print()

    for i in range(len(players)):
        print(players[i] + ": " + player_icon[i], end='  ')
    print()


def set_player():
    os.system('clear')
    num = 0

    try:
        num = int(input("How many player? (2~4)\n> "))

        if 2 > num or num > 4:
            print("Enter the right number.")
            sleep(1)
            set_player()
            return
    except ValueError:
        print("Plz enter as number.")
        sleep(2)
        set_player()

    for i in range(num):
        players.append(input("p" + str(i + 1) + " name: "))
        players_current_location.append(0)
        players_account.append(1500)
        players_building.append([0, 0])
        players_inventory.append([])


def roll_the_dice():
    global distance
    global isRoll
    global isMove
    global crime_value

    isMove = False

    dices[0] = random.randint(1, 6)
    dices[1] = random.randint(1, 6)

    print(str(dices[0]) + " + " + str(dices[1]) + " = " + str(sum(dices)))

    distance = sum(dices)

    if dices[0] != dices[1]:
        isRoll = True
    else:
        crime_value += 1
        if 'inJail' in players_inventory[turn]:
            print("You success to escape!")

    if crime_value == 3:
        players_current_location[turn] = 10
        players_inventory[turn].append('inJail')
        print("Your in Jail...")

    cli()


def start():
    os.system('clear')

    set_map()
    show_map()

    print(players[turn] + "'s turn.")

    cli()


def show_line():
    try:
        cmd = int(input("Which line want to see?\n> "))
        if 4 < cmd or cmd < 1:
            print("Line " + str(cmd) + " doesn't exists.")

        tile = ''',____________,
|name|
|------------|
|building|
|owner|
'____________'
'''
        none = '            '

        os.system('clear')
        show_map()

        length = int(len('            ') / 2)
        split_tile = tile.split("\n")
        for i in split_tile:
            tmp = ''
            for j in range(11):
                l2 = length - int(len(lines[cmd - 1][j]) / 2)
                name = ' ' * l2 + lines[cmd - 1][j] + ' ' * l2
                if (cmd * 10 + j) in line_data:
                    data = line_data[cmd * 10 + j].split(';')
                    building = convert_text(data)
                    owner = data[2]
                else:
                    building = none
                    owner = none
                tmp += i.replace('name', name[:12]).replace("building", building).replace("owner", owner) + ' '
            print(tmp)
        cli()

    except ValueError:
        print("Enter as number(1~4).")
        show_line()


def convert_text(data):
    building = ''
    one = '      @     '
    two = '   @    @   '
    three = '  @   @  @  '

    if int(data[1]) == 1:
        building = one.replace('@', Icon.BUILDING)
    elif int(data[0]) == 1:
        building = one.replace('@', Icon.BUILDING)
    elif int(data[0]) == 2:
        building = two.replace('@', Icon.BUILDING)
    elif int(data[0]) == 3:
        building = three.replace('@', Icon.BUILDING)

    return building


def check():
    if 'inJail' in players_inventory[turn]:
        msg = "Choose the option. (l: show line  r: roll the dices  m: move  p: bail($50) i: info d: done)\n> "
    elif players_current_location[turn] in special_places:
        value = special_places[players_current_location[turn]]
        if "Line" in value or "Plant" in value:
            msg = "Choose the option. (l: show line  r: roll the dices  m: move  b: buy i: info d: done)\n> "
        else:
            msg = "Choose the option. (l: show line  r: roll the dices  m: move i: info d: done)\n> "
    else:
        msg = "Choose the option. (l: show line  r: roll the dices  m: move  b: build i: info d: done)\n> "
    return msg


def cli():
    global distance
    global isRoll
    global isBuild

    msg = check()

    cmd = input(msg)

    if cmd.__eq__('l'):
        show_line()
    elif cmd.__eq__('r'):
        if not isRoll:
            roll_the_dice()
    elif cmd.__eq__('m'):
        action_m()
    elif cmd.__eq__('b'):
        action_b()
    elif cmd.__eq__('d'):
        if not isRoll:
            start()
            return
        set_turn()
    elif cmd.__eq__('p') and 'inJail' in players_inventory[turn]:
        bail()
        players_inventory[turn].remove('inJail')
    elif cmd.__eq__('i'):
        info()
    start()


def action_m():
    if distance == 0:
        cli()
        return
    if not isMove:
        if 'inJail' in players_inventory[turn] and (dices[0] != dices[1]):
            print("You didn't success to escape.")
            cli()
            return
        move()


def action_b():
    if players_current_location[turn] in special_places:
        value = special_places[players_current_location[turn]]
        if "Line" in value or "Plant" in value:
            buy()
    else:
        if not isBuild:
            build()


def bail():
    if 'Free bail' in players_inventory[turn]:
        free_bail = input("You have 'free bail' coupon.\nUse or not?\n> ")
        if free_bail.__eq__('use') or free_bail.__eq__('y'):
            players_inventory[turn].remove(free_bail)
        else:
            players_account[turn] -= 50
    else:
        players_account[turn] -= 50


def info():
    os.system('clear')
    set_map()
    show_map()
    print(START + " : Starting point", PUBLIC + " : Public fund", TAX + " : Tax", TRAIN + " : Train station",
          CHANCE + " : Chance card", POLICE + " : Police office", JAIL + " : Jail", POWER + " : Power plant",
          PARKING + " : Parking lot(free)",
          WATER + " : Water plant", LUXURY + " : Luxury tax")


def buy():
    loc = players_current_location[turn]
    if players_account[turn] < location_data[loc]:
        print("You don't have enough money.")
        cli()
    elif special_places[loc].endswith('Plant'):
        line_data[loc] = '0;0;' + players[turn]
        players_account[turn] -= location_data[loc]
    elif special_places[loc].endswith('Line'):
        line_data[loc] = '0;0;' + players[turn]
        players_account[turn] -= location_data[loc]
        trains = [special_places[5], special_places[15], special_places[25], special_places[35]]
        indexes = [i for i, x in enumerate(trains) if x.__eq__('0;0;' + players[turn])]
        for i in indexes:
            location_data[5 * (int(i) + 1)] = 200 * len(indexes)


def build():
    global isBuild

    if 'inJail' in players_inventory[turn]:
        print("You can't do that.")
    # key: city number, value:house;building;owner
    isBuild = True
    cur = players_current_location[turn]
    tile = map_data[cur]

    print("Account: " + str(players_account[turn]), "Cost: " + str(location_data[cur]))
    yn = input("Are you sure?(Y/N)\n> ")

    if yn.lower().__eq__('y'):
        if tile.__eq__(EMPTY):
            map_data[cur] = BUY
            line_data[cur] = '0;0;' + players[turn]
            players_account[turn] -= location_data[cur]
        elif tile.__eq__(BUY):
            map_data[cur] = HOUSE1
            line_data[cur] = '1;0;' + players[turn]
            location_data[cur] += 50
            players_account[turn] -= 50
        elif tile.__eq__(HOUSE1):
            map_data[cur] = HOUSE2
            line_data[cur] = '2;0;' + players[turn]
            location_data[cur] += 100
            players_account[turn] -= 100
        elif tile.__eq__(HOUSE2):
            map_data[cur] = HOUSE3
            line_data[cur] = '3;0;' + players[turn]
            location_data[cur] += 150
            players_account[turn] -= 150
        elif tile.__eq__(HOUSE3):
            map_data[cur] = BUILDING
            line_data[cur] = '0;1;' + players[turn]
            location_data[cur] += 250
            players_account[turn] -= 250
        else:
            print("You can't do that.")
            sleep(1)
    else:
        start()
    start()


def move():
    global isMove
    global isBuild

    isMove = True
    players_current_location[turn] += distance
    print(players_current_location[turn])
    if players_current_location[turn] >= 40:
        players_current_location[turn] -= 40
        players_account[turn] += 200

    if players_current_location[turn] in special_places.keys():
        if special_places[players_current_location[turn]].__eq__('Chance'):
            chance()
        elif special_places[players_current_location[turn]].__eq__('Public'):
            public()
        else:
            players_account[turn] -= location_data[players_current_location[turn]]

        isBuild = True

    os.system('clear')

    set_map()
    show_map()

    loc = players_current_location[turn]
    print("You're arrive at " + lines[int(loc / 10)][loc % 10])
    print('Account: ' + str(players_account[turn]))
    cli()


def set_turn():
    global turn
    global isBuild
    global isMove
    global isRoll

    if turn == len(players) - 1:
        turn = 0
    else:
        turn += 1
    isBuild = isMove = isRoll = False

    start()


def chance():
    global distance
    card = chance_cards.pop()

    if card.__eq__(TO_START):
        distance = 40 - players_current_location[turn]
        move()
    elif card.__eq__('To Jail'):
        players_inventory[turn].append('inJail')
        players_current_location[turn] = 10
    elif "from Bank" in card:
        players_account[turn] += int(card.replace(FROM_BANK, ''))
    elif 'to Bank' in card:
        bank(card)
    elif 'to other' in card:
        for i in range(len(players)):
            if i != turn:
                players_account[i] += 50
                players_account[turn] -= 50
    elif card.__eq__(FREE_BAIL):
        players_inventory[turn].append(FREE_BAIL)
    elif card.__eq__('Move -3'):
        distance = -3
        move()
    else:
        dist = trip(card)
        if players_current_location[turn] > dist:
            players_account[turn] += 200
        players_current_location[turn] = dist
    chance_cards.append(card)


def trip(card):
    dist = 0
    if card.endswith('Suwon'):
        dist = 1
    elif card.endswith('Changwon'):
        dist = 16
    elif card.endswith('Gyeongju'):
        dist = 11
    elif card.endswith("Honam Line"):
        dist = 5
    elif 'nearest' in card:
        if card.endswith("Line"):
            d = [5, 15, 25, 35]
        else:
            d = [12, 28]
        d.append(players_current_location[turn])
        d.sort()
        a = d[d.index(players_current_location[turn]) - 1]
        b = d[d.index(players_current_location[turn]) + 1]
        if a > b:
            dist = a
        elif a < b:
            dist = b
        else:
            dist = b
    return dist


def public():
    global distance
    card = public_cards.pop()

    if card.__eq__(TO_START):
        distance = 40 - players_current_location[turn]
        move()
    elif card.endswith(FROM_BANK):
        players_account[turn] += int(card.replace(FROM_BANK, ''))
    elif card.endswith(TO_BANK):
        bank(card)

    else:
        for i in range(len(players)):
            if i != turn:
                players_account[turn] += 10
                players_account[i] -= 10
    public_cards.append(card)


def bank(card):
    if '/' not in card:
        players_account[turn] += int(card.replace(TO_BANK, ''))
    else:
        con = re.sub('/.', '', card).replace(TO_BANK, '').split(', ')
        h = int(con[0]) * players_building[turn][0]
        b = int(con[1]) * players_building[turn][1]
        players_account[turn] += (h + b)


if __name__ == '__main__':
    set_player()
    random.shuffle(chance_cards)
    random.shuffle(public_cards)
    start()
