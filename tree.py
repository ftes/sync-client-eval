import os, re, time, sys
import filehelper

def tree(startpath):
    lines = []
    for root, dirs, files in os.walk(startpath):
        basename = os.path.basename(root)
        if filehelper.exclude.match(basename):
                continue
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        lines.append('{}{}/'.format(indent, basename))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if filehelper.exclude.match(f):
                continue
            with open(os.path.join(root, f), 'r') as d:
                lines.append('{}{}: {}'.format(subindent, f, d.read()))
    return "\n".join(lines)

def printTreeAndRefresh(startpath, interval=1):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(tree(startpath))
        time.sleep(interval)
        
if __name__ == "__main__":
    printTreeAndRefresh(*sys.argv[1:])
