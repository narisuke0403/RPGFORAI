import numpy as np
import random
import os.path
import copy
import sys
sys.setrecursionlimit(10000)

#基本的なステータス用クラス

InSimulate = True
class Character:
  def __init__(self,name,hp,mp,power,armor,friend,*args, **kwargs):
    self.name = name
    self.hp = hp
    self.MAXHP = hp
    self.mp = mp
    self.power = power
    self.armor = armor
    self.MAXARMOR = armor
    self.friend = friend
    self.live = True
    self.move = False

  def Attack(self,target):
    damage = int((self.power * random.uniform(0.8, 1.2)) -target.armor * random.uniform(0.9, 1.1))
    target.hp -= damage
    self.move = True
    if InSimulate:
      print("{}が{}に通常攻撃--{}のダメージ".format(self.name,target.name,damage))
  
  def Skill1(self,target):
    if(self.mp >= 10):
      damage = int(self.power * random.uniform(0.8, 1.2) *1.4 - target.armor * random.uniform(0.9, 1.1))
      target.hp -= damage
      self.mp -= 10
      self.move = True
      if InSimulate:
        print("{}が{}にスキル1攻撃--{}のダメージ".format(self.name, target.name, damage))
    else:
      if InSimulate:
        print("MPが不足している")
  
  def Heal(self,target):
    if(self.mp >= 10):
      damage = target.MAXHP/10
      target.hp += damage
      if target.hp > target.MAXHP:
        target.hp = target.MAXHP
      self.move = True
      if InSimulate:
        print("{}が{}を回復--{}の回復".format(self.name, target.name, damage))
    else:
      if InSimulate:
        print("MPが不足している")

def SimulateInQ(player,npc,enemy):
  InSimulate = True
  characterlist = [player, npc, enemy]
  random.shuffle(characterlist)
  my = [player,npc]
  opp = [enemy]
  for i in characterlist:
    while i.move == False and i.live == True:
      if i == npc:
        i.Attack(enemy)
      else:
        if i in my:
          i.Attack(enemy)
        else:
          i.Attack(random.choice(my))
    if player.hp <= 0:
      return -1
    elif enemy.hp <= 0:
      return 1
    elif npc.hp <= 0:
      npc.live = False
    
  SimulateInQ(player, npc, enemy)

def main():
  player = Character('Player', 80, 40, 60, 15,True)
  npc = Character('NPC', 120, 40, 50, 10, True)
  enemy = Character('Enemy', 320, 50, 30, 20, False)
  my = [player, npc]
  opp = [enemy]
  simulatenum = 100
  while player.hp > 0 and enemy.hp > 0:
    for i in range(simulatenum):
      print(i)
      SimulateInQ(copy.deepcopy(player), copy.deepcopy(npc), copy.deepcopy(enemy))
    InSimulate = False
    characterlist = [player, npc, enemy]
    random.shuffle(characterlist)
    for i in characterlist:
      while i.move == False and i.live == True:
        if i == npc:
          i.Attack(enemy)
        else:
          if i in my:
            i.Attack(enemy)
          else:
            i.Attack(random.choice(my))
        if player.hp <= 0 or enemy.hp <= 0:
          break
        elif npc.hp <= 0:
          npc.live = False
  if player.hp >= 0:
    print("win")
  else:
    print("lose")

if __name__ == '__main__':
    main()
    
