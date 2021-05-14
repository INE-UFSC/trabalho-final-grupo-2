from views import init_view, setup_views
from game.single_player import SinglePlayerGame
from game.multi_player import MultiPlayerGame
from model.cards import BoxCard, SaveCard, SilentCard, JumpCard
from views.choice_cards_view import SelectCardsView
from views.finish_view import FinishView
from views.return_view import ReturnView


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

    def return_view(self):
        return ReturnView()

    def init_view(self):
        '''@return InitView'''
        return init_view.InitView(self)

    def choice_view(self):
        '''@return ChoiceView'''
        return setup_views.ChoiceView()

    def finish_view(self, mensagem):
        return FinishView(mensagem)
    
    def card_view(self, personagem):
        '''@return CardView'''
        return setup_views.CardView(personagem)
    
    def instru_view(self):
        '''@return InstruView'''
        return setup_views.InstruView()

    def get_all_cards(self) -> list:
        '''@return all possible cards: list'''
        return [JumpCard(), SaveCard(), BoxCard(), SilentCard()]

    def add_card_to_player(self, player):
        pass

    def select_cards_view(self):
        return SelectCardsView()

    def single_player(self, spritesheet: str):
        '''@return SinglePlayerGame'''
        return SinglePlayerGame(spritesheet)

    def multi_player(self, spritesheet_one: str, spritesheet_two: str):
        '''@return MultiPlayerGame'''
        return MultiPlayerGame(spritesheet_one, spritesheet_two)

    def select_cards_view(self):
        return SelectCardsView()

class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    def some_business_logic(self):
        """
        Finally, any singleton should define some business logic, which can be
        executed on its instance.
        """

        # ...


if __name__ == "__main__":
    # The client code.

    s1 = Singleton()
    s2 = Singleton()

    if id(s1) == id(s2):
        print("Singleton works, both variables contain the same instance.")
    else:
        print("Singleton failed, variables contain different instances.")