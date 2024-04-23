import os


def getRelPath(path: str):
    return os.path.join(os.path.dirname(os.getcwd()), path)
