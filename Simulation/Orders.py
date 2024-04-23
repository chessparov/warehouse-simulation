import datetime
import uuid


class TOrder:
    """

    Defines an order

    """

    def __init__(self, *args):
        self.__uuid = str(uuid.uuid4())
        self.__date = datetime.datetime.now()
        self.__art = list()
        for item in args:
            if isinstance(item, str):
                self.__art.append(item)
            if isinstance(item, list):
                for sub_item in item:
                    if isinstance(sub_item, str):
                        self.__art.append(sub_item)
            else:
                print('Invalid input! ')

    def getDate(self):
        return self.__date

    def getArtlist(self):
        return self.__art

    def getUuid(self):
        return self.__uuid
