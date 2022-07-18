import os
import random
from time import sleep

# EMPTY = '🞎'
# BUY = '🞓'
# HOUSE1 = '🞔'
# HOUSE2 = '🞕'
# HOUSE3 = '🞖'
# BUILDING = '🞋'
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
COMMON = '\u25EB'
TAX = '$'
board = []
map_data = {}
map_temp = [[' ' for _ in range(11)] for _ in range(11)]
players = []
player_icon = ['\u25E7', '\u25E8', '\u25E9', '\u25EA']
players_current_location = []
players_account = []
special_places = {0: 'Start', 2: 'Common', 4: 'Tax', 5: 'Honam Line', 7: 'Chance', 10: 'Jail', 20: 'Parking',
                  30: 'Police'}
lines = [['Start', 'Suwon', 'Common', 'YongIn', 'Tax', 'Honam Line', 'Gunsan', 'Chance', 'Iksan', 'Jeonju', 'Jail'],
         ['Jail', 'Gyoengju', 'PowerPlant', 'Pohang', 'Daegu', 'GB Line', 'Changwon', 'Common', 'Ulsan', 'Busan',
          'Parking'],
         ['Parking', 'Jeju', 'Chance', 'Yeosu', 'Gwangju', 'GU Line', 'Chuncheon', 'Gangneung', 'WaterPlant', 'Wonju',
          'Police'],
         ['Police', 'Cheongju', 'Cheonan', 'Common', 'Daejeon', 'Jungang Line', 'Chance', 'Incheon', 'LuxuryTax',
          'Seoul', 'Start']]
line_data = {}
# key: city name, value:house;building;owner
location_data = {}
# key: city name, value: price
chance_cards = []
dices = [1, 1]
turn = 0
distance = 0
isBuild = False
isMove = False
isRoll = False


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
            elif special_places[i].__eq__('Line'):
                board[i] = TRAIN
            elif special_places[i].__eq__('Common'):
                board[i] = COMMON
            elif special_places[i].__eq__('Jail'):
                board[i] = JAIL
            elif special_places[i].__eq__('Police'):
                board[i] = POLICE
            elif special_places[i].__eq__('Parking'):
                board[i] = PARKING
            elif special_places[i].__eq__('Tax'):
                board[i] = TAX
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


def roll_the_dice():
    global distance
    global isRoll

    dices[0] = random.randint(1, 6)
    dices[1] = random.randint(1, 6)

    print(str(dices[0]) + " + " + str(dices[1]) + " = " + str(sum(dices)))

    distance = sum(dices)

    if dices[0] != dices[1]:
        isRoll = True

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
    cmd = input("Choose the option. (l: show line  r: roll the dices  m: move  b: build  d: done)\n> ")

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
            move()
    elif cmd.__eq__('b'):
        if not isBuild:
            build()
    elif cmd.__eq__('d'):
        if not isRoll:
            CLI()
            return
        set_turn()
    CLI()


def build():
    global isBuild

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

    isMove = True
    players_current_location[turn] += distance
    if players_current_location[turn] >= 40:
        players_current_location[turn] -= 39

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


if __name__ == '__main__':
    set_player()
    start()
'''
,__________,
|   name   |
|----------|
|          |
|          |
'__________'
'''
