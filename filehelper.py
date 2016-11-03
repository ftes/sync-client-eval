import os, shutil, re

exclude = re.compile('^(\..*)|(desktop\.ini)$')

def mkdir(path):
    try:
        os.makedirs(path)
    except OSError:
        pass

def append(path, data):
    write(path, data, "a")

def write(path, data, mode="w"):
    # create directory if necessary
    directory = os.path.dirname(path)
    mkdir(directory)

    # write
    with open(path, "a") as f:
        f.write(data)

def clean(path):
    mkdir(path)
    for child in os.listdir(path):
        # do not delete excluded items
        if exclude.match(child):
            continue
        childPath = os.path.join(path, child)
        if os.path.isfile(childPath):
            os.remove(childPath)
        else:
            shutil.rmtree(childPath)
