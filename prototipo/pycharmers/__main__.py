""" Módulo de entrada do projeto """


import pygame as pg
from pycharmers.engine import DisplayManager, InputManager
from pycharmers.entities import TestEntity
from pycharmers.settings import mappings


def main():
    """ Função principal """

    display = DisplayManager((320, 240), scale=2)
    inputs = InputManager(mappings)

    # Temporário para o teste das colisões
    entity = TestEntity((16, 16))
    entity_layer = pg.Surface((320, 240), pg.SRCALPHA)
    tile_layer = pg.Surface((320, 240))
    rects = [
        pg.Rect(position_x, 224, 16, 16)
        for position_x in range(0, 320, 16)
    ] + [
        pg.Rect(position_x, 208, 16, 16)
        for position_x in range(160, 240, 16)
    ]
    for rect in rects:
        pg.draw.rect(tile_layer, (255, 0, 0), rect)

    # Loop principal do jogo
    while True:
        delta_time = display.tick()
        inputs.update()

        entity_layer.fill((0, 0, 0, 0))

        entity.process()
        entity.input(inputs.pressed, inputs.just_pressed)
        entity.physics(delta_time, rects)
        entity.draw(entity_layer)

        display.draw([tile_layer, entity_layer])


# Chamar a função main ao rodar o módulo
if __name__ == "__main__":
    main()
