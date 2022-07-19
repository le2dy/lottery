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
location_data = {4: 200, 5: 200, 15: 200, 25: 200, 35: 200, 38: 75}
# key: city number, value: price
chance_cards = ["To Suwon", 'To Start', 'To Changwon', 'To Gyeongju', 'To Honam Line', "To nearest Line",
                "To nearest Line", 'To nearest plant', '+150 from Bank', '+50 from Bank', '-15 to Bank',
                '-100/B, -25/H to Bank', '-50 to other players', 'Move -3', 'To Jail', 'Free bail']
public_cards = ['To Start', '+200 from Bank', '+100 from Bank', '+100 from Bank', '+50 from Bank', '+25 from Bank',
                '+20 from Bank', '+10 from Bank', '+10 from Bank', '-150 to Bank', '-100 to Bank', '-50 to Bank',
                '-115/B, -40/H to Bank', '+10 from other players', "To Jail", "Free bail"]
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


def set_map():
    board.clear()
    for i in range(40):
        board.append(EMPTY)
        if i in map_data.keys():
            board[i] = map_data[i]
        else:
            map_data[i] = EMPTY
        if i in special_places.keys():
            if special_places[i].__eq__('Chance'):
                board[i] = CHANCE
            elif special_places[i].__eq__('PowerPlant'):
                board[i] = POWER
            elif special_places[i].__eq__('WaterPlant'):
                board[i] = WATER
            elif special_places[i].find('Line') != -1:
                board[i] = TRAIN
            elif special_places[i].__eq__('Public'):
                board[i] = PUBLIC
            elif special_places[i].__eq__('Jail'):
                board[i] = JAIL
            elif special_places[i].__eq__('Police'):
                board[i] = POLICE
            elif special_places[i].__eq__('Parking'):
                board[i] = PARKING
            elif special_places[i].__eq__('Tax'):
                board[i] = TAX
            elif special_places[i].__eq__('LuxuryTax'):
                board[i] = LUXURY
            else:
                board[i] = START
        if i in players_current_location:
            board[i] = player_icon[players_current_location.index(i)]


def show_map():
    for i in range(11):
        for j in range(11):
            if i == 0:
                map_temp[i][j] = Color.BLUE + board[j] + Color.END
            elif j == 10 and i != 0:
                map_temp[i][j] = Color.RED + board[j + i] + Color.END
            elif i == 10 and j != 10:
                map_temp[i][j] = Color.GREEN + board[30 - j] + Color.END
            elif j == 0 and i != 0 and i != 10:
                map_temp[i][j] = Color.YELLOW + board[40 - i] + Color.END
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
    global crime_value

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

    CLI()


def start():
    os.system('clear')

    set_map()
    show_map()

    print(players[turn] + "'s turn.")

    CLI()


def show_line():
    try:
        cmd = int(input("Which line want to see?\n> "))
        if 4 < cmd or cmd < 1:
            print("Line " + str(cmd) + " doesn't exists.")

        tile = ''',__________,
|name|
|----------|
|          |
|          |
'__________'
'''
        os.system('clear')
        show_map()

        length = int(len('          ') / 2)
        split_tile = tile.split("\n")
        for i in split_tile:
            tmp = ''
            for j in range(11):
                l2 = length - int(len(lines[cmd - 1][j]) / 2)
                name = ' ' * l2 + lines[cmd - 1][j] + ' ' * l2
                tmp += i.replace('name', name[:10]) + ' '
            print(tmp)
        CLI()

    except ValueError:
        print("Enter as number(1~4).")
        show_line()


