import arcade
import controller
from game.player_game import PlayerGame
from model.player import Player
import pickle

from model.save_game import SaveMultiPlayer


class MultiPlayerGame(PlayerGame):
    def __init__(self, player_one, player_two):
        super().__init__()
        # Set up the player info
        self.player_two = player_one
        self.player_one = player_two

    def setup(self, level, savex1=192, savex2=192, savey1=192, savey2=192):
        """ Set up the game here. Call this function to restart the game. """
        super().setup(level)
        self.player_one.state().isInPortal = False
        self.player_one.state().isWithKey = False
        self.player_one.player_sprite.center_x = savex1
        self.player_one.player_sprite.center_y = savey1

        self.player_two.state().isInPortal = False
        self.player_two.state().isWithKey = False
        self.player_two.player_sprite.center_x = savex2
        self.player_two.player_sprite.center_y = savey2

        # Create the 'physics engine'
        self.physics_engine_one = arcade.PhysicsEnginePlatformer(self.player_one.player_sprite,
                                                                 self.wall_list,
                                                                 self.controlador.GRAVITY)

        self.physics_engine_two = arcade.PhysicsEnginePlatformer(self.player_two.player_sprite,
                                                                 self.wall_list,
                                                                 self.controlador.GRAVITY)

        self.player_list.append(self.player_one.player_sprite)
        self.player_list.append(self.player_two.player_sprite)

    def on_draw(self):
        """ Render the screen. """
        super().on_draw()

        # Draw our score on the screen, scrolling it with the viewport
        score_text_one = f"Score: {self.player_one.state().score}"
        arcade.draw_text(score_text_one, 60, 180,
                         arcade.csscolor.BLACK, 18, font_name='assets/Boxy-Bold.ttf')
        score_text_two = f"Score: {self.player_two.state().score}"
        arcade.draw_text(score_text_two, 60, 160,
                         arcade.csscolor.BLACK, 18, font_name='assets/Boxy-Bold.ttf')

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # player one
        if key == arcade.key.W:
            if self.physics_engine_one.can_jump():
                self.player_one.player_sprite.change_y = self.controlador.PLAYER_JUMP_SPEED
        elif key == arcade.key.A:
            self.player_one.player_sprite.change_x = -self.controlador.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_one.player_sprite.change_x = self.controlador.PLAYER_MOVEMENT_SPEED

        elif key == arcade.key.KEY_1:
            self.player_one.deck.cards()[0].power(self.player_one)
        elif key == arcade.key.KEY_2:
            self.player_one.deck.cards()[1].power(self.player_one)

        # player two
        if key == arcade.key.UP:
            if self.physics_engine_two.can_jump():
                self.player_two.player_sprite.change_y = self.controlador.PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_two.player_sprite.change_x = -self.controlador.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_two.player_sprite.change_x = self.controlador.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.B:
            self.player_two.deck.cards()[0].power(self.player_two)
        elif key == arcade.key.M:
            self.player_two.deck.cards()[1].power(self.player_two)


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        # player one
        if key == arcade.key.A:
            self.player_one.player_sprite.change_x = 0
        elif key == arcade.key.D:
            self.player_one.player_sprite.change_x = 0

        # player two
        if key == arcade.key.LEFT:
            self.player_two.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT:
            self.player_two.player_sprite.change_x = 0

    def update(self, level):
        """ Movement and game logic """
        for i in self.player_one.block_list:
            self.wall_list.append(i)
        for i in self.player_two.block_list:
            self.wall_list.append(i)
        self.player_one.deck().clean_blocks()
        self.player_two.deck().clean_blocks()
        # Move the player with the physics engine
        self.physics_engine_one.update()
        self.physics_engine_two.update()

        self.player_one.update_animation()
        self.player_two.update_animation()

        # See if we hit any coins
        key_hit_list_one = arcade.check_for_collision_with_list(self.player_one.player_sprite,
                                                                self.key_list)
        damage_hit_list_one = arcade.check_for_collision_with_list(self.player_one.player_sprite,
                                                                   self.damage_list)

        # player two
        key_hit_list_two = arcade.check_for_collision_with_list(self.player_two.player_sprite,
                                                                self.key_list)
        damage_hit_list_two = arcade.check_for_collision_with_list(self.player_two.player_sprite,
                                                                   self.damage_list)

        # Loop through each coin we hit (if any) and remove it
        for key in key_hit_list_one:
            # Remove the coin
            key.remove_from_sprite_lists()
            # Add score
            self.player_one.state().score = 50
            self.player_one.state().isWithKey = True

        for key in key_hit_list_two:
            # Remove the coin
            key.remove_from_sprite_lists()
            # Add score
            self.player_two.state().score = 50
            self.player_two.state().isWithKey = True

        # Track if we need to change the viewport
        changed_viewport = False

        # Is the player dead?
        for key in damage_hit_list_one:
            key.remove_from_sprite_lists()
            if self.player_one.state().isSave == True:
                self.player_one.state().countSave = self.player_one.state.countSave - 10
                self.player_one.player_sprite.change_y = self.controlador.PLAYER_JUMP_SPEED
                if self.player_one.state().countSave == 0:
                    self.player_one.state().isSave = False
            else:
                self.setup(self.level, self.player_one.state().savex, self.player_two.player_sprite.center_x,
                           self.player_one.state().savey, self.player_two.player_sprite.center_y)

        for key in damage_hit_list_two:
            key.remove_from_sprite_lists()
            if self.player_two.state().isSave == True:
                self.player_two.state().countSave = self.player_two.state().countSave - 10
                self.player_two.player_sprite.change_y = self.controlador.PLAYER_JUMP_SPEED
                if self.player_two.state().countSave == 0:
                    self.player_two.state().isSave = False
            else:
                self.setup(self.level, self.player_one.player_sprite.center_x, self.player_two.state().savex,
                           self.player_one.player_sprite.center_y, self.player_two.state().savey)

        # Is the player in the portal?
        if arcade.check_for_collision_with_list(self.player_one.player_sprite,
                                                self.portal_list):

            if self.player_one.state.isWithKey:
                self.player_one.state.isInPortal = True
                self.level += 1
                if self.level == 4:
                    if self.player_two.state().score > self.player_one.state().score:
                        ini_view = self.controlador.finish_view("Azul vence")
                    else:
                        ini_view = self.controlador.finish_view("Amarelo vence")
                    self.window.show_view(ini_view)

                else:
                    self.setup(self.level)

        # See if the user got to the end of the level
        if self.player_one.player_sprite.center_x >= self.end_of_map:
            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True

        # player two
        if arcade.check_for_collision_with_list(self.player_two.player_sprite,
                                                self.portal_list):

            if self.player_two.state.isWithKey:
                self.player_two.state.isInPortal = True
                self.level += 1
                if self.level == 4:
                    if self.player_two.state().score > self.player_one.state().score:
                        ini_view = self.controlador.finish_view("Azul vence")
                    else:
                        ini_view = self.controlador.finish_view("Amarelo vence")
                    self.window.show_view(ini_view)
                else:
                    self.setup(self.level)

        # See if the user got to the end of the level
        if self.player_two.player_sprite.center_x >= self.end_of_map:
            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True

    def on_close(self):
        """Called when this view is not shown anymore"""
        #SaveMultiPlayer(self.player_one, self.player_two, self.level).save()
        print("ENCERRADO")
