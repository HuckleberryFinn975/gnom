from mainClass import MainClass
import subprocess
import time
from time import sleep
import random
from ahk import AHK

MainClass.moveTerminal()
races = "R5 R6 R7 R8 R9 R10".split()
place = input("\t0 - Wizzards\n\t1 - Banshee\n\t2 - Fairy\n\t3 - Ghost\nSelect location: ")
cords = ([(0, 19), (11, 30), (16, 35), (0, 49), (15, 49), (0, 38)], # wizz
    [(1, 1), (25, 1), (17, 10), (3, 11), (12, 7), (13, 2)], # banshee
    [(47, 48), (44, 42), (40, 45), (49, 38), (48, 32), (35, 45)], # fairy
    [(5, 47), (8, 38), (20, 39), (28, 48), (27, 39), (17, 48)] # ghosts
    )
for k in range(7):
    ch = MainClass(races[k], flead="9999")
    ch.relogin()
    ch.activate()
    if ch.checkInTheCity():
        if ch.leaveTheCity():
            if ch.startMove(firstKey='left'):
                if place in "012":
                    if ch.crossToNextMap(49, 34):
                        if ch.startMove(firstKey='right'):
                            if place == '0':
                                pass
                            elif place in '12':
                                ch.crossToNextMap(7, 49)
                                ch.startMove()
                                ch.followTheRoute(((2, 14), (8, 26), (9, 38)))
                                ch.crossToNextMap(13, 49)
                                ch.startMove()
                                if place == '2':
                                    ch.crossToNextMap(0, 8)
                                    ch.startMove()
                                    ch.followTheRoute(((46, 19), (42, 31), (33, 41), (21, 47), (8, 43)))
                                    ch.crossToNextMap(0, 45)
                                    ch.startMove(firstKey = 'left')
                else:
                    ch.moveOnMap(37, 38)
                    ch.crossToNextMap(34, 49)
                    ch.startMove(firstKey = 'left')
                    ch.followTheRoute(((20, 5), (7, 6)))
                    ch.crossToNextMap(0, 5)
                    ch.startMove(firstKey = 'left')
                    ch.followTheRoute(((35, 3), (22, 3)))
                    ch.crossToNextMap(17, 0)
                    ch.startMove(firstKey = 'up')
                ch.moveOnMap(cords[int(place)][k][0], cords[int(place)][k][1])
                ch.statsFunc()
                ch.hideResp()

try:
    ahk = AHK()
    win = ahk.find_window(title = 'Windows PowerShell')
    if win:
        win.activate()
except Exception as ex:
	print(ex)