def CLI():
    if 'inJail' in players_inventory[turn]:
        cmd = input("Choose the option. (l: show line  r: roll the dices  m: move  p: bail($50) i: info d: done)\n> ")
    else:
        cmd = input("Choose the option. (l: show line  r: roll the dices  m: move  b: build i: info d: done)\n> ")

    if cmd.__eq__('l'):
        show_line()
    elif cmd.__eq__('r'):
        if not isRoll:
            roll_the_dice()
    elif cmd.__eq__('m'):
        if distance == 0:
            CLI()
            return
        if not isMove:
            if 'inJail' in players_inventory[turn] and (dices[0] != dices[1]):
                print("You didn't success to escape.")
                CLI()
                return
            move()
    elif cmd.__eq__('b'):
        if not isBuild:
            build()
    elif cmd.__eq__('d'):
        if not isRoll:
            CLI()
            return
        set_turn()
    elif cmd.__eq__('p') and 'inJail' in players_inventory[turn]:
        if 'Free bail' in players_inventory[turn]:
            free_bail = input("You have 'free bail' coupon.\nUse or not?\n> ")
            if free_bail.__eq__('use') or free_bail.__eq__('y'):
                players_inventory[turn].remove("Free bail")
            else:
                players_account[turn] -= 50
        else:
            players_account[turn] -= 50
        players_inventory[turn].remove('inJail')
    elif cmd.__eq__('i'):
        info()
    CLI()


def info():
    os.system('clear')
    set_map()
    show_map()
    print(START + " : Starting point", PUBLIC + " : Public fund", TAX + " : Tax", TRAIN + " : Train station",
          CHANCE + " : Chance card", POLICE + " : Police office", JAIL + " : Jail", POWER + " : Power plant",
          PARKING + " : Parking lot(free)",
          WATER + " : Water plant", LUXURY + " : Luxury tax")


def build():
    global isBuild

    if 'inJail' in players_inventory[turn]:
        print("You can't do that.")

    isBuild = True
    cur = players_current_location[turn]
    tile = map_data[cur]

    if tile.__eq__(EMPTY):
        map_data[cur] = BUY
    elif tile.__eq__(BUY):
        map_data[cur] = HOUSE1
    elif tile.__eq__(HOUSE1):
        map_data[cur] = HOUSE2
    elif tile.__eq__(HOUSE2):
        map_data[cur] = HOUSE3
    elif tile.__eq__(HOUSE3):
        map_data[cur] = BUILDING
    else:
        print("You can't do that.")
        sleep(1)
    print(map_data[cur])
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
    CLI()


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

    if card.__eq__('To Start'):
        distance = 40 - players_current_location[turn]
        move()
    elif card.__eq__('To Jail'):
        players_inventory[turn].append('inJail')
        players_current_location[turn] = 10
    elif "from Bank" in card:
        players_account[turn] += int(card.replace(' from Bank', ''))
    elif 'to Bank' in card:
        if '/' not in card:
            players_account[turn] += int(card.replace(' to Bank', ''))
        else:
            con = re.sub('/.', '', card).replace(' to Bank', '').split(', ')
            h = int(con[0]) * players_building[turn][0]
            b = int(con[1]) * players_building[turn][1]
            players_account[turn] += (h + b)
    elif 'to other' in card:
        for i in range(len(players)):
            if i != turn:
                players_account[i] += 50
                players_account[turn] -= 50
    elif card.__eq__("Free bail"):
        players_inventory[turn].append("Free bail")
    elif card.__eq__('Move -3'):
        distance = -3
        move()
    else:
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
            d = []
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
        if players_current_location[turn] > dist:
            players_account[turn] += 200
        players_current_location[turn] = dist
    chance_cards.append(card)


def public():
    global distance
    card = public_cards.pop()

    if card.__eq__('To Start'):
        distance = 40 - players_current_location[turn]
        move()
    elif card.endswith(' from Bank'):
        players_account[turn] += int(card.replace(' from Bank', ''))
    elif card.endswith(' to Bank'):
        if '/' not in card:
            players_account[turn] += int(card.replace(' to Bank', ''))
        else:
            con = re.sub('/.', '', card).replace(' to Bank', '').split(', ')
            h = int(con[0]) * players_building[turn][0]
            b = int(con[1]) * players_building[turn][1]
            players_account[turn] += (h + b)
    else:
        for i in range(len(players)):
            if i != turn:
                players_account[turn] += 10
                players_account[i] -= 10


if __name__ == '__main__':
    set_player()
    random.shuffle(chance_cards)
    random.shuffle(public_cards)
    start()
'''
,__________,
|   name   |
|----------|
|          |
|          |
'__________'
'''
