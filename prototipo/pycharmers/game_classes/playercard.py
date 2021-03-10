from card import Card


class PlayerCard:
    def __init__(self, deck: list[Card], hand: list[Card], selected_card=None):
        self.__deck = deck
        self.__hand = hand
        self.__selected_card = selected_card
# implementar o resto quando testarmos as cartas
