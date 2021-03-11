"""
Funções utilitárias
"""


import json
import pygame as pg


def json_load(path: str):
    """
    Carrega um arquivo JSON, e retorna o conteúdo

    Args:
        path (str): o caminho para o arquivo JSON

    Returns:
        dict: o arquivo JSON carregado em um dicionário
    """
    with open(path) as file:
        contents = json.load(file)
    return contents


def image_load(path: str):
    """
    Carrega uma imagem utilizando as funções do pygame

    Args:
        path (str): o caminho para a imagem

    Returns:
        pg.Surface: a superfície da textura
    """
    return pg.image.load(path).convert_alpha()


def image_crop(image: pg.Surface, shape_size: tuple[int, int]):
    """
    Recorta uma imagem em diversas partes de tamanho 'size'

    Args:
        image (pg.Surface): a imagem para recortar
        shape_size (tuple[int, int]): o tamanho de cada recorte

    Returns:
        list[pg.Surface]: lista de recortes da imagem
    """
    image_width, image_height = image.get_size()
    shape_width, shape_height = shape_size
    cropped = []
    for j in range(0, image_height, shape_height):
        for i in range(0, image_width, shape_width):
            clip_rect = pg.Rect(i, j, shape_width, shape_height)
            cropped.append(image.subsurface(clip_rect))
    return cropped
