""" Módulo de entrada do projeto """

import pygame as pg
from pycharmers.engine import DisplayManager, InputManager
from pycharmers.settings import mappings
from pycharmers.game.player import Player


def main():
    """ Função principal """

    display = DisplayManager((320, 240), scale=2)
    inputs = InputManager(mappings)

    entity_layer = pg.Surface((320, 240), pg.SRCALPHA)
    tile_layer = pg.Surface((320, 240))
    rects = [
        pg.Rect(position_x, 224, 16, 16)
        for position_x in range(0, 320, 16)
    ] + [
        pg.Rect(position_x, 208, 16, 16)
        for position_x in range(160, 240, 16)
    ] + [
        pg.Rect(position_x, 160, 16, 16)
        for position_x in range(80, 160, 16)
    ]

    for rect in rects:
        pg.draw.rect(tile_layer, (255, 0, 0), rect)

    player = Player((0, 0), (16, 16))

    # Loop principal do jogo
    while True:
        delta_time = display.tick()
        inputs.update()

        entity_layer.fill((0, 0, 0, 0))
        player.entity.process()
        player.entity.input(inputs.pressed, inputs.just_pressed)
        player.entity.physics(delta_time, rects)
        player.entity.draw(entity_layer)

        display.draw([tile_layer, entity_layer])


# Chamar a função main ao rodar o módulo
if __name__ == "__main__":
    main()
