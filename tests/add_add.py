from filehelper import *

def setup():
    pass

def change1():
    write('file', '1')

def change2():
    write('file', '2')

def getWinningChange(): # 0: neither won, 1/2: 1/2 won
    result = read('file')
    if result == "1": return 1
    if result == "2": return 2
    return 0
