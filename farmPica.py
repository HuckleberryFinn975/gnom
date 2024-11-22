from mainClass import MainClass
import subprocess
import time
from time import sleep
import random
from ahk import AHK

MainClass.moveTerminal()
race = input("\t1 - Elf\n\t2 - Orc\n\t3 - Dead\n\t4 - Human\n\t5 - Dwarf\nSelect race: ")
bagSize = input("  Enter your bag size (Default = 35): ")
if bagSize.isdigit():
    bagSize = int(bagSize)
else:
    print("  The bag size is incorrect. Use default")
    bagSize = 35 
ch = MainClass(race, 0)
ch.savePID()
point, timeUntilRestart = "right", 600

routePica1 = (18, 17), (16, 7)
routePica2 = (23, 21), (26, 17)
routePica3 = (28, 20), (31, 13)
ch.relogin()
farmStartTime = time.time()
process = subprocess.Popen(['py', 'walkClanMessages.py'])
ch.activate()
if ch.checkInTheCity():
    if ch.defineTheCityImage('Picathron'):
        def checkBagAndGo(notCheck = False):
            if notCheck:
                ch.emptyBackpack(bagSize = bagSize)
            else:
                bgfull = ch.bagFullness(bagSize = bagSize)
                if bgfull == 'FULL':
                    ch.outOfCharacter()
                    ch.emptyBackpack(bagSize = bagSize)
                elif bgfull == 'NOTFULL':
                    ch.outOfCharacter()
            ch.leaveTheCity()
            ch.startMove(firstKey='up')
            ch.followTheRoutePumpkin(random.choice((routePica1, routePica2, routePica3)))
        
        checkBagAndGo()
        lap, side, fails = 0, "1", 0
        while True:
            if lap > 0 and lap % 66 == 0:
                print("Change the way")
                if side == '1':
                    print("SWITCH SIDE ON 2")
                    side = '2'
                elif side == '2':
                    print("SWITCH SIDE ON 3")
                    side = '3'
                elif side == '3':
                    print("SWITCH SIDE ON 1")
                    side = '1'
            if lap > 0 and lap % 7 == 0:
                bgfull = ch.bagFullness(bagSize = bagSize)
                if bgfull == 'FULL':
                    process.terminate()
                    ch.relogin()
                    farmStartTime = time.time()
                    process = subprocess.Popen(['py', 'walkClanMessages.py'])
                    ch.activate()
                    if ch.checkInTheCity():
                        if ch.defineTheCityImage('Picathron'):
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
                sleep(1)
            elif farmGold == "FailedBattle":
                fails += 1 
                lap += 1
            if time.time() > farmStartTime + timeUntilRestart:
                ch.send_message("More than 10 minutes without restart", ch.token2)
                ch.relogin()
                farmStartTime = time.time()
            if fails >= 15:
                ch.send_message("MORE 15 FAILS | sleep 60 sec", ch.token1, timeOut = ch.to1)
                sleep(60)
                process.terminate()
                ch.relogin()
                farmStartTime = time.time()
                process = subprocess.Popen(['py', 'walkClanMessages.py'])
                ch.activate()
                if ch.checkInTheCity():
                    if ch.defineTheCityImage('Picathron'):
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