"""
Módulo relacionado ao jogador
"""


import pygame as pg
from pycharmers.nodes import PhysicsBody, Sprite
from pycharmers.entities import Entity


class PlayerEntity(Entity):
    """ Entidade de testes para colisão """

    def __init__(self, position: tuple[int, int], size: tuple[int, int]):
        self.__body = PhysicsBody(position, size)
        self.__sprite = Sprite(pg.image.load(  # type: ignore
            "assets/python.png")
        )

    def process(self):
        pass

    def physics(self, delta_time: float, colliders: list[pg.Rect]):
        self.__body.apply_gravity(delta_time)
        self.__body.move_and_collide(delta_time, colliders)

    def input(self, pressed: list[str], just_pressed: list[str]):
        self.__body.velocity.x = 0

        if "left" in pressed:
            self.__body.velocity.x = -2
            self.__sprite.flip[0] = True
        if "right" in pressed:
            self.__body.velocity.x = 2
            self.__sprite.flip[0] = False
        if "space" in just_pressed and self.__body.grounded:
            self.__body.velocity.y = -8

    def draw(self, surface: pg.Surface):
        surface.blit(
            self.__sprite.texture,
            self.__body.shape
        )


class PlayerState:
    """ Informações sobre o estado do jogador """

    def __init__(self):
        self.__is_playing = False
        self.__has_item = False
        self.__finished_level = False

    def reset(self):
        """
        Reinicia os atributos para False
        """
        self.__is_playing = False
        self.__has_item = False
        self.__finished_level = False

    @property
    def has_item(self):
        """
        Se o jogador coletou o item

        Returns:
            bool: estado
        """
        return self.__has_item

    def grab_item(self):
        """
        Coleta o item
        """
        self.__has_item = True

    def release_item(self):
        """
        Solta o item
        """
        self.__has_item = False

    @property
    def finished_level(self):
        """
        Se o jogador terminou a fase

        Returns:
            bool: estado
        """
        return self.__finished_level

    def finish_level(self):
        """
        Termina a fase
        """
        self.__finished_level = True

    @property
    def is_playing(self):
        """
        Se o jogador está jogando a fase

        Returns:
            bool: estado
        """
        return self.__is_playing

    @property
    def gave_up(self):
        """
        Caso o jogador não tenha desistido da fase

        Returns:
            bool: estado
        """
        return not self.__is_playing and not self.__finished_level

    def give_up(self):
        """
        Desiste da fase
        """
        self.__is_playing = False
        self.__finished_level = False


class Player:
    """ Unifica as classes do player """

    def __init__(self, position: tuple[int, int], size: tuple[int, int]):
        self.__score = 0
        self.__entity = PlayerEntity(position, size)
        self.__state = PlayerState()

    @property
    def entity(self):
        """
        A entidade do jogador no nível

        Returns:
            PlayerEntity: a entidade
        """
        return self.__entity

    @property
    def state(self):
        """
        A classe do estado do jogador

        Returns:
            PlayerState: o estado do jogador
        """
        return self.__state

    @property
    def score(self):
        """
        Pontuação do jogador

        Returns:
            int: a pontuação
        """
        return self.__score

    @score.setter
    def score(self, score: int):
        """
        Define uma nova pontuação para o jogador

        Args:
            score (int): Nova pontuação
        """
        self.__score = score
