import arcade
import controller
from player_game import PlayerGame, Player


class MultiPlayerGame(PlayerGame):
    def __init__(self, player_img_one, player_img_two):
        super().__init__(player_img_one)
        # Set up the player info
        self.player_one = Player(player_img_one)
        self.player_two = Player(player_img_two)

    def setup(self, level):
        """ Set up the game here. Call this function to restart the game. """
        super().setup(level)
        self.player_one.state.isInPortal = False
        self.player_one.state.isWithKey = False
        self.player_one.player_sprite.center_x = 192
        self.player_one.player_sprite.center_y = 192
        self.player_one.score = 0
        self.player_one.cards = (self.controlador.get_cards())

        self.player_two.state.isInPortal = False
        self.player_two.state.isWithKey = False
        self.player_two.player_sprite.center_x = 192
        self.player_two.player_sprite.center_y = 192
        self.player_two.score = 0
        self.player_two.cards = (self.controlador.get_cards())
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
        score_text_one = f"Score: {self.player_one.score}"
        arcade.draw_text(score_text_one, 10, 10,
                         arcade.csscolor.BLACK, 18)
        score_text_two = f"Score: {self.player_two.score}"
        arcade.draw_text(score_text_two, 20, 20,
                         arcade.csscolor.BLUE_VIOLET, 18)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        #player one
        if key == arcade.key.W:
            if self.physics_engine_one.can_jump():
                self.player_one.player_sprite.change_y = self.controlador.PLAYER_JUMP_SPEED
        elif key == arcade.key.A:
            self.player_one.player_sprite.change_x = -self.controlador.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_one.player_sprite.change_x = self.controlador.PLAYER_MOVEMENT_SPEED
        ####mudar
        elif key == arcade.key.KEY_1:
            self.player_one.cards[0].power(self.player_one)
        elif key == arcade.key.KEY_2:
            self.player_one.cards[1].power(self.player_one)
        
        #player two
        if key == arcade.key.UP:
            if self.physics_engine_two.can_jump():
                self.player_two.player_sprite.change_y = self.controlador.PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_two.player_sprite.change_x = -self.controlador.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_two.player_sprite.change_x = self.controlador.PLAYER_MOVEMENT_SPEED
        ####mudar
        elif key == arcade.key.B:
            self.player_two.cards[0].power(self.player_two)
        elif key == arcade.key.N:
            self.player_two.cards[1].power(self.player_two)
            
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        #player one
        if key == arcade.key.A:
            self.player_one.player_sprite.change_x = 0
        elif key == arcade.key.D:
            self.player_one.player_sprite.change_x = 0

        #player two
        if key == arcade.key.LEFT:
            self.player_two.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT:
            self.player_two.player_sprite.change_x = 0

    def update(self, level):
        """ Movement and game logic """

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

        #player two
        key_hit_list_two = arcade.check_for_collision_with_list(self.player_two.player_sprite,
                                                                self.key_list)
        damage_hit_list_two = arcade.check_for_collision_with_list(self.player_two.player_sprite,
                                                                   self.damage_list)

        # Loop through each coin we hit (if any) and remove it
        for key in key_hit_list_one:
            # Remove the coin
            key.remove_from_sprite_lists()
            # Add score
            self.player_one.score += 50
            self.player_one.state.isWithKey = True
            arcade.play_sound(self.collect_sound)

        for key in key_hit_list_two:
            # Remove the coin
            key.remove_from_sprite_lists()
            # Add score
            self.player_two.score += 50
            self.player_two.state.isWithKey = True
            arcade.play_sound(self.collect_sound)

        # Track if we need to change the viewport
        changed_viewport = False

        # Is the player dead?
        for key in damage_hit_list_one:
            key.remove_from_sprite_lists()
            self.setup(self.level)

        for key in damage_hit_list_two:
            key.remove_from_sprite_lists()
            self.setup(self.level)

        # Is the player in the portal?
        if arcade.check_for_collision_with_list(self.player_one.player_sprite,
                                                self.portal_list):

            if self.player_one.state.isWithKey:
                self.player_one.state.isInPortal = True
                self.level_finished += 1
                self.level += 1
                if self.level_finished == 4:
                    ini_view = self.controlador.finish_view()
                    self.window.show_view(ini_view)
                else:
                    self.setup(self.level)

        # See if the user got to the end of the level
        if self.player_one.player_sprite.center_x >= self.end_of_map:
            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True

        #player two
        if arcade.check_for_collision_with_list(self.player_two.player_sprite,
                                                self.portal_list):

            if self.player_two.state.isWithKey:
                self.player_two.state.isInPortal = True
                self.level_finished += 1
                self.level += 1
                if self.level_finished == 4:
                    ini_view = self.controlador.finish_view()
                    self.window.show_view(ini_view)
                else:
                    self.setup(self.level)

        # See if the user got to the end of the level
        if self.player_two.player_sprite.center_x >= self.end_of_map:
            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
