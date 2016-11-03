from filehelper import *

def setup():
    mkdir('parent')

def change1():
    write('parent/child', '')

def change2():
    rm('parent')

def getWinningChange(): # 0: neither won, 1/2: 1/2 won
    if exists('parent/child'): return 1
    if not exists('parent'): return 2
    return 0
