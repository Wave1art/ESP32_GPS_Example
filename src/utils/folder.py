import os

def mkdir_if_not_exist(path):
    try:
        os.mkdir(path)
    except OSError:
        pass