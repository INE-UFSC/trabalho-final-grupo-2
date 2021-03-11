"""
Módulo responsável pelas fases do jogo
"""


import pygame as pg
from pycharmers.nodes import Tilemap


class Level:
    """
    Classe responsável pelas informações relacionadas a uma fase
    """

    def __init__(self, tilemap: Tilemap):
        self.__tilemap = tilemap
        self.__entity_layer = pg.Surface(
            self.__tilemap.surface.get_size(), pg.SRCALPHA
        )

    @property
    def layers(self):
        """
        Todos os layers a serem desenhados

        Returns:
            list[Surface]: as camadas do nível
        """
        return [self.__tilemap.surface, self.__entity_layer]

    @property
    def entity_layer(self):
        """
        A superfície para o desenho das entidades

        Returns:
            pg.Surface: a superfície de entidades
        """
        return self.__entity_layer

    @property
    def tilemap(self):
        """
        O tilemap do nível

        Returns:
            Tilemap: o tilemap em questão
        """
        return self.__tilemap
