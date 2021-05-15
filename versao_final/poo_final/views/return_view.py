import json

import arcade
import arcade.gui
from controller import controller
from arcade.gui import UIManager
from model.cards import SilentCard, JumpCard, SaveCard, BoxCard
from model.player import Player
from model.save_gamee import SaveMultiPlayer, SaveSinglePlayer


class Button(arcade.Sprite):
    def __init__(self, go_to, scale=0.75):

        self.image_file_name = 'assets/iconn.png'
        self.go_to = go_to
        # Call the parent
        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")


class ReturnView(arcade.View):
    """
    Main view. Really the only view in this example. """

    def __init__(self):
        super().__init__()
        self.buttons_list = None
        self.ui_manager = UIManager()
        self.controlador = controller.Controller()

    def on_draw(self):
        """ Draw this view. GUI elements are automatically drawn. """
        """ Draw this view """
        arcade.start_render()

        backgound_menu = arcade.load_texture('assets/menu.png')
        arcade.draw_lrwh_rectangle_textured(0, 0, self.controlador.SCREEN_WIDTH, self.controlador.SCREEN_HEIGHT,
                                            backgound_menu)
        self.buttons_list.draw()

        arcade.draw_text("Continuar", self.window.width // 2 , self.window.height // 4 * 1,
                         arcade.csscolor.BLACK, 18, align="center",
                         anchor_x="center", anchor_y="center", font_name='assets/Boxy-Bold.ttf')

        arcade.draw_text("Novo Jogo", self.window.width // 2 , self.window.height // 4 * 2,
                         arcade.csscolor.BLACK, 18, align="center",
                         anchor_x="center", anchor_y="center", font_name='assets/Boxy-Bold.ttf')

    def on_show_view(self):
        """ Called once when view is activated. """
        self.setup()

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def setup(self):
        arcade.draw_text("PyCharmers", self.controlador.SCREEN_WIDTH / 2, self.controlador.SCREEN_HEIGHT / 2,
                         arcade.color.BEAU_BLUE, font_size=50, anchor_x="center")
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

        y_slot = self.window.height // 4
        left_column_x = self.window.width // 2

        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

        y_slot = self.window.height // 4
        middle_x = self.window.width // 2
        right_column_x = 3 * self.window.width // 4
        self.buttons_list = arcade.SpriteList()
        b1 = Button(1)
        b1.position = middle_x - 15, y_slot * 1
        self.buttons_list.append(b1)
        b2 = Button(2)
        b2.position = middle_x- 15, y_slot * 2
        self.buttons_list.append(b2)

    def on_mouse_press(self, x, y, button, key_modifiers):
        buttons = arcade.get_sprites_at_point((x, y), self.buttons_list)
        if len(buttons) > 0:
            if buttons[0].go_to == 1:
                try:
                    outfile = open("save.json", "rb")
                    dict = json.load(outfile)
                    if dict["mode"] == "multiplayer":
                        start_view = SaveMultiPlayer(self.controlador).return_game(dict)
                    elif dict['mode'] == "singleplayer":
                        start_view = SaveSinglePlayer(self.controlador).return_game(dict)

                    self.window.show_view(start_view)
                except:
                     print("erro")

            elif buttons[0].go_to == 2:
                self.window.show_view(self.controlador.init_view())