import os
import platform

def clear():
    if platform.system() == "Windows":
        return os.system('cls')
    else:
        return os.system('clear')