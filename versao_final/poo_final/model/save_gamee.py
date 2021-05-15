import json

import controller.controller
from model.cards import JumpCard, SilentCard, BoxCard, SaveCard
from model.player import Player


class SaveMultiPlayer:
    def __init__(self, controller, player1 = None, player2 = None, nivel = None):
        self.__player1 = player1
        self.__player2 = player2
        self.__nivel = nivel
        self.controlador = controller

    def save(self):
        dict = {
            "mode":"multiplayer",
            "Player1_score": self.__player1.state().score,
            "Player2_score": self.__player2.state().score,
            "Nivel": self.__nivel,
            "Player1_savex": self.__player1.player_sprite.center_x,
            "Player1_savey":self.__player1.player_sprite.center_y,
            "Player1_cards": [str(self.__player1.deck().cards()[0]), str(self.__player1.deck().cards()[1])],
            "Player2_savex": self.__player2.player_sprite.center_x,
            "Player2_savey": self.__player2.player_sprite.center_y,
            "Player2_cards": [str(self.__player2.deck().cards()[0]), str(self.__player2.deck().cards()[1])],
        }
        with open(f"save.json", "w") as arq:
            json_dump = json.dumps(dict)
            arq.write(json_dump)

    def return_game(self, dict):
        p1 = Player('assets/yellow')
        p2 = Player('assets/blue')
        p1.state().volta_score(dict["Player1_score"])
        p2.state().volta_score(dict["Player2_score"])
        if "Jump" in dict["Player1_cards"][0]:
            p1.deck().add_card(JumpCard())
        if "Silent" in dict["Player1_cards"][0]:
            p1.deck().add_card(SilentCard())
        if "Box" in dict["Player1_cards"][0]:
            p1.deck().add_card(BoxCard())
        if "Save" in dict["Player1_cards"][0]:
            p1.deck().add_card(SaveCard())

        if "Jump" in dict["Player1_cards"][1]:
            p1.deck().add_card(JumpCard())
        if "Silent" in dict["Player1_cards"][1]:
            p1.deck().add_card(SilentCard())
        if "Box" in dict["Player1_cards"][1]:
            p1.deck().add_card(BoxCard())
        if "Save" in dict["Player1_cards"][1]:
            p1.deck().add_card(SaveCard())

        if dict["Player2_cards"][0] == "Jump":
            p2.deck().add_card(JumpCard())
        if dict["Player2_cards"][0] == "Silent":
            p2.deck().add_card(SilentCard())
        if dict["Player2_cards"][0]  == "Box":
            p2.deck().add_card(BoxCard())
        if dict["Player2_cards"][0] == "Save":
            p2.deck().add_card(SaveCard())
        if  dict["Player2_cards"][1] == "Jump":
            p2.deck().add_card(JumpCard())
        if dict["Player2_cards"][1] == "Silent":
            p2.deck().add_card(SilentCard())
        if  dict["Player2_cards"][1] == "Box":
            p2.deck().add_card(BoxCard())
        if  dict["Player2_cards"][1] == "Save":
            p2.deck().add_card(SaveCard())

        start_view = self.controlador.multi_player(p2, p1)
        start_view.setup(dict["Nivel"], dict["Player1_savex"], dict["Player2_savex"], dict["Player1_savey"],
                         dict["Player2_savey"])
        return start_view


class SaveSinglePlayer:
    def __init__(self,controller,  player = None, nivel = None):
        self.__player = player
        self.__nivel = nivel
        self.controlador = controller

    def save(self):
        dict = {
            "mode":"singleplayer",
            "player_front":self.__player.image_source,
            "Player_score": self.__player.state().score,
            "Nivel": self.__nivel,
            "Player_savex": self.__player.player_sprite.center_x,
            "Player_savey":self.__player.player_sprite.center_y
        }
        with open(f"save.json", "w") as arq:
            json_dump = json.dumps(dict)
            arq.write(json_dump)

    def return_game(self, dict):
        player = Player(dict["player_front"])
        player.state().volta_score(dict["Player_score"])
        single = self.controlador.single_player(player)
        single.setup(dict["Nivel"], dict["Player_savex"], dict["Player_savey"])
        return single
