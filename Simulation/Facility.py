import Variables as v
import uuid
import numpy as np
from collections import defaultdict
import time
import datetime
import pandas as pd
from pathlib import Path


class ExceptInvaliditem(Exception):
    """

       Defines the Exception class that is raised when a not-existing item is requested

    """

    def __init__(self, *args):
        super().__init__(self, *args)

    def __str__(self):
        return f"Invalid Item! The item doesn't currently exist. "


class TItem:
    """

    Defines the stored object. Contains info on the name, code, and position

    """

    def __init__(self, itemName: str, weight: float, volume: float):
        self.__strName = itemName
        self.__uuid = str(uuid.uuid4())
        self.__weight = weight
        self.__volume = volume

    def setName(self, itemName: str):
        self.__strName = itemName

    def getName(self):
        return self.__strName

    def getWeight(self):
        return self.__weight

    def setWeight(self, new_weight: int):
        self.__strName = new_weight

    def getVolume(self):
        return self.__volume

    def setVolume(self, new_volume: int):
        self.__strName = new_volume

    def getUuid(self):
        return self.__uuid


class TShelf:
    """

    This class represents a section of the storage facility with a capacity of 10x10

    """
    def __init__(self):
        self.__uuid = str(uuid.uuid4())
        arrBlank = np.zeros((v.COMPARTMENT_NUMBER, v.COMPARTMENT_NUMBER))
        self.layout = np.asarray(arrBlank, dtype=object)

    def getUuid(self):
        return self.__uuid


class TFacility:
    """

    Defines the whole storage facility with all the sections and items stored

    """
    def __init__(self, strFacName: str, shelf_number: int):
        super().__init__()
        self.__strName = strFacName
        self.lstShelfs = []
        for i in range(shelf_number * 2):
            self.createShelf()
        arrShelfs = np.array(self.lstShelfs)
        self.__layout = np.reshape(arrShelfs, (2, shelf_number))

        self.__path = r'C:\Users\Cristian\Desktop'
        self.__logList = []
        self.__log = pd.DataFrame

    def setName(self, strFacName: str):
        self.__strName = strFacName

    def getName(self):
        return self.__strName

    def createShelf(self):
        new_shelf = TShelf()
        self.lstShelfs.append(new_shelf)

    def getLayout(self):
        return self.__layout

    def setItems(self, items: list):
        item_number = len(items)
        i = int(0)
        overflow = False
        for shelf in self.__layout[0]:
            for h, row in enumerate(shelf.layout):
                for j, item in enumerate(row):
                    if i < item_number:
                        shelf.layout[h][j] = items[i]
                        i += 1
                    else:
                        overflow = True
                        break
        for shelf in self.__layout[1]:
            for row in shelf.layout:
                for j, item in enumerate(row):
                    if i < item_number:
                        row[j] = items[i]
                        i += 1
                    else:
                        overflow = True
                        break
        if overflow:
            print('Not enough space! ')

    def getLog(self):
        self.__log = pd.DataFrame(self.__logList, columns=['Uuid', 'Time', 'N° Items', 'Items'])
        return self.__log

    def setLoglist(self, data: list):
        self.__logList = data

    def getLogList(self):
        return self.__logList

    def getPath(self):
        return self.__path

    # Allows to set a path where to save your data
    def setPath(self, path: str):
        if Path(path).is_dir():
            self.__path = path
        else:
            print('Please insert a valid path! ')

    # Allows to save a log of the activity to a csv file in a specified directory
    def saveLog(self):
        try:
            path = ''.join([self.getPath(), r'\orders_log.csv'])
            self.getLog().to_csv(path_or_buf=path, index=False)
        except:
            print('Invalid path!')

    def getPosition(self, itemName: str):
        if self.checkItem(itemName):
            for i, shelf in enumerate(self.__layout[0]):
                for h, row in enumerate(shelf.layout):
                    for j, item in enumerate(row):
                        if item.getName() == itemName:
                            return [(0, i), (h, j)]
            for i, shelf in enumerate(self.__layout[1]):
                for h, row in enumerate(shelf.layout):
                    for j, item in enumerate(row):
                        if item.getName() == itemName:
                            return [(1, i), (h, j)]
        else:
            print('Invalid name')

    def getItemName(self, position: list):
        return self.__layout[position[0][0], position[0][1]].layout[position[1][0], position[1][1]].getName()

    def checkItem(self, itemName: str):
        for shelf in self.getLayout().flatten():
            for art in shelf.layout.flatten():
                if itemName == art.getName():
                    return True
        else:
            return False