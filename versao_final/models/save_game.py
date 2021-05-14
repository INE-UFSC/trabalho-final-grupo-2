import json


class SaveMultiPlayer:
    def __init__(self, player1, player2, nivel):
        self.__player1 = player1
        self.__player2 = player2
        self.__nivel = nivel

    def save(self):
        dict = {
            "Player1_score": self.__player1.score,
            "Player2_score": self.__player2.score,
            "Nivel": self.__nivel,
            "Player1_savex": self.__player1.player_sprite.center_x,
            "Player1_savey":self.__player1.player_sprite.center_y,
            "Player1_cards": [str(self.__player1.cards[0]), str(self.__player1.cards[1])],
            "Player2_savex": self.__player2.player_sprite.center_x,
            "Player2_savey": self.__player2.player_sprite.center_y,
            "Player2_cards": [str(self.__player2.cards[0]), str(self.__player2.cards[1])],
        }
        with open(f"save.json", "w") as arq:
            json_dump = json.dumps(dict)
            arq.write(json_dump)
