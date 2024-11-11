from mainClass import MainClass
import subprocess
from time import sleep
import random
from ahk import AHK

MainClass.moveTerminal()
race = input("\t1 - Elf\n\t2 - Orc\n\t3 - Dead\n\t4 - Human\n\t5 - Dwarf\nSellect race: ")
# location = input("\t  1 - Bats\n\t  2 - Pumpkins\nSellect location: ")
bagSize = input("  Enter your bag size (Default = 35): ")
if bagSize.isdigit():
    bagSize = int(bagSize)
else:
    print("  The bag size is incorrect. Use default")
    bagSize = 35 
ch = MainClass(race, 0)
ch.savePID()

routeTree1A = (30, 3), (19, 4), (13, 4)
routeTree1B = (29, 8), (17, 7), (9, 3)
routeTree2A = (35, 11), (26, 10), (16, 13)
routeTree2B = (32, 14), (23, 8), (11, 11)
routeTree3A = (38, 9), (33, 15), (35, 25), (23, 28), (22, 39), (11, 30), (6, 20), (3, 9)
routeTree3B = (40, 16), (30, 27), (19, 39), (6, 30), (14, 20), (10, 6)
ch.relogin()
process = subprocess.Popen(['py', 'walkClanMessages.py'])
ch.activate()
if ch.checkInTheCity():
    if ch.defineTheCityImage('TreeAbode'):
        def checkBagAndGo(notCheck = False):
            if notCheck:
                ch.emptyBackpack()
            else:
                bgfull = ch.bagFullness(bagSize = bagSize)
                if bgfull == 'FULL':
                    ch.outOfCharacter()
                    ch.emptyBackpack()
                elif bgfull == 'NOTFULL':
                    ch.outOfCharacter()
            ch.leaveTheCity()
            ch.startMove()
            randRoute = random.randint(1, 6)
            if randRoute == 1:
                ch.followTheRoutePumpkin(routeTree1A, unit = "Camel", collect=True)
            elif randRoute == 2:
                ch.followTheRoutePumpkin(routeTree1B, unit = "Camel", collect=True, exactCoors=(17, 7))
            elif randRoute == 3:
                ch.followTheRoutePumpkin(routeTree2B, unit = "Camel", collect=True, exactCoors=(26, 10))
            elif randRoute == 4:
                ch.followTheRoutePumpkin(routeTree2B, unit = "Camel", collect=True, exactCoors=(23, 8))
            elif randRoute == 5:
                ch.followTheRoutePumpkin(routeTree3A, unit = "Camel", collect=True, exactCoors=(6, 20))
            elif randRoute == 6:
                ch.followTheRoutePumpkin(routeTree3B, unit = "Camel", collect=True, exactCoors=(19, 39))
        checkBagAndGo()
        lap, side, fails = 0, "1", 0
        while True:
            if lap > 0 and lap % 7 == 0:
                bgfull = ch.bagFullness(bagSize = bagSize)
                if bgfull == 'FULL':
                    process.terminate()
                    ch.relogin()
                    process = subprocess.Popen(['py', 'walkClanMessages.py'])
                    ch.activate()
                    if ch.checkInTheCity():
                        if ch.defineTheCityImage('TreeAbode'):
                            checkBagAndGo(notCheck = True)
                        else:
                            process.terminate()
                            print("ANOTHER CITY")
                            fails += 1
                    else:
                        process.terminate()
                        print("NOT IN CITY")
                        fails += 1
                elif bgfull == 'NOTFULL':
                    ch.outOfCharacterMap()
            farmGold = ch.farmingGold(magic = False, magnetAngle = side) 
            if farmGold == "Battle":
                lap += 1
                fails = 0
            elif farmGold == "KILLED":
                fails = 0
            elif farmGold == "FAILED":
                fails += 1 
                lap += 1
            elif farmGold == "NOBOTS":
                dx = random.randint(-1, 1)
                if dx == 0:
                    dy = random.randint(-1, 1)
                else:
                    dy = 0
                fails += 1
                ch.moveOnMap(17 + dx, 12 + dy, npcAttack = False)
            elif farmGold == "FailedBattle":
                fails += 1 
                lap += 1
            if fails >= 10:
                ch.send_message("MORE 10 FAILS | sleep 60 sec", ch.token1, timeOut = ch.to1)
                sleep(60)
                process.terminate()
                ch.relogin()
                process = subprocess.Popen(['py', 'walkClanMessages.py'])
                ch.activate()
                if ch.checkInTheCity():
                    if ch.defineTheCityImage('TreeAbode'):
                        checkBagAndGo()
            sleep(.2)
    else:
        process.terminate()
        print("ANOTHER CITY")
else:
    process.terminate()
    print("NOT IN CITY")
ch.send_message("Farm Silk FINISH", ch.token1, timeOut = ch.to1)
process.terminate()

try:
    ahk = AHK()
    win = ahk.find_window(title = 'Windows PowerShell')
    if win:
        win.activate()
except Exception as ex:
	print(ex)