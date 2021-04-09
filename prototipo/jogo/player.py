import arcade

class PlayerState():
    def __init__(self):
        self.__isWithKey = False
        self.__isInPortal = False
    
    @property
    def isWithKey(self):
        return self.__isWithKey
    
    @property
    def isInPortal(self):
        return self.__isInPortal
    
    @isInPortal.setter
    def isInPortal(self, state):
        self.__isInPortal = state
    
    @isWithKey.setter
    def isWithKey(self, state):
        self.__isWithKey = state


class Player():
    def __init__(self, image_source):
        self.image_source = image_source
        self.player_sprite = arcade.Sprite(image_source, 3)
        self.player_sprite.center_x = 192
        self.player_sprite.center_y = 192
        self.score = 0
        self.state = PlayerState()
    
    