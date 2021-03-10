class PlayerState:
    def __init__(self, is_playing=False, has_item=False, finished_level=False, gave_up=False):
        self.__is_playing = is_playing
        self.__has_item = has_item
        self.__finished_level = finished_level
        self.__gave_up = gave_up

    def reset(self):
        self.__is_playing = False
        self.__has_item = False
        self.__finished_level = False

    @property
    def has_item(self):
        return self.__has_item

    def grab_item(self):
        self.__has_item = True

    def release_item(self):
        self.__has_item = False

    @property
    def finished_level(self):
        return self.__finished_level

    def finish_level(self):
        self.__finished_level = True

    @property
    def is_playing(self):
        return self.__is_playing

    @property
    def gave_up(self):
        return self.__gave_up

    def give_up(self):
        self.__gave_up = True