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
    with open(path, mode) as f:
        f.write(data)

def read(path):
    # write
    with open(path, "r") as f:
        return f.read().rstrip()

def clean(path):
    mkdir(path)
    for child in os.listdir(path):
        # do not delete excluded items
        if exclude.match(child):
            continue
        rm(os.path.join(path, child))

def rm(path):
    if os.path.isfile(path):
        os.remove(path)
    else:
        shutil.rmtree(path)

def exists(path):
    return os.path.exists(path)
