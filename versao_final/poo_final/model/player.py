import arcade

RIGHT_FACING = 0
LEFT_FACING = 1
UPDATES_PER_FRAME = 4

'''
O player possuir três responsabilidades dentro da mecânica -> estados, cartas e update visual,
assim, separamos em uma classe player que é comporta por PlayerState e PlayerDeck 
'''
class PlayerState():
    def __init__(self):
        self.__isWithKey = False
        self.__isInPortal = False
        self.__isSave = False
        self.__countSave = 0
        self.__savey = 192
        self.__savex = 192
        self.__score = 100

    @property
    def savey(self):
        return self.__savey

    @savey.setter
    def savey(self, y):
        self.__savey = y

    @property
    def savex(self):
        return self.__savex

    @savex.setter
    def savex(self, x):
        self.__savex = x

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, score):
        self.__score += score

    @property
    def isWithKey(self):
        return self.__isWithKey

    @property
    def isInPortal(self):
        return self.__isInPortal

    @property
    def isSave(self):
        return self.__isSave

    @property
    def countSave(self):
        return self.__countSave

    @isInPortal.setter
    def isInPortal(self, state):
        self.__isInPortal = state

    @isWithKey.setter
    def isWithKey(self, state):
        self.__isWithKey = state

    @isSave.setter
    def isSave(self, state):
        self.__isSave = state

    @countSave.setter
    def countSave(self, num):
        self.__countSave = num


class PlayerDeck():
    def __init__(self):
        self.__block_list = arcade.SpriteList(use_spatial_hash=True)
        self.__cards = []

    def cards(self):
        return self.__cards

    def blocks(self):
        return self.__block_list

    def add_card(self, card):
        self.__cards.append(card)

    def add_list_cards(self, cards):
        for c in cards:
            self.__cards.append(c)

    def add_blocks(self, blocks):
        self.__block_list.append(blocks)

    def clean_blocks(self):
        self.__block_list = []

class Player():
    def __init__(self, image_source):
        self.image_source = image_source
        self.player_sprite = arcade.Sprite(f"{image_source}_idle.png", 3)
        self.player_sprite.center_x = 192
        self.player_sprite.center_y = 192
        self.__player_deck = PlayerDeck()
        self.__player_state = PlayerState()
        self.face_direction = RIGHT_FACING
        self.jumping = 0
        self.current_texture = 0
        self.idle_texture_pair = self.load_texture_pair(f"{image_source}_idle.png")
        self.walk_textures = []
        for i in range(2):
            texture = self.load_texture_pair(f"{image_source}_walk_{i}.png")
            self.walk_textures.append(texture)

        # self.player_sprite.update_animation()

    def state(self):
        return self.__player_state

    def deck(self):
        return self.__player_deck

    def load_texture_pair(self, filename):
        """
        Load a texture pair, with the second being a mirror image.
        """
        return [
            arcade.load_texture(filename),
            arcade.load_texture(filename, flipped_horizontally=True)
        ]

    def update_animation(self, delta_time: float = 1 / 60):
        # Figure out if we need to flip face left or right
        if self.player_sprite.change_x < 0 and self.face_direction == RIGHT_FACING:
            self.face_direction = LEFT_FACING
        elif self.player_sprite.change_x > 0 and self.face_direction == LEFT_FACING:
            self.face_direction = RIGHT_FACING
        # see if player is jumping or falling
        if self.player_sprite.change_y > 0 and self.jumping != 1:
            self.jumping = 1
        elif self.player_sprite.change_y < 0 and self.jumping != 2:
            self.jumping = 2
        elif self.player_sprite.change_y == 0:
            self.jumping = 0

        # walking animation
        self.current_texture += 1
        if self.current_texture > 1 * UPDATES_PER_FRAME:
            self.current_texture = 0
        frame = self.current_texture // UPDATES_PER_FRAME
        direction = self.face_direction
        self.player_sprite.texture = self.walk_textures[frame][direction]

        # idle animation
        if self.player_sprite.change_x == 0 and self.player_sprite.change_y == 0:
            self.jumping = 0
            self.player_sprite.texture = self.idle_texture_pair[self.face_direction]

        # jumping animation
        if self.jumping == 1:
            climbing = self.load_texture_pair(f"{self.image_source}_jump_0.png")
            self.player_sprite.texture = climbing[self.face_direction]
        elif self.jumping == 2:
            falling = self.load_texture_pair(f"{self.image_source}_jump_1.png")
            self.player_sprite.texture = falling[self.face_direction]

