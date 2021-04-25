import arcade
import arcade.gui
#import constants
from controller import Controller


class Game:


    def main(self):
        """ Main method """

        window = arcade.Window(Controller().SCREEN_WIDTH, Controller().SCREEN_HEIGHT, Controller().SCREEN_TITLE)
        start_view = Controller().init_view()
        if Controller().game is not None:
            start_view = Controller().game

        window.show_view(start_view)
        arcade.run()


if __name__ == "__main__":
    Game().main()
