import os
import sys


def getRelPath(path: str):
    parent = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
    return os.path.join(parent, path)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
        if not os.path.exists(os.path.join(base_path, "data")):
            os.mkdir(os.path.join(base_path, "data"))
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
