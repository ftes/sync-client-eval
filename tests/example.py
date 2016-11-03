from filehelper import *

def setup():
    write('parent/child', '')

def change1():
    write('parent/child', 'A')

def change2():
    write('parent/child', 'B')

def getWinningChange(): # 0: neither won, 1/2: 1/2 won
    return 1
