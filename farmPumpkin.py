from mainClass import MainClass
import subprocess
from time import sleep
import random
from ahk import AHK

MainClass.moveTerminal()
race = input("\t1 - Elf\n\t2 - Orc\n\t3 - Dead\n\t4 - Human\n\t5 - Dwarf\nSellect race: ")
location = input("\t  1 - Bats\n\t  2 - Pumpkins\nSellect location: ")
ch = MainClass(race, 0)
ch.savePID()
routes = {
    "routeAoFLeft": ((18, 31), (22, 17), (22, 18), (22, 19), (25, 28), (26, 38), (23, 47), (11, 45), (2, 36), (5, 25), (6, 13), (17, 6), (28, 10), (40, 7), (47, 18), (46, 28), (44, 35), (47, 45), (36, 43), (26, 36)),
    "routeAoFRight": ((25, 27), (25, 22), (22, 17), (17, 21), (17, 34), (28, 44), (38, 48), (47, 38), (43, 28), (46, 17), (46, 4), (35, 5), (24, 7), (12, 9), (2, 18), (3, 28), (2, 36), (14, 46), (19, 39)),
    "routeAoFCloud": ((23, 45), (35, 48), (47, 47), (47, 36)),
    "routePumpkin1": ((2, 22), (11, 15), (18, 10), (25, 12), (27, 10), (30, 14), (39, 13), (43, 22), (42, 30), (38, 37), (34, 33), (26, 39), (21, 36), (19, 37), (17, 39), (14, 35), (7, 35), (2, 31)),
    "routePumpkin2": ((7, 31), (14, 34), (21, 35), (25, 41), (27, 34), (32, 36), (35, 32), (36, 39), (40, 36), (43, 29), (40, 21), (39, 14), (34, 17), (30, 14), (27, 17), (23, 12), (18, 15), (12, 12), (8, 18), (4, 26))
}
currentRoute = random.choice(("routeAoFLeft", "routeAoFRight"))
if location == "2":
    currentRoute = random.choice(("routePumpkin1", "routePumpkin2"))
lap, side, fails = 0, "1", 0

ch.relogin()
process = subprocess.Popen(['py', 'walkClanMessages.py'])
ch.activate()
if ch.checkInTheCity():
    if ch.defineTheCityImage('AbodeOfFear'):
        ch.leaveTheCity()
        ch.startMove()
        if location == "2":
            ch.followTheRoutePumpkin(routes["routeAoFCloud"])
            ch.crossToNextMap(49, 29)
            ch.startMove()
        while True:
            ftr = ch.followTheRoutePumpkin(routes[currentRoute], collect = True)
            if ftr:
                fails, lap = 0, lap + 1
                ch.send_message(f"LAP {lap}", token=ch.token2)
            else:
                fails, lap = fails + 1, lap + 1
                process.terminate()
                ch.relogin()
                process = subprocess.Popen(['py', 'walkClanMessages.py'])
                ch.activate()
                if ch.checkInTheCity():
                    if ch.defineTheCityImage('AbodeOfFear'):
                        ch.leaveTheCity()
                        ch.startMove()
                        if location == "2":
                            ch.followTheRoutePumpkin(routes["routeAoFCloud"])
                            ch.crossToNextMap(49, 29)
                            ch.startMove()
                    else:
                        process.terminate()
                        print("ANOTHER CITY")
                        fails += 1
                else:
                    process.terminate()
                    print("NOT IN CITY")
                    fails += 1
            if fails >= 5:
                print("More 5 Fails in the row. Break")
                break
            if lap > 0 and lap % 50 == 0:
                ch.send_message("Change the route", ch.token2)
                if currentRoute == "routeAoFLeft":
                    currentRoute = "routeAoFRight"
                elif currentRoute == "routeAoFRight":
                    currentRoute = "routeAoFLeft"
                elif currentRoute == "routePumpkin1":
                    currentRoute = "routePumpkin2"
                elif currentRoute == "routePumpkin2":
                    currentRoute = "routePumpkin1"
    else:
        process.terminate()
        print("ANOTHER CITY")
else:
    process.terminate()
    print("NOT IN CITY")

ch.send_message("Farm Pumpkin FINISH", ch.token1, timeOut = ch.to1)

try:
    ahk = AHK()
    win = ahk.find_window(title = 'Windows PowerShell')
    if win:
        win.activate()
except Exception as ex:
	print(ex)