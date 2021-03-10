""" Módulo de entrada do projeto """

import pygame as pg
from pycharmers.engine import DisplayManager, InputManager
from pycharmers.entities import TestEntity
from pycharmers.settings import mappings
from pycharmers.game_classes.player import Player

def main():
    """ Função principal """

    display = DisplayManager((320, 240), scale=2)
    inputs = InputManager(mappings)

    #Cria a entity dentro da classe Player
    player = Player((16, 16))

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

    # Para testar mudanças de estado do jogador
    key = tuple([pg.Rect(position_x, 128, 16, 16) for position_x in range(144, 160, 16)])
    pg.draw.rect(tile_layer, (255, 255, 0), key)

    for rect in rects:
        pg.draw.rect(tile_layer, (255, 0, 0), rect)

    # Loop principal do jogo
    while True:
        #Adicionar condição
        player.state.grab_item()
        if player.state.has_item:
            # Cria um retâgulo onde é possível escrever texto
            font = pg.font.Font('freesansbold.ttf', 10)
            text = font.render('Está com o item', True, (135, 206, 250), (0, 0, 0))
            textRect = text.get_rect()
            # set the center of the rectangular object.
            textRect.center = (160, 10)
        else:
            font = pg.font.Font('freesansbold.ttf', 10)
            text = font.render('Não está com o item', True, (135, 206, 250), (0, 0, 0))
            textRect = text.get_rect()
            # set the center of the rectangular object.
            textRect.center = (160, 10)

        delta_time = display.tick()
        inputs.update()

        entity_layer.fill((0, 0, 0, 0))
        entity_layer.blit(text, textRect)
        player.entity.process()
        player.entity.input(inputs.pressed, inputs.just_pressed)
        player.entity.physics(delta_time, rects)
        player.entity.draw(entity_layer)

        display.draw([tile_layer, entity_layer])


# Chamar a função main ao rodar o módulo
if __name__ == "__main__":
    main()
