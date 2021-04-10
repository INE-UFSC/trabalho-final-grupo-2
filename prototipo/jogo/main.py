import arcade
import arcade.gui
import constants
from views import InitView 

def main():
    """ Main method """

    window = arcade.Window(constants.Constants().SCREEN_WIDTH, constants.Constants().SCREEN_HEIGHT, constants.Constants().SCREEN_TITLE)
    start_view = InitView()
    if constants.Constants().game is not None:
        start_view = constants.Constants().game

    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
