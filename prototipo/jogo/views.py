import arcade
import arcade.gui
import controller
from arcade.gui import UIManager


class InitView(arcade.View):
    """ View to show instructions """

    def __init__(self):
        super().__init__()

        self.ui_manager = UIManager()
        self.controlador = controller.Controller()

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.LIGHT_GOLDENROD_YELLOW)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.controlador.SCREEN_WIDTH - 1, 0, self.controlador.SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("PyCharmers", self.controlador.SCREEN_WIDTH / 2, self.controlador.SCREEN_HEIGHT / 2,
                         arcade.color.BEAU_BLUE, font_size=50, anchor_x="center")
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

        y_slot = self.window.height // 4
        left_column_x = self.window.width // 2
        backgound_menu = arcade.load_texture('assets/menu.png')
        button_normal = arcade.load_texture('assets/iconn.png')
        hovered_texture = arcade.load_texture('assets/iconn.png')
        pressed_texture = arcade.load_texture('assets/iconn.png')
        arcade.draw_lrwh_rectangle_textured(0, 0, self.controlador.SCREEN_WIDTH, self.controlador.SCREEN_HEIGHT, backgound_menu)
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
        choice_view = self.controlador.choice_view()
        self.window.show_view(choice_view)


class FinishView(arcade.View):
    """ View to show instructions """

    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.controlador = controller.Controller()

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.BLEU_DE_FRANCE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.controlador.SCREEN_WIDTH - 1, 0, self.controlador.SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Você terminou o jogo!", self.controlador.SCREEN_WIDTH / 2, self.controlador.SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.show_view(self.controlador.init_view())


class ChoiceView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.controlador = controller.Controller()

    
    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.BLEU_DE_FRANCE)
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.controlador.SCREEN_WIDTH - 1, 0, self.controlador.SCREEN_HEIGHT - 1)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.KEY_1:
            self.ui_manager.purge_ui_elements()
            card = None
            personagem = 1
            choice_view = self.controlador.card_view(card, personagem)
            self.window.show_view(choice_view)
        elif key == arcade.key.KEY_2:
            self.ui_manager.purge_ui_elements()
            card = None
            personagem = 2
            choice_view = self.controlador.card_view(card, personagem)
            self.window.show_view(choice_view)
            #choice_view = self.controlador.single_player('assets/player_spritesheet.png')
            
        elif key == arcade.key.KEY_3:
            self.ui_manager.purge_ui_elements()
            card = 1
            personagem = None
            choice_view = self.controlador.card_view(card, personagem)
            self.window.show_view(choice_view)


    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()
        backgound_menu = arcade.load_texture('assets/choice_view.jpg')
        arcade.draw_lrwh_rectangle_textured(0, 0, self.controlador.SCREEN_WIDTH, self.controlador.SCREEN_HEIGHT, backgound_menu)

class CardView(arcade.View):
    def __init__(self, card, personagem):
        super().__init__()
        self.ui_manager = UIManager()
        self.controlador = controller.Controller()
        self.card = card
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
        if self.card is not None:
            y_slot = self.window.height // 4
            left_column_x = self.window.width // 2
            backgound_cards = arcade.load_texture('assets/cartas.jpg')
            arcade.draw_lrwh_rectangle_textured(0, 0, self.controlador.SCREEN_WIDTH, self.controlador.SCREEN_HEIGHT, backgound_cards)
        else:
            y_slot = self.window.height // 4
            left_column_x = self.window.width // 2
            backgound_cards = arcade.load_texture('assets/cartas_single.jpg')
            arcade.draw_lrwh_rectangle_textured(0, 0, self.controlador.SCREEN_WIDTH, self.controlador.SCREEN_HEIGHT, backgound_cards)
        
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.show_view(self.controlador.instru_view(self.card, self.personagem))

class InstruView(arcade.View):
    def __init__(self, card, personagem):
        super().__init__()
        self.ui_manager = UIManager()
        self.controlador = controller.Controller()
        self.card = card
        self.personagem = personagem
            
    def on_draw(self):
        arcade.start_render()
        self.ui_manager.purge_ui_elements()
        y_slot = self.window.height // 4
        left_column_x = self.window.width // 2
        backgound_instru = arcade.load_texture('assets/instruções.jpg')
        arcade.draw_lrwh_rectangle_textured(0, 0, self.controlador.SCREEN_WIDTH, self.controlador.SCREEN_HEIGHT, backgound_instru)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        if self.card  != None:
            choice_view = self.controlador.multi_player('assets/blue', 'assets/yellow')
            choice_view.setup(1)
            self.window.show_view(choice_view)
        else:
            if self.personagem == 1:
                choice_view = self.controlador.single_player('assets/yellow')
                choice_view.setup(1)
                self.window.show_view(choice_view)
            else:
                choice_view = self.controlador.single_player('assets/blue')
                choice_view.setup(1)
                self.window.show_view(choice_view)
    
