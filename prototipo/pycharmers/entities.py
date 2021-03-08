"""
Classes abstratas nas quais as entidades do jogo
devem basear sua implementação.
"""


from abc import ABC, abstractmethod
import pygame as pg


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

        :param delta_time: tempo desde o último frame
        :param colliders: retângulos que possuem colisão
        """

    @abstractmethod
    def draw(self, surface: pg.Surface):
        """
        Método que realiza o desenho da entidade em
        determinada posição na superfície passada.
        """


class ControllableEntity(Entity):
    """ Entidade que deve receber também o estado do teclado. """

    @abstractmethod
    def input(self, pressed: list[str], just_pressed: list[str]):
        """
        Método para a atualização da entidade conforme
        o estado das teclas pressionadas.
        """
