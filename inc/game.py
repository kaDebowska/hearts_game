from inc.player import Player
from inc.deck import Deck
from inc.table import Table

class Game:
    def __init__(self, names):
        self.players = list()
        self.active_player = 0
        self.deck = Deck()
        self.table = Table()
        self. round = 0
        self.rounds = {
            1 : 'bez lew',
            2 : 'bez kierów',
            3 : 'bez dam',
            4 : 'bez panów',
            5 : 'bez króla kier',
            6 : 'rozbójnik',
            7 : 'odgrywka'
        }
        for name in names:
            self.players.append(Player(name, 'human'))

    def new_round(self):
       self.deck = Deck()
       self.round +=1

    def deal_cards(self):
        self.deck.shuffle()
        for i in range(13):
            for player in self.players:
                player.add_to_hand(self.deck.deal())
