"""
Contém classes 'building blocks' do jogo, responsáveis por
realizar diversas das funcionalidades necessárias, como testes de
colisão e o desenho de sprites
"""


import pygame as pg
from pycharmers.utils import image_crop, image_load, json_load


class PhysicsBody:
    """
    Classe responsável pela posição e velocidade
    de uma entidade, levando em conta as colisões
    """

    def __init__(self, position: tuple[int, int], size: tuple[int, int]):
        self.__shape = pg.Rect(*position, *size)
        self.__position = pg.Vector2(*position)
        self.__velocity = pg.Vector2(0)
        self.__grounded = False

    @property
    def shape(self):
        """
        O retângulo de colisão da entidade

        Returns:
            pg.Rect: retângulo da entidade
        """
        return self.__shape

    @property
    def grounded(self):
        """
        Indica se a entidade está colidindo com o chão

        Returns:
            bool: se o corpo está no chão
        """
        return self.__grounded

    @property
    def velocity(self):
        """
        A velocidade do corpo

        Returns:
            pg.Vector2: vetor de velocidade da entidade
        """
        return self.__velocity

    def __is_colliding(self, colliders: list[pg.Rect]):
        """
        Retorna se o corpo está colidindo com uma lista de retângulos

        Args:
            colliders (list[pg.Rect]): lista de retângulos de colisão

        Returns:
            None: caso não haja colisão
            pg.Rect: caso haja colisão, é o retângulo de colisão
        """
        collision_index = self.__shape.collidelist(colliders)
        if collision_index != -1:
            return colliders[collision_index]
        return None

    def __collide_horizontally(self, collider: pg.Rect):
        """
        Corrige a posição horizontal em relação a velocidade
        e o retângulo de colisão

        Args:
            collider (pg.Rect): retângulo de colisão
        """
        if self.__velocity.x > 0:
            self.__shape.right = collider.left
        elif self.__velocity.x < 0:
            self.__shape.left = collider.right
        self.__position.x = self.__shape.x

    def __collide_vertically(self, collider: pg.Rect):
        """
        Corrige a posição vertical em relação a velocidade
        e o retângulo de colisão

        Args:
            collider (pg.Rect): retângulo de colisão
        """
        if self.__velocity.y > 0:
            self.__grounded = True
            self.__velocity.y = 1
            self.__shape.bottom = collider.top
        elif self.__velocity.y < 0:
            self.__velocity.y = 0
            self.__shape.top = collider.bottom
        self.__position.y = self.__shape.y

    def move_and_collide(self, delta_time: float, colliders: list[pg.Rect]):
        """
        Atualiza a posição com base na velocidade e no delta_time,
        e checa colisões na posição.

        Args:
            delta_time (float): tempo desde o último frame
            colliders (list[pg.Rect]): lista de retângulos de colisão
        """
        self.__grounded = False

        self.__position.x += self.__velocity.x * delta_time
        self.__shape.x = int(self.__position.x)
        if self.__velocity.x != 0:
            collision_rect = self.__is_colliding(colliders)
            if collision_rect is not None:
                self.__collide_horizontally(collision_rect)

        self.__position.y += self.__velocity.y * delta_time
        self.__shape.y = int(self.__position.y)
        if self.__velocity.y != 0:
            collision_rect = self.__is_colliding(colliders)
            if collision_rect is not None:
                self.__collide_vertically(collision_rect)

    def apply_gravity(self, delta_time: float):
        """
        Aplica a gravidade, além de fixar a velocidade vertical
        em um valor.

        Args:
            delta_time (float): tempo desde o último frame
        """
        self.__velocity.y += 0.5 * delta_time
        if self.__velocity.y > 6:
            self.__velocity.y = 6


class Sprite:
    """ Gerencia uma textura e o desenho dela """

    def __init__(self, texture: pg.Surface = None):
        self.__texture = texture
        self.__flip = [False, False]

    @property
    def texture(self):
        """
        A textura atual do sprite

        Returns:
            pg.Surface: a superfície da textura
        """
        return pg.transform.flip(self.__texture, *self.__flip)

    @texture.setter
    def texture(self, texture: pg.Surface):
        """
        Setter para uma nova texture

        Args:
            texture (pg.Surface): a nova textura
        """
        self.__texture = texture

    @property
    def flip(self):
        """
        O estado de reflexão do sprite

        Returns:
            list[bool]: o flip horizontal e vertical
        """
        return self.__flip


