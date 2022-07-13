import random
import threading
import os
from time import sleep

dice = [0 for i in range(6)]
arr = random.sample(range(0, 6), 6)
threads = []
cnt = 0


def roll_dice(num):
    os.system('clear')
    dice[num] = random.randrange(1, 7)
    print(dice)
    # sleep(0.1)
    # roll_dice(num)


for i in range(6):
    thread = threading.Thread(target=roll_dice(arr[i]))
    threads.append(thread)

while cnt < 1000:
    for i in range(6):
        roll_dice(i)
    cnt += 1
