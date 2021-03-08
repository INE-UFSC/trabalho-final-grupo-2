"""
Contém classes 'building blocks' das entidades, responsáveis por
realizar diversas das funcionalidades necessárias, como teste de
colisão e o desenho de sprites
"""


import pygame as pg


class PhysicsBody:
    """
    Classe responsável pela posição e velocidade
    de uma entidade, levando em conta as colisões
    """

    def __init__(self, shape: tuple[int, int], position: tuple[int, int]):
        self.__shape = pg.Rect(*position, *shape)
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
