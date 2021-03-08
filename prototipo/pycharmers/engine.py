"""
Contém classes responsáveis pela inicialização
do pygame e a captura de teclas pressionadas.
"""


import pygame as pg


class DisplayManager:
    """
    Responsável pela inicialização do pygame
    e a atualização do conteúdo da janela.
    """

    def __init__(self, resolution: tuple[int, int], scale: int = 1):
        pg.init()
        pg.display.set_caption("Game")

        self.__framerate = 60
        self.__clock = pg.time.Clock()
        self.__window = pg.display.set_mode(
            (resolution[0] * scale, resolution[1] * scale), 0, 32
        )

        # Primeiro tick do clock, para corrigir o próximo no loop
        self.tick()

    def tick(self) -> float:
        """
        Atualiza o clock do jogo e retorna o delta time

        :returns: o tempo passado desde o último frame
        """
        return self.__clock.tick(self.__framerate) * 0.001 * self.__framerate

    def draw(self, layers: list[pg.Surface]):
        """
        Desenha a camada de superfícies na janela.

        Assume que todas as camadas passadas possuem tamanho
        igual ao da janela, sem levar em conta a scale.

        :param layers: a lista de superfícies para desenhar na janela
        """
        self.__window.fill((0, 0, 0))
        for surface in layers:
            self.__window.blit(
                pg.transform.scale(surface, self.__window.get_size()), (0, 0)
            )
        pg.display.update()
