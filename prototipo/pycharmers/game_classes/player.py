
from pycharmers.game_classes.playerstate import PlayerState
from pycharmers.entities import TestEntity


# Implementar atributos e métodos para o funcionamento das cartas
class Player:
    def __init__(self, shape: tuple[int, int]):
        self.__score = 0
        self.__entity = TestEntity(shape)
        self.__state = PlayerState()

    @property
    def entity(self):
        return self.__entity

    @property
    def state(self):
        return self.__state

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, score: int):
        self.__score += score
