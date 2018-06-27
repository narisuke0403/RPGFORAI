import numpy as np
import random
import copy
import sys
import csv
sys.setrecursionlimit(10000)

#基本的なステータス用クラス

class Character:
  def __init__(self,name,hp,mp,power,armor,notInsimulate,*args, **kwargs):
    self.name = name
    self.hp = hp
    self.MAXHP = hp
    self.mp = mp
    self.power = power
    self.armor = armor
    self.MAXARMOR = armor
    self.notInsimulate = notInsimulate
    self.live = True
    self.move = False

  #攻撃
  def Attack(self,target):
    damage = int((self.power ) -target.armor * random.uniform(0.9, 1.1))
    target.hp -= damage
    self.move = True
    if self.notInsimulate:
      print("{}が{}に通常攻撃--{}のダメージ".format(self.name,target.name,damage))
  
  #スキル攻撃
  def Skill1(self,target):
    if(self.mp >= 10):
      damage = int(self.power *1.5 - target.armor * random.uniform(0.9, 1.1))
      target.hp -= damage
      self.mp -= 10
      self.move = True
      if self.notInsimulate:
        print("{}が{}にスキル1攻撃--{}のダメージ".format(self.name, target.name, damage))
    else:
      if self.notInsimulate:
        print("MPが不足している")
      self.Attack(target)
  
  #回復
  def Heal(self,target):
    if(self.mp >= 10):
      damage = target.MAXHP/10 * 5
      target.hp += damage
      if target.hp > target.MAXHP:
        target.hp = target.MAXHP
      self.move = True
      if self.notInsimulate:
        print("{}が{}を回復--{}の回復".format(self.name, target.name, damage))
    else:
      if self.notInsimulate:
        print("MPが不足している")
      self.Attack(target)

#Q学習用
def SimulateInQ(player,npc,enemy,Qtable):
  alpha = 0.5
  characterlist = [player, npc, enemy]
  random.shuffle(characterlist)
  my = [player,npc]
  opp = [enemy]
  temp = CheckSituation(player,npc,enemy)
  for i in characterlist:
    i.notInsimulate = False
    while i.move == False and i.live == True:
      if i == npc:
        choice = np.argmax(Qtable[temp])
        if choice == 0:
          i.Attack(enemy)
        elif choice == 1:
          i.Skill1(enemy)
          if i.mp < 10:
            choice = 0
        elif choice == 2:
          i.Heal(player)
          if i.mp < 10:
            choice = 0
      else:
        if i in my:
          i.Attack(enemy)
        else:
          i.Attack(random.choice(my))
    i.move = False
    if player.hp <= 0 or enemy.hp <= 0:
      if temp > 16*3 and player.hp >= 0:
        return 100
      else:
        return -100
    elif npc.hp <= 0:
      npc.live = False
  temp_next = CheckSituation(player,npc,enemy)
  score = SimulateInQ(player, npc, enemy,Qtable)
  if npc.live:
    Qtable[temp][choice] = (1-alpha) * Qtable[temp][choice] + alpha * (score + Qtable[temp_next][np.argmax(Qtable[temp_next])])
  return score
  
#状況を離散化
def CheckSituation(player,npc,enemy):
  st = ""
  li = [player,npc,enemy]
  for i in li:
    if i.hp > i.MAXHP / 4 * 3:
      st += "0"
    elif i.hp > i.MAXHP / 2:
      st += "1"
    elif i.hp > i.MAXHP / 4:
      st += "2"
    else:
      st += "3"
  return int(st,4)

#一ターンの流れ
def flow():
  player = Character('Player', 300, 40, 60, 15,True)
  npc = Character('NPC', 340, 40, 50, 10, True)
  enemy = Character('Enemy', 700, 100, 75, 20, True)
  my = [player, npc]
  opp = [enemy]
  simulatenum = 1000
  line = 4*4*4
  Qtable = np.zeros((line,3))
  history = []
  while player.hp > 0 and enemy.hp > 0:
    for i in range(simulatenum):
      SimulateInQ(copy.deepcopy(player), copy.deepcopy(npc), copy.deepcopy(enemy),Qtable)
    characterlist = [player, npc, enemy]
    random.shuffle(characterlist)
    temp = CheckSituation(player,npc,enemy)
    for i in characterlist:
      while i.move == False and i.live == True:
        if i == npc:
          choice = np.argmax(Qtable[temp])
          if choice == 0:
            i.Attack(enemy)
          elif choice == 1:
            i.Skill1(enemy)
            if i.mp < 10:
              choice = 0
          elif choice == 2:
            i.Heal(random.choice(my))
            if i.mp < 10:
              choice = 0
          history.append(choice)
        else:
          if i in my:
            i.Attack(enemy)
          else:
            i.Attack(random.choice(my))
        if player.hp <= 0 or enemy.hp <= 0:
          break
        elif npc.hp <= 0:
          npc.live = False
      i.move = False
  if player.hp >= 0:
    print("win")
  else:
    print("lose")
  with open("history.csv", "w+") as f:
      writer = csv.writer(f, lineterminator='\n')
      writer.writerow(history)     

def main():
  flow()

if __name__ == '__main__':
  main()