""" Classes representando as entidades do jogo """


from abc import ABC, abstractmethod
import pygame as pg
from pycharmers.nodes import PhysicsBody


class Entity(ABC):
    """ Uma entidade deve implementar estes métodos """

    @abstractmethod
    def process(self):
        """
        Método de processamento dos componentes
        da entidade, como a atualização do frame
        de animação e a troca de estados.

        É interessante utilizar desta função para
        a atualização de atributos que independem
        de influência externa direta.
        """

    @abstractmethod
    def physics(self, delta_time: float, colliders: list[pg.Rect]):
        """
        Método de atualização de componentes que
        necessitam de informações externas sobre
        o jogo, como testes de colisão e atualização
        de velocidade.

        Priorizar a multiplicação pelo delta_time
        de valores que dependem de tempo, como por
        exemplo movimentação, de forma a obter
        framerate independence.

        Args:
            delta_time (float): o tempo passado desde o último frame
            colliders (list[pg.Rect]): lista de retângulos para colisão
        """

    @abstractmethod
    def draw(self, surface: pg.Surface):
        """
        Método que realiza o desenho da entidade em
        determinada posição na superfície passada.

        Args:
            surface (pg.Surface): superfície para desenhar o sprite
        """


class ControllableEntity(Entity):
    """ Entidade que deve receber também o estado do teclado. """

    @abstractmethod
    def input(self, pressed: list[str], just_pressed: list[str]):
        """
        Método para a atualização da entidade conforme
        o estado das teclas pressionadas.

        Args:
            pressed (list[str]): teclas pressionadas
            just_pressed (list[str]): teclas pressionadas no frame atual
        """


class TestEntity(ControllableEntity):
    """ Entidade de testes para colisão """

    def __init__(self, shape: tuple[int, int]):
        self.__body = PhysicsBody(shape, (0, 0))

    def process(self):
        pass

    def physics(self, delta_time: float, colliders: list[pg.Rect]):
        self.__body.apply_gravity(delta_time)
        self.__body.move_and_collide(delta_time, colliders)

    def input(self, pressed: list[str], just_pressed: list[str]):
        self.__body.velocity.x = 0

        if "left" in pressed:
            self.__body.velocity.x = -2
        if "right" in pressed:
            self.__body.velocity.x = 2
        if "space" in just_pressed and self.__body.grounded:
            self.__body.velocity.y = -8

    def draw(self, surface: pg.Surface):
        pg.draw.rect(surface, (255, 255, 255), self.__body.shape)
