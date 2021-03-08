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
