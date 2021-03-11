"""
Contém classes responsáveis pela inicialização
do pygame e a captura de teclas pressionadas.
"""


import sys
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

        Returns:
            float: o tempo passado desde o último frame
        """
        return self.__clock.tick(self.__framerate) * 0.001 * self.__framerate

    def draw(self, surface: pg.Surface):
        """
        Desenha uma superfície na janela.

        Args:
            surface (pg.Surface): superfície a desenhar
        """
        self.__window.fill((0, 0, 0))
        self.__window.blit(
            pg.transform.scale(surface, self.__window.get_size()), (0, 0)
        )
        pg.display.update()


class InputManager:
    """
    Gerencia as teclas pressionadas, com base em um dicionário de
    mapeamento de teclas à ações passado na inicialização

    O dicionário de mapeamentos passado na inicialização deve
    seguir o seguinte formato:

    mappings = {
        pg.KEY: "ação",
        ...
    }

    Em que pg.KEY são as constantes do pygame representando cada
    uma das teclas do teclado.
    """

    def __init__(self, mappings: dict[int, str]):
        self.__mappings = mappings
        self.__pressed: set[str] = set()
        self.__just_pressed: set[str] = set()

    @property
    def pressed(self):
        """
        Todas as teclas que estão pressionadas

        Returns:
            set[str]: set de teclas pressionadas, conforme os mapeamentos
        """
        return self.__pressed

    @property
    def just_pressed(self):
        """
        As teclas que foram pressionadas no frame

        Returns:
            set[str]: set de teclas pressionadas no frame,
            conforme os mapeamentos
        """
        return self.__just_pressed

    def update(self):
        """
        Atualiza o estado das teclas pressionadas, com base
        nos eventos do pygame
        """
        self.__just_pressed.clear()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type in (pg.KEYDOWN, pg.KEYUP) and event.key in self.__mappings:
                action_name = self.__mappings[event.key]
                if event.type == pg.KEYDOWN:
                    self.__pressed.add(action_name)
                    self.__just_pressed.add(action_name)
                elif action_name in self.__pressed:
                    self.__pressed.remove(action_name)
