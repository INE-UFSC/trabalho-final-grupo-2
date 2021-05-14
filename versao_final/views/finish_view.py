import arcade
import arcade.gui
from controller import controller
from arcade.gui import UIManager

from model.player import Player


class FinishView(arcade.View):
    def __init__(self, mensagem):
        super().__init__()
        self.ui_manager = UIManager()
        self.controlador = controller.Controller()
        self.mensagem = mensagem

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.BLEU_DE_FRANCE)
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.controlador.SCREEN_WIDTH - 1, 0, self.controlador.SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()
        backgound_menu = arcade.load_texture('assets/background.jpg')
        arcade.draw_lrwh_rectangle_textured(0, 0, self.controlador.SCREEN_WIDTH, self.controlador.SCREEN_HEIGHT,
                                            backgound_menu)
        arcade.draw_text(self.mensagem, self.window.width // 2, self.window.height // 4 * 2,
                         arcade.csscolor.WHITE, 32, align="center",
                         anchor_x="center", anchor_y="center", font_name='assets/Boxy-Bold.ttf')

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.show_view(self.controlador.init_view())

