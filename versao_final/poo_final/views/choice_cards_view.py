import arcade
import arcade.gui
from controller import controller
from arcade.gui import UIManager
from model.cards import SilentCard, JumpCard, SaveCard, BoxCard
from model.player import Player


class Card_shape(arcade.Sprite):
    def __init__(self, filename, tipo, scale=0.75):

        self.image_file_name = filename
        self.tipo = tipo
        # Call the parent
        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")


class SelectCardsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.controlador = controller.Controller()
        self.player_1 = Player('assets/blue')
        self.player_2 = Player('assets/yellow')
        self.cards_list = None
        self.text = "Jogador azul escolha carta 0/2"
    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.BLEU_DE_FRANCE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.controlador.SCREEN_WIDTH - 1, 0, self.controlador.SCREEN_HEIGHT - 1)

    def on_draw(self):
        arcade.start_render()
        self.ui_manager.purge_ui_elements()
        backgound_cards = arcade.load_texture('assets/cartas.jpg')
        arcade.draw_lrwh_rectangle_textured(0, 0, self.controlador.SCREEN_WIDTH, self.controlador.SCREEN_HEIGHT,
                                                backgound_cards)
        self.cards_list.draw()
        arcade.draw_text(self.text, self.window.width // 2, self.window.height // 4 * 2,
                         arcade.csscolor.WHITE, 18, align="center",
                         anchor_x="center", anchor_y="center", font_name='assets/Boxy-Bold.ttf')

    def setup(self):
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

        y_slot = self.window.height // 4
        middle_x = self.window.width // 5

        self.cards_list = arcade.SpriteList()
        b1 = Card_shape('assets/Encapsulamento_button.jpg', SaveCard())
        b1.position = middle_x *1 , y_slot * 1
        self.cards_list.append(b1)
        b2 = Card_shape('assets/expl_silenciados_button.jpg', SilentCard())
        b2.position = middle_x * 2, y_slot * 1
        self.cards_list.append(b2)
        b3 = Card_shape('assets/instanciar_button.jpg', BoxCard())
        b3.position = middle_x * 3, y_slot * 1
        self.cards_list.append(b3)
        b4 = Card_shape('assets/polimorfismo_button.jpg', JumpCard())
        b4.position = middle_x * 4, y_slot * 1
        self.cards_list.append(b4)

    def on_mouse_press(self, x, y, _button, _modifiers):
        choice = arcade.get_sprites_at_point((x, y), self.cards_list)
        if len(choice) > 0:
            if len(self.player_1.deck().cards()) < 2:
                self.player_1.deck().add_card(choice[0].tipo)
                self.text = f"Jogador azul escolha carta {len(self.player_1.deck().cards())}/2"
            elif len(self.player_2.deck().cards()) < 2:
                self.player_2.deck().add_card(choice[0].tipo)
                self.text = f"Jogador amarelo escolha carta {len(self.player_2.deck().cards())}/2"
                if len(self.player_2.deck().cards()) == 2:
                    choice_view = self.controlador.multi_player(self.player_1, self.player_2)
                    choice_view.setup(1)
                    self.window.show_view(choice_view)
