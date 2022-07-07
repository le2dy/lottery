import random
import os
from time import sleep

maxCount = 6
cnt = 0

print("How many lotteries want to buy?")
print('Input: ', end='')
a = input()

numbers = [[0 for j in range(6)] for i in range(int(a))]

for j in range(int(a)):
    for i in range(len(numbers[j])):
        num = random.randrange(1, 45)
        if(num in numbers):
            numbers[j].remove(num)
        numbers[j][i] = num
        os.system('clear')
        print(numbers[j][i])
        sleep(1)

os.system('clear')
print("Today's lottery number is")

for i in numbers:
    i.sort()
    print(i)

print("Good luck!")
