import arcade
import arcade.gui
from controller import Controller


class Game:
    def main(self):
        """ Main method """
        controlador = Controller()
        window = arcade.Window(controlador.SCREEN_WIDTH,
                               controlador.SCREEN_HEIGHT,
                               controlador.SCREEN_TITLE)
        start_view = controlador.init_view()
        if controlador.game is not None:
            start_view = controlador.game

        window.show_view(start_view)
        arcade.run()

if __name__ == "__main__":
    Game().main()
