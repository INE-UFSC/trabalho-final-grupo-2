

class Card:

    def __init__(self, description: str, name:str, functionality=None):
        self.__description = description
        self.__name = name
        self.__functionality = functionality

    @property
    def description(self):
        return self.__description

    @property
    def name(self):
        return self.__name

    @property
    def functionality(self):
        return self.__functionality

    @description.setter
    def description(self, description):
        self.__description = description

    @name.setter
    def name(self, name):
        self.__name = name

    @functionality.setter
    def functionality(self, functionality):
        self.__functionality = functionality
