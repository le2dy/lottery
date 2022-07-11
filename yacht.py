import os
import random
from time import sleep
from collections import Counter

category = ['Ones', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes', 'Choice', '4 of a Kind', 'Full House', 'Small Straight', 'Big Straight', 'Yacht']
scores = [[0 for i in range(len(category))] for j in range(2)]
scores_check = [[0 for i in range(len(category))] for j in range(2)]
turn = 0
names = []
chance = 3
dices = [1 for i in range(5)]
dice_fixed = [0 for i in range(5)]
isRecord = 0


def set_board():
  os.system('clear')

  print('',names[0], names[1])
  for i in range(len(category)):
    print(category[i], scores[0][i], scores[1][i])
  print('total', sum(scores[0]), sum(scores[1]))
  
  print()

  for i in range(len(dices)):
    print(dices[i], end=' ')
  print()
  print()
  CLI()

def CLI():
  global isRecord
  
  cmd = input(names[turn] + '> ')

  if cmd.__eq__('roll'):
    if chance == 0:
      print("You have no more chance to reroll.")
    else:
      roll_dices()
  elif cmd.__eq__('record'):
    if chance == 0:
      print("You have no more chance to reroll.")
      CLI()
      return
    if chance == 3:
      print("You can't do that.")
      CLI()
      return
    isRecord = 1
    for i in range(len(category)):
      print(str(i + 1)+'. ' + category[i])
    print('13. Back')
  elif cmd.__eq__('hold'):
    print(dice_fixed)
    msg = input('Choose the dices.\n> ')
    choosen = msg.split(' ')
    try:
      for i in range(len(choosen)):
        dice_fixed[int(choosen[i]) - 1] = 1 if dice_fixed[int(choosen[i]) - 1] == 0 else 0
    except ValueError:
      print('Insert as number.')
      CLI()
  elif cmd.__eq__('help'):
    print('roll: Roll the dices.')
    print('record: Record the score.')
    print('help: print command list and description.')
    print('hold: Hold the selected dice. ex) 1 : Hold 1st dice, 1 4 5 : Hold 1st, 4th, 5th dice.')
  else:
    if isRecord:
      try:
        record(cmd)
      except ValueError:
        CLI()
    else:
      print(cmd+": command not found")
      sleep(0.5)
  CLI()


def record(cmd):
  global scores
  global isRecord
  global dices
  score = 0

  if 1 <= int(cmd) <= 6:
    score = int(cmd) * int(dices.count(int(cmd)))
  elif cmd.__eq__('7'):
    for i in range(dices):
      score += int(dices[i])
  elif cmd.__eq__('8'):
    for i in range(1, 7):
      if dices.count(i) >= 4:
        score = i * int(dices.count(i))
  elif cmd.__eq__('9'):
    counter = Counter(dices).most_common(2)
    v1 = counter[0][1]
    v2 = counter[1][1]
    if v1 == 5:
      score = counter[0][0] * 5
    elif (v1 == 3 and v2 == 2):
      score = (counter[0][0] * 3) + (counter[1][0] * 2)
  elif cmd.__eq__('10'):
    sorted = dices
    sorted.sort()
    cnt = 0
    for i in range(len(sorted) - 1):
      if sorted[i] + 1 == sorted[i + 1]:
        cnt += 1
    if cnt == 3:
      score = 15
  elif cmd.__eq__('11'):
    sorted = dices
    sorted.sort()
    cnt = 0
    for i in range(len(sorted) - 1):
      if sorted[i] + 1 == sorted[i + 1]:
        cnt += 1
    if cnt == 4:
      score = 30
  elif cmd.__eq__('12'):
    for i in range(1, 7):
      if dices.count(i) == 5:
        score = 30
  elif cmd.__eq__('13'):
    isRecord = 0

  yn = input("Are you sure to record " + str(score) + " at " + category[int(cmd) - 1]+"?(Y/N)\n> ")

  if yn.__eq__('Y'):
    if scores_check[turn][int(cmd) - 1] == 1:
      print('You already checked.')
      CLI()
    else:
      scores[turn][int(cmd) - 1] = score
      scores_check[turn][int(cmd) - 1] = 1
      end_check()
  else:
    CLI()
  set_turn()


def end_check():
  for i in range(len(scores)):
    for j in range(len(scores[i])):
      if scores_check[i][j] == 0:
        return
  end_of_game()


def end_of_game():
  p1 = sum(scores[0])
  p2 = sum(scores[1])
  if p1 > p2:
    winner = names[0]
  elif p1 == p2:
    winner = "draw"
  else:
    winner = names[1]
  comments = ['The game is finished.', "Let's check the final score.", 'Final score is...', str(p1)+":"+str(p2),"Winner is " + winner+"!","Congratulation!"]

  for i in range(len(comments)):
    os.system('clear')
    print(comments[i])
    sleep(1)


def set_turn():
  global turn
  global chance
  global dices
  global dice_fixed
  
  turn = 1 if turn == 0 else 0
  chance = 3
  dices = [1 for i in range(5)]
  dice_fixed = [0 for i in range(5)]
  
  set_board()


def roll_dices():
  global chance
  
  for i in range(len(dices)):
    if dice_fixed[i] == 0:
      dices[i] = random.randint(1, 6)
  chance -= 1
  set_board()


def start():
  for i in range(3, 0, -1):
    os.system('clear')
    print("Game start in... " + str(i))
    sleep(1)
  set_board()
    

if __name__.__eq__('__main__'):
  for i in range(2):
    name = input('Enter your name: ')
    names.append(name)
  start()
