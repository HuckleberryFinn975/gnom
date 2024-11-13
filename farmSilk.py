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
point = "right"
routeTree1A = (30, 3), (19, 4), (13, 4)
routeTree1B = (29, 8), (17, 7), (12, 2)
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
            randRoute = random.randint(1, 2)
            if randRoute == 1:
                ch.followTheRoutePumpkin(routeTree1A, unit = "Camel", collect=True)
            elif randRoute == 2:
                ch.followTheRoutePumpkin(routeTree1B, unit = "Camel", collect=True, exactCoors=(17, 7))
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
                fails += 1
                if point == 'left':
                    ch.moveOnMap(21, 10, npcAttack = False)
                    point = 'right'
                elif point == 'right':
                    ch.moveOnMap(13, 5, npcAttack = False)
                    point = 'left'
                sleep(.5)
            elif farmGold == "FailedBattle":
                fails += 1 
                lap += 1
            if fails >= 25:
                ch.send_message("MORE 25 FAILS | sleep 20 sec", ch.token1, timeOut = ch.to1)
                sleep(20)
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