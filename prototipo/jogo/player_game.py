import arcade
import controller
from player import Player


class PlayerGame(arcade.View):
    def __init__(self, player_img):
        super().__init__()

        # Set up the player info
        '''self.player = Player(player_img)'''
        # Don't show the mouse cursor
        self.window.set_mouse_visible(True)

        arcade.set_background_color(arcade.color.BLEU_DE_FRANCE)
        self.key_list = None
        self.wall_list = None
        self.portal_list = None
        self.background_list = None
        self.player_list = None
        self.damage_list = None
        # Where is the right edge of the map?
        self.end_of_map = 0
        self.physics_engine = None
        # Level
        self.level = 1

        self.level_finished = 0
        self.controlador = controller.Controller()

    def setup(self, level):
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.portal_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.key_list = arcade.SpriteList()
        self.damage_list = arcade.SpriteList()

        # Set up the player

        # --- Load in a map from the tiled editor ---

        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'Platforms'
        # Name of the layer that has items for pick-up
        key_layer_name = 'chave'
        # Name of the layer that has the user  portal
        portal_layer_name = 'gate'
        # Name of the layer that has items for background
        background_layer_name = 'fundo'
        # Name of the layer that has damage platforms
        damage_layer_name = 'damage'

        # Map name

        map_name = f"assets/map-{level}.tmx"


        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = my_map.map_size.width * 1 * 128

        # -- Background
        self.background_list = arcade.tilemap.process_layer(my_map,
                                                            background_layer_name)

        # -- portals
        self.portal_list = arcade.tilemap.process_layer(my_map,
                                                        portal_layer_name,
                                                        1,
                                                        use_spatial_hash=True)

        # -- Platforms
        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=platforms_layer_name,
                                                      scaling=1,
                                                      use_spatial_hash=True)

        # -- keys
        self.key_list = arcade.tilemap.process_layer(my_map,
                                                     key_layer_name,
                                                     1,
                                                     use_spatial_hash=True)
        # -- damage
        self.damage_list = arcade.tilemap.process_layer(my_map,
                                                        damage_layer_name,
                                                        1,
                                                        use_spatial_hash=True)

        # --- Other stuff
        # Set the background color
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        self.wall_list.draw()
        self.background_list.draw()
        self.wall_list.draw()
        self.key_list.draw()
        self.player_list.draw()
        self.portal_list.draw()
        self.damage_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        pass

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        pass

    def update(self, level):
        """ Movement and game logic """
        pass