from mainClass import MainClass
import subprocess
from time import sleep
import random

log_file_path = "logOasis.txt"
with open(log_file_path, 'w') as file:
	file.close()
try:
	subprocess.run('wmctrl -r "osboxes@" -e 0,1050,0,400,900', shell=True, check=True)
	sleep(3)
except Exception as ex:
	print(ex)

ch = MainClass("2", 0)

routeTree1A = (30, 3), (19, 4), (13, 4)
routeTree1B = (29, 8), (17, -7), (9, 3)
routeTree2A = (35, 11), (26, -10), (16, 13)
routeTree2B = (32, 14), (23, -8), (11, 11)
routeTree3A = (38, 9), (33, 15), (35, 25), (23, 28), (22, 39), (11, 30), (6, -20), (3, 9)
routeTree3B = (40, 16), (30, 27), (19, -39), (6, 30), (14, 20), (10, 6)
routePica1 = (18, 17), (16, 7)
routePica2 = (23, 21), (26, 17)
routePica3 = (28, 20), (31, 13)
ch.relogin()
process = subprocess.Popen(['python3', 'walkClanMessages.py'])
ch.activate()
if ch.checkInTheCity():
    if ch.defineTheCity() == 'Picathron':
        bgfull = ch.bagFullness(bagSize = 35)
        if bgfull == 'FULL':
            ch.outOfCharacter()
            ch.emptyBackpack()
        elif bgfull == 'NOTFULL':
            ch.outOfCharacter()
        ch.leaveTheCity()
        ch.startMove()
        ch.followTheRoute(random.choice((routePica1, routePica2, routePica3)))
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
                bgfull = ch.bagFullness(bagSize = 35)
                if bgfull == 'FULL':
                    process.terminate()
                    ch.relogin()
                    process = subprocess.Popen(['python3', 'walkClanMessages.py'])
                    ch.activate()
                    if ch.checkInTheCity():
                        if ch.defineTheCity() == 'Picathron':
                            ch.emptyBackpack()
                            ch.leaveTheCity()
                            ch.startMove()
                            ch.followTheRoute(routePica1)
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
            if fails >= 10:
                ch.send_message("MORE 10 FAILS | sleep 60 sec", ch.token1, timeOut = ch.to1)
                sleep(60)
                process.terminate()
                ch.relogin()
                process = subprocess.Popen(['python3', 'walkClanMessages.py'])
                ch.activate()
                if ch.defineTheCity() == 'Picathron':
                    bgfull = ch.bagFullness(bagSize = 35)
                    if bgfull == 'FULL':
                        ch.outOfCharacter()
                        ch.emptyBackpack()
                    elif bgfull == 'NOTFULL':
                        ch.outOfCharacter()
                    ch.leaveTheCity()
                    ch.startMove()
                    ch.followTheRoute(random.choice((routePica1, routePica2, routePica3)))
            sleep(.2)
ch.send_message("Farm Silk FINISH", ch.token1, timeOut = ch.to1)
process.terminate()


try:
    subprocess.run('wmctrl -a "osboxes@"', shell=True, check=True)
    sleep(3)
except Exception as ex:
    print(ex)
    