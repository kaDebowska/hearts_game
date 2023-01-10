from inc.player import Player
from inc.deck import Deck
from inc.table import Table

class Game:
    def __init__(self, names):
        self.players = list()
        self.active_player = 0
        self.deck = Deck()
        self.table = Table()
        for name in names:
            self.players.append(Player(name, 'human'))

    def new_round(self):
       self.deck = Deck()

    def deal_cards(self):
        self.deck.shuffle()
        for i in range(3):
            for player in self.players:
                player.add_to_hand(self.deck.deal())
