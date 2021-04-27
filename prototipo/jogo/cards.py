from abc import ABC, abstractmethod

import arcade


class Card(ABC):
    @abstractmethod
    def __init__(self):
        pass
    @abstractmethod
    def power(self, player):
        pass


class JumpCard(Card):

    def __init__(self):
        self.__jumpspeed = 20

    def power(self, player):
        player.player_sprite.change_y = self.__jumpspeed


class BoxCard(Card):

    def __init__(self):
        pass

    def power(self, player):
        wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", 0.25)
        wall.position = player.player_sprite.position
        return wall
        #player.block_list.append(wall)


class SaveCard(Card):

    def __init__(self):
        pass

    def power(self, player):
        player.state.isSave = True
        player.state.countSave = 60


class SilentCard(Card):
    def __init__(self):
        pass

    def power(self, player):
        player.savex = player.player_sprite.position[0]
        player.savey = player.player_sprite.position[1]


