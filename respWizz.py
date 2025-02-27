from mainClass import MainClass
import subprocess
import time
from time import sleep
import random
from ahk import AHK

MainClass.moveTerminal()
races = "R5 R6 R7 R8 R9 R10".split()
cords = ((0, 19), (11, 30), (16, 35), (0, 49), (15, 49), (0, 38))
for k in range(1):
    ch = MainClass(races[k], flead="9999")
    ch.relogin()
    ch.activate()
    if ch.checkInTheCity():
        if ch.leaveTheCity():
            if ch.startMove(firstKey='left'):
                if ch.crossToNextMap(49, 34):
                    if ch.startMove(firstKey='right'):
                        if ch.moveOnMap(cords[k][0], cords[k][1]):
                            ch.statsFunc()
                            ch.hideResp()
try:
    ahk = AHK()
    win = ahk.find_window(title = 'Windows PowerShell')
    if win:
        win.activate()
except Exception as ex:
	print(ex)