class Tile:
    """ Textura e informações de uma tile """

    def __init__(self, texture: pg.Surface, category: str, tags: list[str]):
        self.__texture = texture
        self.__category = category
        self.__tags = tags

    @classmethod
    def from_dict(cls, texture: pg.Surface, data: dict):
        """
        Cria a tile a partir de uma textura e um dicionário

        Args:
            texture (pg.Surface): a textura da tile
            data (dict): as informações da tile

        Returns:
            Tile: a tile criada
        """
        return cls(texture, data["category"], data["tags"])

    @property
    def texture(self):
        """
        A texture da tile

        Returns:
            Surface: a superfície da textura
        """
        return self.__texture

    @property
    def category(self):
        """
        O tipo da tile

        Returns:
            str: o nome da categoria
        """
        return self.__category

    def has_tag(self, tag: str):
        """
        Testa para ver se a tag especificada
        está nas tags da tile

        Args:
            tag (str): a tag em questão

        Returns:
            bool: se a tile possui a tag
        """
        return tag in self.__tags


class Tileset:
    """ Conjunto de tiles """

    def __init__(self, tiles: list[Tile], tile_size: tuple[int, int]):
        self.__tiles = tiles
        self.__tile_size = tile_size

    @classmethod
    def from_json(cls, path: str):
        """
        Cria o tileset a partir de um arquivo JSON

        Args:
            path (str): o caminho do arquivo JSON do tileset

        Returns:
            Tileset: o tileset criado
        """
        contents = json_load(path)
        return cls.from_dict(contents)

    @classmethod
    def from_dict(cls, data: dict):
        """
        Cria o tileset a partir de um dicionário

        Args:
            data (dict): dicionário com dados do tileset

        Returns:
            Tileset: o tileset criado
        """
        tileset = image_load(data["file_name"])
        textures = image_crop(tileset, data["tile_size"])

        tiles: list[Tile] = []
        # Criando tiles para cada informação e textura
        for texture, tile_data in zip(textures, data["tile_data"]):
            tiles.append(Tile.from_dict(texture, tile_data))
        return cls(tiles, data["tile_size"])

    @property
    def tile_size(self):
        """
        O tamanho das tiles do tileset

        Returns:
            tuple[int, int]: o (width, height) das tiles
        """
        return self.__tile_size

    def get_tile(self, index: int):
        """
        A tile com base no index

        Args:
            index (int): o index da tile

        Returns:
            None: se não existir essa tile no tileset
            Tile: a tile do index passado
        """
        index -= 1  # Consideramos 0 uma tile vazia
        if index < 0 or index >= len(self.__tiles):
            return None
        return self.__tiles[index]


