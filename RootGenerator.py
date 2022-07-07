import random

stage = 1
stages = []
ways = []


def setLoads():
    global stage
    global stages

    for i in range(1, depth):
        rand = random.randrange(1, 4)
        stages.append(rand)
        for j in range(rand):
            stage += 1
            miniMap[i][j] = stage


def setWay():
    global ways

    for i in range(len(miniMap)):
        if i + 1 != len(miniMap):
            if stages[i] == 1:
                if stages[i + 1] == 1:
                    ways.append("|")
                elif stages[i + 1] == 2:
                    ways.append("/ \\")
                else:
                    ways.append("/ | \\")
            elif stages[i] == 2:
                if stages[i + 1] == 1:
                    ways.append("\\ /")
                elif stages[i + 1] == 2:
                    ways.append("|  |")
                else:
                    a = random.randrange(0, 3)
                    if a == 0:
                        ways.append("| / |")
                    elif a == 1:
                        ways.append("|\\ |")
                    else:
                        ways.append("|\\/|")
            else:
                if stages[i + 1] == 1:
                    ways.append("\\ | /")
                elif stages[i + 1] == 2:
                    a = random.randrange(0, 3)
                    if a == 0:
                        ways.append("| / |")
                    elif a == 1:
                        ways.append("| \\ |")
                    else:
                        ways.append("| /\\ |")
                else:
                    ways.append("| | |")


if __name__ == '__main__':
    print("Insert depth: ")
    depth = int(input())
    miniMap = [[0 for i in range(3)] for j in range(depth)]
    miniMap[0][0] = stage
    stages.append(1)
    setLoads()
    setWay()
    for i in range(len(ways)):
        if stages[i] == 1:
            print("", miniMap[i][0], "")
        elif stages[i] == 2:
            print(miniMap[i][0], "", miniMap[i][1])
        else:
            print(miniMap[i][0], miniMap[i][1], miniMap[i][2])
        print(ways[i])
    if stages[4] == 1:
        print("", miniMap[4][0], "")
    elif stages[4] == 2:
        print(miniMap[4][0], "", miniMap[4][1])
    else:
        print(miniMap[4][0], miniMap[4][1], miniMap[4][2])
