import arcade
import controller
from player_game import PlayerGame, Player


class SinglePlayerGame(PlayerGame):
    def __init__(self, player_img):
        super().__init__(player_img)
        self.player = Player(player_img)

    def setup(self, level, savex=192, savey=192):
        """ Set up the game here. Call this function to restart the game. """
        super().setup(level)
        self.player.state.isInPortal = False
        self.player.state.isWithKey = False
        self.player.player_sprite.center_x = savex
        self.player.player_sprite.center_y = savey
        self.player.score = 0
        self.player.cards = (self.controlador.get_all_cards())

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player.player_sprite,
                                                             self.wall_list,
                                                             self.controlador.GRAVITY)

        self.player_list.append(self.player.player_sprite)

    def on_draw(self):
        """ Render the screen. """
        super().on_draw()
        self.player.block_list.draw()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.player.score}"
        arcade.draw_text(score_text, 10, 10,
                         arcade.csscolor.BLACK, 18)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player.player_sprite.change_y = self.controlador.PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.player_sprite.change_x = -self.controlador.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.player_sprite.change_x = self.controlador.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.KEY_1:
            self.player.cards[0].power(self.player)
        elif key == arcade.key.KEY_2:
            self.player.cards[1].power(self.player)
        elif key == arcade.key.KEY_3:
            self.wall_list.append(self.player.cards[2].power(self.player))
        elif key == arcade.key.KEY_4:
            self.player.cards[3].power(self.player)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.player_sprite.change_x = 0

    def update(self, level):
        """ Movement and game logic """

        # Move the player with the physics engine
        self.player.update_animation()
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
            self.setup(self.level, self.player.savex, self.player.savey)

        # Is the player in the portal?
        if arcade.check_for_collision_with_list(self.player.player_sprite,
                                                self.portal_list):

            if self.player.state.isWithKey:
                self.player.state.isInPortal = True
                self.level_finished += 1
                self.level += 1
                if self.level_finished == 4:
                    ini_view = controller.Controller().finish_view()
                    self.window.show_view(ini_view)
                else:
                    self.setup(self.level)

        # See if the user got to the end of the level
        if self.player.player_sprite.center_x >= self.end_of_map:
            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True

