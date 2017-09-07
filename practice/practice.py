import numpy as np
import random
import os.path

#基本的なステータス用クラス
class Status:
    def __init__(self,_name,_hitpoint,_magicpoint,_attack,_defence,player=True,friend=False,enemy=False):
        self.NAME = _name
        self.hitpoint = _hitpoint
        self.MAXHITPOINT = _hitpoint
        self.magicpoint = _magicpoint
        self.MAXMAGICPOINT = _magicpoint
        self.attack = _attack
        self.defence = _defence
        self.movecheck = False
        self.live = True
        self.speed = 0
        self.player = player
        self.friend = friend
        self.enemy = enemy
    def Attack(self,target):
        damage = int((self.attack * random.uniform(0.7,1.3)) - target.defence * random.uniform(0.9,1.1))
        target.hitpoint -= damage
        print('{}が{}に通常攻撃--{}のダメージ'.format(self.NAME,target.NAME,damage))
        if target.hitpoint <= 0 :
            target.hitpoint = 0
            target.live = False
        self.movecheck = True
    def Skill1(self,target):
        if(self.magicpoint >= 10):
            damage = int(self.attack * random.uniform(0.7,1.3) * 1.4 - target.defence * random.uniform(0.9,1.1))
            target.hitpoint -= damage
            print('{}が{}にスキル攻撃--{}のダメージ'.format(self.NAME,target.NAME,damage))
            self.magicpoint -= 10
            if target.hitpoint <= 0 :
                target.hitpoint = 0
                target.live = False
            self.movecheck = True
    def Heal(self,target):
        if(self.magicpoint >= 10):
            print('{}が{}を回復'.format(self.NAME,target.NAME))
            target.hitpoint += int(target.MAXHITPOINT / 10)
            self.magicpoint -= 10
            if(target.hitpoint >= target.MAXHITPOINT):
                target.hitpoint = target.MAXHITPOINT
            self.movecheck = True
    def Choice(self):
        st1 = int(CheckStatus(player,friend,enemy),4)
        t = 0
        for y in data[st1]:
            t += y
        ra = random.randrange(t)
        if ra < data[st1][0]:
            temp = 0
        elif ra < data[st1][0] + data[st1][1]:
            temp = 1
        elif ra < data[st1][0] + data[st1][1] + data[st1][2]:
            temp = 2
        return temp

    def Action(self):
        if self.live == True:
            st1 = int(CheckStatus(player,friend,enemy),4)
            if self.friend == True:
                number = self.Choice()
            elif self.player == True:
                _number = input('0:通常攻撃,1:スキル攻撃,2:自己回復 >>')
                number = int(_number)
            elif self.enemy == True:
                number = 0
            if self.friend == True or self.player == True:
                target = _list[2]
            elif self.enemy == True:
                target = _list[random.randrange(2)]
            if number == 2:
                if self.enemy == True:
                    target = _list[2]
                elif self.friend == True:
                    target = _list[random.randrange(2)]
            if number == 0 :
                self.Attack(target)
            elif number == 1:
                self.Skill1(target)
            elif number == 2:
                self.Heal(target)
            if self.NAME == 'NPC':
                listSt.append(st1)
                listNm.append(number)
def Qsort(li):
    if len(li) < 2:
        return li
    pivot = li[0]
    li_rest = li[1:]
    smaller = [x for x in li_rest if x.speed < pivot.speed]
    larger = [x for x in li_rest if x.speed >= pivot.speed]
    le = Qsort(smaller) + [pivot] + Qsort(larger)
    return  le