class Tilemap:
    """ Um mapa com tiles pertencentes a um Tileset """

    def __init__(self, tileset: Tileset, tiles: list[list[int]]):
        self.__surface = pg.Surface((
            tileset.tile_size[0] * len(tiles[0]),
            tileset.tile_size[1] * len(tiles)
        ))
        self.__colliders: list[pg.Rect] = []
        self.__tileset = tileset
        self.__tiles = tiles

        self.draw()
        self.generate_colliders()

    @property
    def surface(self):
        """
        O tilemap desenhado em uma superfície

        Returns:
            pg.Surface: a superfície
        """
        return self.__surface

    @property
    def colliders(self):
        """
        Todos os retângulos de colisão do tilemap

        Returns:
            list[pg.Rect]: Lista de retângulos de colisão
        """
        return self.__colliders

    def generate_colliders(self):
        """
        Cria rects para cada uma das tiles que apresentam colisão
        """
        self.__colliders.clear()
        for tile_y, row in enumerate(self.__tiles):
            for tile_x in range(len(row)):
                tile = self.get_tile(tile_x, tile_y)

                if tile is not None:
                    if tile.category == "block":
                        tile_position = self.__get_tile_position(
                            tile_x, tile_y)
                        self.__colliders.append(
                            pg.Rect(*tile_position, *self.__tileset.tile_size)
                        )

    def __get_tile_position(self, tile_x: int, tile_y: int):
        """
        A posição real da tile

        Args:
            tile_x (int): a posição horizontal na matriz de tiles
            tile_y (int): a posição vertical na matriz de tiles

        Returns:
            tuple[int, int]: a posição real da tile, na superfície
        """
        return (
            self.__tileset.tile_size[0] * tile_x,
            self.__tileset.tile_size[1] * tile_y,
        )

    def get_tile(self, tile_x: int, tile_y: int):
        """
        Retorna a tile de uma determinada posição na matriz

        Args:
            tile_x (int): posição horizontal na matriz
            tile_y (int): posição vertical na matriz

        Returns:
            Tile: o objeto da tile
        """
        if tile_y < 0 or tile_y >= len(self.__tiles):
            return None
        if tile_x < 0 or tile_x >= len(self.__tiles[0]):
            return None
        tile_index = self.__tiles[tile_y][tile_x]
        return self.__tileset.get_tile(tile_index)

    def draw(self):
        """
        Atualiza o desenho do tilemap na superfície
        """
        for tile_y, row in enumerate(self.__tiles):
            for tile_x in range(len(row)):
                self.draw_tile(tile_x, tile_y)

    def draw_tile(self, tile_x: int, tile_y: int):
        """
        Atualiza o desenho de uma única tile na superfície

        Args:
            tile_x (int): posição horizontal da tile na matriz
            tile_y (int): posição vertical da tile na matriz
        """
        tile = self.get_tile(tile_x, tile_y)

        if tile is not None:
            self.__surface.blit(
                tile.texture, self.__get_tile_position(tile_x, tile_y))


class Camera:
    """
    Classe responsável por recortar o nível
    para o tamanho da janela, seguindo os jogadores
    """

    def __init__(self, size: tuple[int, int]):
        self.__size = size
        self.__shape = pg.Rect(0, 0, *size)
        self.__surface = pg.Surface(size)

    @property
    def surface(self):
        """
        O que deve ser desenhado das entidades / cenário
        do ponto de vista da câmera

        Returns:
            pg.Surface: a superfície da câmera
        """
        return self.__surface

    def __get_destination(self, bounds: tuple[int, int]):
        """
        Atualiza a posição de destino e o tamanho da superfície
        caso o tamanho dos layers seja menor que o tamanho da janela.

        Args:
            bounds (tuple[int, int]): tamanho dos layers

        Returns:
            tuple[int, int]: posição a desenhar
        """
        destination = [0, 0]
        self.__shape.size = self.__size  # Retorna ao valor original
        if self.__shape.width > bounds[0]:
            destination[0] = (self.__shape.width // 2) - (bounds[0] // 2)
            self.__shape.width = bounds[0]
        if self.__shape.height > bounds[1]:
            destination[1] = (self.__shape.height // 2) - (bounds[1] // 2)
            self.__shape.height = bounds[1]
        return destination

    def __fix_shape_to_bounds(self, bounds: tuple[int, int]):
        """
        Altera a posição do retângulo da câmera caso
        tenha ultrapassado o limite dos layers

        Args:
            bounds (tuple[int, int]): limite dos layers
        """
        self.__shape.x = max(self.__shape.x, 0)
        self.__shape.right = min(self.__shape.right, bounds[0])
        self.__shape.y = max(self.__shape.y, 0)
        self.__shape.bottom = min(self.__shape.bottom, bounds[1])

    def draw(self, targets: list[pg.Rect], layers: list[pg.Surface]):
        """
        Desenha na superfície conforme a posição da câmera

        Args:
            bounds (tuple[int, int]): as dimensões, para utilizar como bordas
            layers (list[pg.Surface]): lista de layers para desenhar
        """
        bounds = layers[0].get_size()  # Utiliza o primeiro layer
        self.__shape.center = targets[0].center  # Utiliza a primeira entidade

        destination = self.__get_destination(bounds)
        self.__fix_shape_to_bounds(bounds)

        for layer in layers:
            self.__surface.blit(layer.subsurface(self.__shape), destination)
