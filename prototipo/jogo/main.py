import arcade
import arcade.gui
from arcade.gui import UIManager
from player import Player

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
SCREEN_TITLE = "PyCharmers"
# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
game = None


class InitView(arcade.View):
    """ View to show instructions """

    def __init__(self):
        super().__init__()

        self.ui_manager = UIManager()

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.LIGHT_GOLDENROD_YELLOW)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("PyCharmers", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BEAU_BLUE, font_size=50, anchor_x="center")
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

        y_slot = self.window.height // 4
        left_column_x = self.window.width // 2
        backgound_menu = arcade.load_texture('assets/menu.png')
        button_normal = arcade.load_texture('assets/iconn.png')
        hovered_texture = arcade.load_texture('assets/iconn.png')
        pressed_texture = arcade.load_texture('assets/iconn.png')
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, backgound_menu)
        button = arcade.gui.UIImageButton(
            center_x=left_column_x,
            center_y=y_slot * 1,
            normal_texture=button_normal,
            hover_texture=hovered_texture,
            press_texture=pressed_texture,
            text=''
        )
        self.ui_manager.add_ui_element(button)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        self.ui_manager.purge_ui_elements()
        choice_view = ChoiceView()
        self.window.show_view(choice_view)


class FinishView(arcade.View):
    """ View to show instructions """

    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.BLEU_DE_FRANCE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Você terminou o jogo!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.show_view(InitView())


class ChoiceView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.BLEU_DE_FRANCE)
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.KEY_1:
            self.ui_manager.purge_ui_elements()
            choice_view = SinglePlayerGame('assets/player_spritesheet2.png')
            choice_view.setup(1)
            self.window.show_view(choice_view)
        elif key == arcade.key.KEY_2:
            self.ui_manager.purge_ui_elements()
            choice_view = SinglePlayerGame('assets/player_spritesheet.png')
            choice_view.setup(1)
            self.window.show_view(choice_view)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()
        backgound_menu = arcade.load_texture('assets/choicepersonagem.png')
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, backgound_menu)


class SinglePlayerGame(arcade.View):
    def __init__(self, player_img):
        super().__init__()

        # Set up the player info
        self.player = Player(player_img)
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

    def setup(self, level):
        """ Set up the game here. Call this function to restart the game. """
        self.player.player_sprite.center_x = 192
        self.player.player_sprite.center_y = 192
        self.player.score = 0

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

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player.player_sprite,
                                                             self.wall_list,
                                                             GRAVITY)
        self.player_list.append(self.player.player_sprite)

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

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.player.score}"
        arcade.draw_text(score_text, 10, 10,
                         arcade.csscolor.BLACK, 18)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.player_sprite.change_x = 0

    def update(self, level):
        """ Movement and game logic """

        # Move the player with the physics engine
        self.physics_engine.update()

        # See if we hit any coins
        key_hit_list = arcade.check_for_collision_with_list(self.player.player_sprite,
                                                            self.key_list)
        damage_hit_list = arcade.check_for_collision_with_list(self.player.player_sprite,
                                                               self.damage_list)
        # Loop through each coin we hit (if any) and remove it
        for key in key_hit_list:
            # Remove the coin
            key.remove_from_sprite_lists()
            # Add score
            self.player.score += 50
            self.player.state.isWithKey = True

        # Track if we need to change the viewport
        changed_viewport = False

        # Is the player dead?
        for key in damage_hit_list:
            key.remove_from_sprite_lists()
            self.setup(self.level)

        # Is the player in the portal?
        if arcade.check_for_collision_with_list(self.player.player_sprite,
                                                self.portal_list):

            if self.player.state.isWithKey:
                self.player.state.isInPortal = True
                self.level_finished += 1
                self.level += 1
                if self.level_finished == 4:
                    ini_view = FinishView()
                    self.window.show_view(ini_view)
                else:
                    self.setup(self.level)

        # See if the user got to the end of the level
        if self.player.player_sprite.center_x >= self.end_of_map:
            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True


def main():
    """ Main method """

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InitView()
    if game is not None:
        start_view = game

    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
