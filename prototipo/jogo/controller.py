from views import InitView, ChoiceView, FinishView, CardView, InstruView
from single_player import SinglePlayerGame
from multi_player import MultiPlayerGame


class Controller:
    def __init__(self):
        self.SPRITE_SCALING_PLAYER = 0.5

        self.SCREEN_WIDTH = 1366
        self.SCREEN_HEIGHT = 768
        self.SCREEN_TITLE = "PyCharmers"
        # Movement speed of player, in pixels per frame
        self.PLAYER_MOVEMENT_SPEED = 10
        self.GRAVITY = 1
        self.PLAYER_JUMP_SPEED = 20
        self.game = None

    def init_view(self):
        '''@return InitView'''
        return InitView()

    def choice_view(self):
        '''@return ChoiceView'''
        return ChoiceView()

    def finish_view(self):
        '''@return FinishView'''
        return FinishView()
    
    def card_view(self, card, personagem):
        '''@return CardView'''
        return CardView(card, personagem)
    
    def instru_view(self, card, personagem):
        '''@return InstruView'''
        return InstruView(card, personagem)

    def add_card_to_player(self, player):
        pass

    def single_player(self, spritesheet: str):
        '''@return SinglePlayerGame'''
        return SinglePlayerGame(spritesheet)

    def multi_player(self, spritesheet_one: str, spritesheet_two: str):
        '''@return MultiPlayerGame'''
        return MultiPlayerGame(spritesheet_one, spritesheet_two)
