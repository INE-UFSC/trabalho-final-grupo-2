import arcade
import arcade.gui
from controller.controller import Controller
import json

from model.cards import JumpCard, SilentCard, BoxCard
from model.player import Player


class Game:
    def main(self):
        """ Main method """
        start_view = None
        controlador = Controller()
        window = arcade.Window(controlador.SCREEN_WIDTH,
                               controlador.SCREEN_HEIGHT,
                               controlador.SCREEN_TITLE)

        if start_view == None:
            start_view = controlador.return_view()
            if controlador.game is not None:
                start_view = controlador.game

        window.show_view(start_view)
        arcade.run()

if __name__ == "__main__":
    Game().main()
