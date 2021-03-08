"""
Módulo responsável por armazenar algumas configurações
que serão utilizadas no setup dos objetos do jogo.

Talvez no futuro seja mais ideal a utilização de outro formato,
como um JSON, YAML ou até um arquivo arquivo gerado pelo pickle.
"""


import pygame as pg


mappings: dict[int, str] = {
    pg.K_w: "up",
    pg.K_a: "left",
    pg.K_s: "down",
    pg.K_d: "right",
    pg.K_SPACE: "space"
}
