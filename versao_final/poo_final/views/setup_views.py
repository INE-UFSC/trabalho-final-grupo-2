import arcade
import arcade.gui
from controller import controller
from arcade.gui import UIManager

from model.player import Player


class Personagem(arcade.Sprite):
    def __init__(self, filename, tipo, scale=1):

        self.image_file_name = filename
        self.tipo = tipo
        # Call the parent
        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")


class ChoiceView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.controlador = controller.Controller()
        self.personagem_list = None

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
        backgound_menu = arcade.load_texture('assets/choice_view.jpg')
        arcade.draw_lrwh_rectangle_textured(0, 0, self.controlador.SCREEN_WIDTH, self.controlador.SCREEN_HEIGHT,
                                            backgound_menu)
        self.personagem_list.draw()

    def setup(self):
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

        y_slot = self.window.height // 4
        middle_x = self.window.width // 5

        self.personagem_list = arcade.SpriteList()
        b1 = Personagem('assets/button_yellow.png', 1)
        b1.position = middle_x * 2, y_slot * 1
        self.personagem_list.append(b1)
        b2 = Personagem('assets/button_blue.png', 2)
        b2.position = middle_x * 3, y_slot * 1
        self.personagem_list.append(b2)

    def on_mouse_press(self, x, y, _button, _modifiers):
        choice = arcade.get_sprites_at_point((x, y), self.personagem_list)
        if len(choice) > 0:
            if choice[0].tipo == 1:
                self.window.show_view(self.controlador.card_view(Player('assets/yellow')))
            else:
               self.window.show_view(self.controlador.card_view(Player('assets/blue')))


class CardView(arcade.View):
    def __init__(self, personagem):
        super().__init__()
        self.ui_manager = UIManager()
        self.controlador = controller.Controller()
        self.personagem = personagem

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.BLEU_DE_FRANCE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.controlador.SCREEN_WIDTH - 1, 0, self.controlador.SCREEN_HEIGHT - 1)

    def on_draw(self):
        arcade.start_render()
        self.ui_manager.purge_ui_elements()
        y_slot = self.window.height // 4
        left_column_x = self.window.width // 2
        backgound_cards = arcade.load_texture('assets/cartas_single.jpg')
        arcade.draw_lrwh_rectangle_textured(0, 0, self.controlador.SCREEN_WIDTH, self.controlador.SCREEN_HEIGHT,
                                                backgound_cards)
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        single = self.controlador.single_player(self.personagem)
        single.setup(1)
        self.window.show_view(single)


# Multi player views
class InstruView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.controlador = controller.Controller()

    def on_draw(self):
        arcade.start_render()
        self.ui_manager.purge_ui_elements()
        y_slot = self.window.height // 4
        left_column_x = self.window.width // 2
        backgound_instru = arcade.load_texture('assets/instruções.jpg')
        arcade.draw_lrwh_rectangle_textured(0, 0, self.controlador.SCREEN_WIDTH, self.controlador.SCREEN_HEIGHT,
                                            backgound_instru)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        choice_view = self.controlador.select_cards_view()
        choice_view.setup()
        self.window.show_view(choice_view)

