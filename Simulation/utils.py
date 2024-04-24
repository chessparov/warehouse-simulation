import os


def getRelPath(path: str):
    parent = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
    return os.path.join(parent, path)
