import arcade
import arcade.gui
import constants
from single_player import SinglePlayerGame
from arcade.gui import UIManager


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
        arcade.set_viewport(0, constants.Constants().SCREEN_WIDTH - 1, 0, constants.Constants().SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("PyCharmers", constants.Constants().SCREEN_WIDTH / 2, constants.Constants().SCREEN_HEIGHT / 2,
                         arcade.color.BEAU_BLUE, font_size=50, anchor_x="center")
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

        y_slot = self.window.height // 4
        left_column_x = self.window.width // 2
        backgound_menu = arcade.load_texture('assets/menu.png')
        button_normal = arcade.load_texture('assets/iconn.png')
        hovered_texture = arcade.load_texture('assets/iconn.png')
        pressed_texture = arcade.load_texture('assets/iconn.png')
        arcade.draw_lrwh_rectangle_textured(0, 0, constants.Constants().SCREEN_WIDTH, constants.Constants().SCREEN_HEIGHT, backgound_menu)
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
        arcade.set_viewport(0, constants.Constants().SCREEN_WIDTH - 1, 0, constants.Constants().SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Você terminou o jogo!", constants.Constants().SCREEN_WIDTH / 2, constants.Constants().SCREEN_HEIGHT / 2,
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
        arcade.set_viewport(0, constants.Constants().SCREEN_WIDTH - 1, 0, constants.Constants().SCREEN_HEIGHT - 1)

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
        arcade.draw_lrwh_rectangle_textured(0, 0, constants.Constants().SCREEN_WIDTH, constants.Constants().SCREEN_HEIGHT, backgound_menu)