import os
from ahk import AHK
import pyautogui
import requests
import random
from time import sleep
from pyautogui import hotkey, click, press
import subprocess
pyautogui.FAILSAFE = False
ahk = AHK()

def terminate_process(process_name):
    try:
        subprocess.run(["taskkill", "/F", "/IM", process_name], check=True)
        print(f"Successfully terminated the process: {process_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to terminate the process: {process_name}. Error: {e}")

def killWindow():
    print("Killing OASIS")
    oasis = ahk.find_window(process=r"C:\Program Files\Java\jdk-21\bin\javaw.exe")
    if oasis:
        print("Found Java, killing | sleep 2...")
        oasis.kill()
    sleep(2)
