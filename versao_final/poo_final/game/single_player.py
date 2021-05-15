import arcade
import controller.controller
from game.player_game import PlayerGame
from model.player import Player
from model.save_gamee import SaveSinglePlayer


class SinglePlayerGame(PlayerGame):
    def __init__(self, player_img):
        super().__init__()
        self.player = player_img

    def setup(self, level, savex=192, savey=192):
        """ Set up the game here. Call this function to restart the game. """
        super().setup(level)
        self.level = level

        self.player.state().isInPortal = False
        self.player.state().isWithKey = False
        self.player.player_sprite.center_x = savex
        self.player.player_sprite.center_y = savey
        self.player.deck().add_list_cards(self.controlador.get_all_cards())

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player.player_sprite,
                                                             self.wall_list,
                                                             self.controlador.GRAVITY)

        self.player_list.append(self.player.player_sprite)

    def on_draw(self):
        """ Render the screen. """
        super().on_draw()


        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.player.state().score}"
        arcade.draw_text(score_text, 60, 180,
                         arcade.csscolor.BLACK, 18,  font_name='assets/Boxy-Bold.ttf')

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                arcade.play_sound(self.jump_sound)
                self.player.player_sprite.change_y = self.controlador.PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.player_sprite.change_x = -self.controlador.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.player_sprite.change_x = self.controlador.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.KEY_1:
            self.player.state().score = - 5
            self.player.deck().cards()[0].power(self.player)
        elif key == arcade.key.KEY_2:
            self.player.state().score = - 5
            self.player.deck().cards()[1].power(self.player)
        elif key == arcade.key.KEY_3:
            self.player.state().score = - 5
            self.player.deck().cards()[2].power(self.player)
        elif key == arcade.key.KEY_4:
            self.player.state().score = - 5
            self.player.deck().cards()[3].power(self.player)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.player_sprite.change_x = 0

    def update(self, level):
        """ Movement and game logic """
        for i in self.player.deck().blocks():
            self.wall_list.append(i)
        self.player.deck().clean_blocks()
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
            self.player.state().score = 50
            self.player.state().isWithKey = True
            arcade.play_sound(self.collect_sound)

        # Track if we need to change the viewport
        changed_viewport = False

        # Is the player dead?
        for key in damage_hit_list:
            key.remove_from_sprite_lists
            if self.player.state().isSave == True:
                self.player.state().countSave = self.player.state().countSave - 10
                self.player.player_sprite.change_y = self.controlador.PLAYER_JUMP_SPEED
                if self.player.state().countSave == 0:
                    self.player.state().isSave = False
            else:
                self.setup(self.level, self.player.state().savex, self.player.state().savey)
                self.player.state().score = -20

        # Is the player in the portal?
        if arcade.check_for_collision_with_list(self.player.player_sprite,
                                                self.portal_list):

            if self.player.state().isWithKey:
                self.player.state().isInPortal = True
                self.level += 1
                if self.level == 4:
                    ini_view = self.controlador.finish_view("Você terminou o jogo")
                    self.window.show_view(ini_view)
                else:
                    self.setup(self.level)

        # See if the user got to the end of the level
        if self.player.player_sprite.center_x >= self.end_of_map:
            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True

    def on_close(self):
        """Called when this view is not shown anymore"""
        SaveSinglePlayer(self.controlador, self.player, self.level).save()
