from views import InitView, ChoiceView, FinishView
import single_player

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

        return ChoiceView()

    def finish_view(self):

        return FinishView()

    def single_player(self, spritesheet: str):
        return single_player.SinglePlayerGame(spritesheet)

    def multi_player(self, spritesheet: str):
        ''' implementar '''
        pass