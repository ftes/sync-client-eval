from filehelper import *

def setup():
    write('parent/child', ' ')

def change1():
    write('parent/child', '1')

def change2():
    rm('parent')

def getWinningChange(): # 0: neither won, 1/2: 1/2 won
    if exists('parent/child') and read('parent/child') == '1': return 1
    if not exists('parent'): return 2
    return 0
