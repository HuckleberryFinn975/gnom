from mainClass import MainClass
import subprocess
import time
from time import sleep
import random
from ahk import AHK

routes = {
    "route5kPeninsula": ((31, 6), (19, 8), (31, 18)),
    "route5kPeninsula1": ((24, 46), (15, 48), (5, 40)), # exact [15, 48]
    "route5kPeninsula2": ((2, 31), (3, 20), (4, 11), (14, 1), (25, 2)), # exact [2, 31]
    "route5kGreenLake": ((18, 45), (9, 39), (10, 28), (17, 18), (22, 8)),
    "route5kGreenLakeDown": ((24, 43), (18, 46)), # cr{4, 49} fk=right
    "route5kTree": ((16, 5), (28, 7), (40, 14), (45, 20), (41, 32), (39, 41), (28, 46), (16, 44)), # exact [16, 44]
    "unicorn": ((18, 44), (18, 43), (18, 44), (18, 43), (18, 44), (18, 43), (18, 44), (18, 43)),
    "unicornNext": ((18, 44), (18, 45), (18, 44), (18, 45), (18, 46), (18, 45), (17, 45), (18, 45), (17, 45), (16, 45), (17, 45), (16, 45), (15, 45), (16, 45), (16, 46), (16, 45), (16, 46), (16, 47), (16, 46), (16, 47), (16, 48), (16, 47), (16, 48), (16, 49), (16, 48), (16, 49), (17, 49), (16, 49), (15, 49), (16, 49), (15, 49), (14, 49), (15, 49), (14, 49), (13, 49), (14, 49), (13, 49), (12, 49), (13, 49), (12, 49)),
    "shooter": ((35, 18), (36, 18), (35, 18), (36, 18), (35, 18), (36, 18), (35, 18)),
    "shooterNext": ((36, 18), (35, 18), (36, 18), (35, 18), (36, 18), (35, 18), (34, 18), (35, 18), (34, 18), (33, 18), (34, 18), (33, 18), (32, 18), (33, 18), (32, 18), (31, 18), (32, 18), (31, 18), (30, 18), (31, 18), (30, 18), (29, 18), (30, 18), (29, 18), (28, 18), (29, 18), (28, 18), (27, 18), (28, 18), (27, 18), (26, 18), (27, 18), (26, 18), (25, 18), (26, 18), (25, 18), (24, 18), (25, 18), (24, 18), (23, 18), (24, 18), (23, 18), (22, 18), (23, 18), (22, 18), (21, 18), (22, 18), (21, 18), (21, 17), (21, 18), (21, 19), (21, 18), (21, 19), (21, 20), (21, 19), (21, 20), (21, 21), (21, 20), (21, 21), (21, 22), (21, 21), (21, 22), (21, 23), (21, 22), (21, 23), (21, 24), (21, 23), (21, 24), (21, 25), (21, 24), (21, 25), (21, 26), (21, 25), (21, 26), (21, 27), (21, 26), (21, 27), (22, 27), (21, 27), (20, 27), (21, 27), (20, 27), (19, 27), (20, 27), (19, 27), (18, 27), (19, 27), (18, 27), (17, 27), (18, 27), (17, 27), (17, 26), (17, 27), (17, 28), (17, 27), (17, 28), (17, 29), (17, 28), (17, 29), (17, 30), (17, 29), (17, 30))
}

MainClass.moveTerminal()
race = "1"
unicorn, shooter = False, False
npc = input("\t1 - Unicorn\n\t2 - Shooter\n\tNothing - both\nSelect desired NPC: ")
if npc == '1':
    unicorn = True
elif npc == '2':
    shooter = True
else:
    unicorn, shooter = True, True

ch = MainClass(race, flead="9999")
ch.relogin()
ch.activate()
if ch.checkInTheCity():
    if ch.leaveTheCity():
        if ch.startMove(firstKey='left'):
            if unicorn:
                ch.followTheRoute(routes["route5kGreenLakeDown"])
                ch.crossToNextMap(4, 49)
                ch.startMove(firstKey = "right")
                ch.statsFunc()
                ch.activate(terminal = True)
                ch.activate()
                ch.clMessageCheckImage()
                ch.outOfCharacterMap()
                ch.followTheRoute(routes["route5kTree"], exactCoors = (16, 44))
                ch.moveOnMap(18, 43)
                print("sleep 10")
                sleep(10)
                ch.followTheRouteNPC(routes["unicorn"])
                ch.followTheRouteNPC(routes["unicornNext"])
                sleep(5)
                ch.killWindow()
            if shooter and unicorn:
                ch.relogin()
                ch.activate()
                if ch.checkInTheCity():
                    if ch.leaveTheCity():
                        ch.startMove(firstKey='left')
            if shooter:
                ch.followTheRoute(routes["route5kGreenLake"])
                ch.crossToNextMap(30, 0)
                ch.startMove(firstKey = "up")
                ch.statsFunc()
                ch.activate(terminal = True)
                ch.activate()
                ch.clMessageCheckImage()
                ch.outOfCharacterMap()
                ch.followTheRoute(routes["route5kPeninsula1"], exactCoors = (15, 48))
                ch.followTheRoute(routes["route5kPeninsula2"], exactCoors = (2, 31))
                ch.followTheRoute(routes["route5kPeninsula"])
                ch.moveOnMap(36, 19)
                print("sleep 10")
                sleep(10)
                ch.followTheRouteNPC(routes["shooter"])
                ch.followTheRouteNPC(routes["shooterNext"])
                sleep(5)
                ch.killWindow()
            

try:
    ahk = AHK()
    win = ahk.find_window(title = 'Windows PowerShell')
    if win:
        win.activate()
except Exception as ex:
	print(ex)