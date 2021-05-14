import arcade

import arcade.gui
from arcade.gui import UIManager


class Button(arcade.Sprite):
    def __init__(self, go_to, scale=0.75):

        self.image_file_name = 'assets/iconn.png'
        self.go_to = go_to
        # Call the parent
        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")


class InitView(arcade.View):
    """
    Main view. Really the only view in this example. """

    def __init__(self, controller):
        super().__init__()
        self.buttons_list = None
        self.ui_manager = UIManager()
        self.controlador = controller

    def on_draw(self):
        """ Draw this view. GUI elements are automatically drawn. """
        """ Draw this view """
        arcade.start_render()

        backgound_menu = arcade.load_texture('assets/menu.png')
        arcade.draw_lrwh_rectangle_textured(0, 0, self.controlador.SCREEN_WIDTH, self.controlador.SCREEN_HEIGHT,
                                            backgound_menu)
        self.buttons_list.draw()

        arcade.draw_text("Single Player", self.window.width // 2 , self.window.height // 4 * 1,
                         arcade.csscolor.BLACK, 18, align="center",
                         anchor_x="center", anchor_y="center", font_name='assets/Boxy-Bold.ttf')

        arcade.draw_text("Multi Player", self.window.width // 2 , self.window.height // 4 * 2,
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
                choice_view = self.controlador.choice_view()
                choice_view.setup()
                self.window.show_view(choice_view)
            elif buttons[0].go_to == 2:
                self.window.show_view(self.controlador.instru_view())