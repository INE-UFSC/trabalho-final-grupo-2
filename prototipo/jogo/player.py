import arcade

RIGHT_FACING = 0
LEFT_FACING = 1
UPDATES_PER_FRAME = 4


class PlayerState():
    def __init__(self):
        self.__isWithKey = False
        self.__isInPortal = False
    
    @property
    def isWithKey(self):
        return self.__isWithKey
    
    @property
    def isInPortal(self):
        return self.__isInPortal
    
    @isInPortal.setter
    def isInPortal(self, state):
        self.__isInPortal = state
    
    @isWithKey.setter
    def isWithKey(self, state):
        self.__isWithKey = state


class Player():
    def __init__(self, image_source):
        self.image_source = image_source
        self.player_sprite = arcade.Sprite(f"{image_source}_idle.png", 3)
        self.player_sprite.center_x = 192
        self.player_sprite.center_y = 192
        self.score = 0
        self.state = PlayerState()
        self.face_direction = RIGHT_FACING
        self.jumping = 0
        self.current_texture = 0
        self.idle_texture_pair = self.load_texture_pair(f"{image_source}_idle.png")
        self.walk_textures = []
        for i in range(2):
            texture = self.load_texture_pair(f"{image_source}_walk_{i}.png")
            self.walk_textures.append(texture)

    def load_texture_pair(self, filename):
        """
        Load a texture pair, with the second being a mirror image.
        """
        return [
            arcade.load_texture(filename),
            arcade.load_texture(filename, flipped_horizontally=True)
        ]

    def update_animation(self, delta_time: float = 1/60):
        # Figure out if we need to flip face left or right
        if self.player_sprite.change_x < 0 and self.face_direction == RIGHT_FACING:
            self.face_direction = LEFT_FACING
        elif self.player_sprite.change_x > 0 and self.face_direction == LEFT_FACING:
            self.face_direction = RIGHT_FACING
        #see if player is jumping or falling
        if self.player_sprite.change_y > 0 and self.jumping != 1:
            self.jumping = 1
        elif self.player_sprite.change_y < 0 and self.jumping != 2:
            self.jumping = 2
        elif self.player_sprite.change_y == 0:
            self.jumping = 0

        #walking animation
        self.current_texture += 1
        if self.current_texture > 1 * UPDATES_PER_FRAME:
            self.current_texture = 0
        frame = self.current_texture // UPDATES_PER_FRAME
        direction = self.face_direction
        self.player_sprite.texture = self.walk_textures[frame][direction]

        #idle animation
        if self.player_sprite.change_x == 0 and self.player_sprite.change_y == 0:
            self.jumping = 0
            self.player_sprite.texture = self.idle_texture_pair[self.face_direction]

        #jumping animation
        if self.jumping == 1:
            climbing = self.load_texture_pair(f"{self.image_source}_jump_0.png")
            self.player_sprite.texture = climbing[self.face_direction]
        elif self.jumping == 2:
            falling = self.load_texture_pair(f"{self.image_source}_jump_1.png")
            self.player_sprite.texture = falling[self.face_direction]
