import random
import os
import sys
from time import sleep

myHands = []
otherHands = []
deck = [[] for i in range(54)]
dummy = []
signs = ["H", "S", "C", "D"]
cardNum = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
color = {"H": "RED", "S": "BLACK", "C": "BLACK", "D": "RED", "Black": "BLACK", "Color": "RED"}
flag = "M"
turn = "M"
winFlag = 0
top = []
attackStack = 0
col = ""


def setting():
    global flag
    global deck
    global myHands
    global otherHands
    global signs
    global cardNum
    global dummy
    global col

    for i in range(4):
        for j in range(13):
            deck[j + (i * 13)] = [cardNum[j], signs[i]]
    deck[52] = ["Joker", "Black"]
    deck[53] = ["Joker", "Color"]

    random.shuffle(deck)

    while len(otherHands) < 7 or len(myHands) < 7:
        if flag.__eq__("M"):
            myHands.append(deck.pop())
            flag = "O"
        else:
            otherHands.append(deck.pop())
            flag = "M"

    dummy.append(deck.pop())
    top.append(dummy[0][0])
    top.append(dummy[0][1])
    col = top[1]


def start():
    global winFlag

    while winFlag == 0:
        chooseCard()
        winFlag = 1


def chooseCard():
    global turn
    num = 0

    os.system("clear")
    hands = myHands if turn.__eq__("M") else otherHands
    print("Field:", dummy[len(dummy) - 1])
    for i in range(len(hands)):
        print(str(i) + ".", str(hands[i][0]) + str(hands[i][1]))
    print()

    print( "Card left:" + str(len(deck)), "Attack Stack:" + str(attackStack), turn, "Dummy:"+(str(len(dummy))),"MyHand:"+(str(len(myHands))),"OtherHand:"+(str(len(otherHands))))
    print()

    print("Choose your card(number) or grab a card(99): ", end="")
    try:
        num = int(input())
    except ValueError:
        chooseCard()

    if num >= len(hands) and num != 99:
        print("Plz pick again...")
        sleep(1)
        chooseCard()
        return

    if attackStack == 0:
        if num == 99:
            addCard(hands, 1)
            setTurn()
            chooseCard()
            return
    else:
        if num == 99:
            addCard(hands, attackStack)
            setTurn()
            chooseCard()
            return
        elif not (hands[num][0].__eq__("A") or hands[num][0].__eq__("2") or hands[num][0].__eq__("3") or
                  hands[num][0].__eq__("Joker")):
            print("Plz pick again...")
            sleep(1)
            chooseCard()
            return

    card = hands[num]
    check = checkCard(card, hands)
    if check == 1:
        submitCard(card, hands)
        setTurn()
        chooseCard()


def setTurn():
    global turn
    turn = "O" if turn.__eq__("M") else "M"


def checkCard(card, hands):
    global attackStack
    global col

    if col.__eq__(card[1]) or top[0].__eq__(card[0]) or (
            (card[0].__eq__("Joker") or top[0].__eq__("Joker")) and color[col].__eq__(color[card[1]])):
        if (card[0].__eq__("A") and card[1].__eq__("S")) or card[0].__eq__("Joker"):
            attackStack += 5
        elif card[0].__eq__("2"):
            attackStack += 2
        elif card[0].__eq__("3"):
            attackStack = 0
        elif card[0].__eq__("7"):
            setColor()
            return 1
        elif card[0].__eq__("A"):
            attackStack += 3
        elif card[0].__eq__("Joker") and card[1].__eq__("Color"):
            attackStack += 7
        elif card[0].__eq__("K") or card[0].__eq__("J"):
            submitCard(card, hands)
            col = card[1]
            chooseCard()
            return
        col = card[1]
        return 1
    else:
        print("You can't do it.")
        sleep(1)
        chooseCard()
        return 0


def setColor():
    global col
    print("Choose Sign: ", end="")
    c = str(input())
    if col.__eq__("S") or col.__eq__("H") or col.__eq__("C") or col.__eq__("D"):
        col = c
    else:
        print("Wrong sign")
        setColor()


def submitCard(card, hands):
    dummy.append(card)
    hands.remove(card)
    setTop()

    if len(hands) == 0:
        os.system("clear")
        print(turn + " win.")
        sys.exit(0)


def addCard(hands, num):
    global attackStack
    attackStack = 0
    for i in range(num):
        if len(deck) == 0:
            reset()
        hands.append(deck.pop())
    if len(hands) >= 26:
        os.system("clear")
        print(turn + " lose.")
        sys.exit(0)


def reset():
    temp = dummy[len(dummy) - 1]
    while len(dummy) != 0:
        deck.append(dummy.pop())

    for i in range(10):
        os.system('clear')
        print("Shuffle"+("." * int(i / 3)),len(dummy))
        random.shuffle(deck)
        sleep(0.5)
    dummy.append(temp)


def setTop():
    top.clear()
    top.append(dummy[len(dummy) - 1][0])
    top.append(dummy[len(dummy) - 1][1])


if __name__ == "__main__":
    setting()
    start()
