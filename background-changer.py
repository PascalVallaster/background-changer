# https://stackoverflow.com/questions/1977694/how-can-i-change-my-desktop-background-with-python
# @Vlad Bezden

import os
import struct
import ctypes
import random
from time import sleep
from os import listdir
from os.path import isfile, join


secure_random = random.SystemRandom()
SPI_SETDESKWALLPAPER = 20
WALLPAPER_PATH = "~null~"


def show_window():
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)


def check_environment():
    if os.path.normpath(os.path.dirname(__file__)) != os.getcwd():
        os.chdir(os.path.normpath(os.path.dirname(__file__)))

    if not os.path.isfile("data.json"):
        show_window()
        print(f"No such file named 'data.json'!\nCurrent working directory: {os.getcwd()}")
        input("Press any key to exit")
        exit()

    data = eval(open("data.json", "r").read())
    _root = os.path.normpath(data["root"])

    if not _root:
        print("Root-Path is empty. Creating new one...")
        data["root"] = os.path.normpath(os.path.dirname(__file__))
        _root = data["root"]
        open("data.json", "w").write(str(data))
    elif os.path.normpath(os.path.dirname(__file__)) != _root:
        show_window()
        print("Unable to load current app path! Maybe the application was moved to a different location?")
        while True:
            choice = input("Do you want to change the app path to the current working directory? [y/N]:")
            if choice not in ["y", "N"]:
                continue
            elif choice == "y":
                data["root"] = os.path.normpath(os.path.dirname(__file__))
                new_previous = os.path.normpath(data["previous"]).split(os.sep)[-2:]
                new_previous = data["root"] + os.sep + os.sep.join(new_previous)
                data["previous"] = new_previous
                break
            else:
                print("Exited cleanly.")
                sleep(2)  # To read the text
                exit()
        open("data.json", "w").write(str(data))
    elif not os.path.isdir(_root + os.sep + "wallpapers"):
        show_window()
        print("Unable to locate folder 'wallpapers'! Maybe it was deleted?")
        while True:
            choice = input("Do you want to re-create the folder? [y/N]:")
            if choice not in ["y", "N"]:
                continue
            elif choice == "y":
                os.mkdir("wallpapers")
                print("The folder 'wallpapers' is empty! See README.md > Usage > Adding images")
                input("Press any key to exit")
                exit()
            else:
                print("Exited cleanly.")
                sleep(2)  # To read the text
                exit()

    if os.path.normpath(os.getcwd()) != _root:
        os.chdir(_root)


def check_wallpapers(_wallpapers):
    if len(_wallpapers) < 2:
        exit()


def get_latest():
    data = eval(open("data.json", "r").read())
    previous = data["previous"]
    root = data["root"]
    wallpapers = [root + os.sep + "wallpapers" + os.sep + f for f in listdir("wallpapers") if isfile(join("wallpapers", f))]
    check_wallpapers(wallpapers)
    while True:
        _wallpaper = secure_random.choice(wallpapers)
        if _wallpaper == previous:
            continue
        else:
            data["previous"] = _wallpaper
            open("data.json", "w").write(str(data))
            return _wallpaper


def is_64_windows():
    """ Find out how many bits is OS. """
    return struct.calcsize('P') * 8 == 64


def get_sys_parameters_info():
    """ Based on if this is 32bit or 64bit returns correct version of SystemParametersInfo function. """
    return ctypes.windll.user32.SystemParametersInfoW if is_64_windows() \
        else ctypes.windll.user32.SystemParametersInfoA


def change_wallpaper():
    sys_parameters_info = get_sys_parameters_info()
    r = sys_parameters_info(SPI_SETDESKWALLPAPER, 0, WALLPAPER_PATH, 3)
    if not r:
        show_window()
        print("An error occurred while changing the background")
        print(ctypes.WinError())
        input("Press any key to exit")
        exit()


if __name__ == '__main__':
    check_environment()
    WALLPAPER_PATH = get_latest()
    change_wallpaper()