def CheckStatus(st1,st2,st3):
    if st1.hitpoint > st1.MAXHITPOINT / 4 * 3:
        st = "0"
    elif st1.hitpoint > st1.MAXHITPOINT / 2:
        st = "1"
    elif st1.hitpoint > st1.MAXHITPOINT / 4:
        st = "2"
    elif st1.hitpoint >= 0:
        st = "3"
    if st1.magicpoint > st1.MAXMAGICPOINT / 4 * 3:
        st += "0"
    elif st1.magicpoint > st1.MAXMAGICPOINT / 2:
        st += "1"
    elif st1.magicpoint > st1.MAXMAGICPOINT / 4:
        st += "2"
    elif st1.magicpoint >= 0:
        st += "3"

    if st2.hitpoint > st2.MAXHITPOINT / 4 * 3:
        st += "0"
    elif st2.hitpoint > st2.MAXHITPOINT / 2:
        st += "1"
    elif st2.hitpoint > st2.MAXHITPOINT / 4:
        st += "2"
    elif st2.hitpoint >= 0:
        st += "3"
    if st2.magicpoint > st2.MAXMAGICPOINT / 4 * 3:
        st += "0"
    elif st2.magicpoint > st2.MAXMAGICPOINT / 2:
        st += "1"
    elif st2.magicpoint > st2.MAXMAGICPOINT / 4:
        st += "2"
    elif st2.magicpoint >= 0:
        st += "3"

    if st3.hitpoint > st3.MAXHITPOINT / 4 * 3:
        st += "0"
    elif st3.hitpoint > st3.MAXHITPOINT / 2:
        st += "1"
    elif st3.hitpoint > st3.MAXHITPOINT / 4:
        st += "2"
    elif st3.hitpoint >= 0:
        st += "3"
    if st3.magicpoint > st3.MAXMAGICPOINT / 4 * 3:
        st += "0"
    elif st3.magicpoint > st3.MAXMAGICPOINT / 2:
        st += "1"
    elif st3.magicpoint > st3.MAXMAGICPOINT / 4:
        st += "2"
    elif st3.magicpoint >= 0:
        st += "3"
    return st

def Flow():
    while 1:
        if player.live == False or enemy.live == False:
            break
        for x in _list:
            x.speed = random.random()
        list1 = Qsort(_list)
        for x in list1:
            if player.live == False or enemy.live == False:
                break
            x.Action()
    if enemy.live == True:
        for x in listSt:
            for y in listNm:
                if(data[x][y] > 1):
                    data[x][y] -= 1
    elif enemy.live == False:
        for x in listSt:
            for y in listNm:
                data[x][y] += 1
    return

def FlowTest():
    while 1:
        if player.live == False or enemy.live == False:
            break
        for x in _list:
            x.speed = random.random()
        list1 = Qsort(_list)
        for x in _list:
            print('{0},{1}'.format(x.hitpoint,x.magicpoint))
        for x in list1:
            if player.live == False or enemy.live == False:
                break
            x.Action()
    return


def DataSave():
    np.save('data.npy',data)
    np.savetxt('data.csv',data)
def DataRead():
    try:
        data = np.load('data.npy')
    except IOError:
        data = np.ones((4096,3))
    return data


data = DataRead()
COUNT = 1000
n = 0
win = 0

choice = int(input('0 : 学習結果 , 1 : 学習 >>'))
if choice == 0:
    #自キャラ
    player = Status('Player',80,40,40,15)
    #味方AI
    friend = Status('NPC',120,50,30,10,False,True)
    #敵キャラ
    enemy = Status('Enemy',350,60,30,20,False,False,True)
    _list = [player,friend,enemy]
    listSt = []
    listNm = []
    FlowTest()
    if enemy.live == False:
        print("WIN")
    elif enemy.live == True:
        print("LOSE")
elif choice == 1:
    while(n < COUNT):
        print("{}回目".format(n))
        #自キャラ
        player = Status('Player',80,40,40,15,False,True)
        #味方AI
        friend = Status('NPC',120,50,30,10,False,True)
        #敵キャラ
        enemy = Status('Enemy',350,60,30,20,False,False,True)
        _list = [player,friend,enemy]
        listSt = []
        listNm = []
        Flow()
        if enemy.live == False:
            win += 1
        n += 1
    DataSave()
    print("勝率:{}%".format(win / COUNT * 100))