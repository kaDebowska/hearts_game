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
        self.rounds_names = {
            1 : 'bez lew',
            2 : 'bez kierów',
            3 : 'bez dam',
            4 : 'bez panów',
            5 : 'bez króla kier',
            6 : 'rozbójnik',
            7 : 'odgrywka'
        }
        self.rounds_points = {
            1 : self.round1,
            2 : self.round2,
            3 : self.round3,
            4 : self.round4,
            5 : self.round5,
            6 : self.round6,
            7 : self.round7
        }
        for name in names:
            self.players.append(Player(name, 'human'))

    def new_round(self):
       self.deck = Deck()
       self.round +=1

    def round1(self, idx):
        for player in self.players:
            player.round_points[idx] = int((len(player.taken_cards)/4)*(-20))
            player.total_points += player.round_points[idx]

    def round2(self, idx):
        for player in self.players:
            for card in player.taken_cards:
                if card.color == 'kier':
                    player.round_points[idx] -= 20
            player.total_points += player.round_points[idx]

    def round3(self, idx):
        for player in self.players:
            for card in player.taken_cards:
                if card.value == 12:
                    player.round_points[idx] -= 60
            player.total_points += player.round_points[idx]

    def round4(self, idx):
        for player in self.players:
            for card in player.taken_cards:
                if card.value == 11 or card.value == 13:
                    player.round_points[idx] -= 30
            player.total_points += player.round_points[idx]

    def round5(self, idx):
        for player in self.players:
            for card in player.taken_cards:
                if card.value == 13 and card.color == 'kier':
                    player.round_points[idx] -= 150
            player.total_points += player.round_points[idx]

    def round6(self, idx):
        for player in self.players:
            player.round_points[idx] = int((len(player.taken_cards) / 4) * (-20))
            for card in player.taken_cards:
                if card.color == 'kier':
                    player.round_points[idx] -= 20
                if card.value == 12:
                    player.round_points[idx] -= 60
                if card.value == 11 or card.value == 13:
                    player.round_points[idx] -= 30
                if card.value == 13 and card.color == 'kier':
                    player.round_points[idx] -= 150
            player.total_points += player.round_points[idx]

    def round7(self, idx):
        self.round6(idx)
        for player in self.players:
            player.round_points[idx] *= (-1)
            player.total_points += (2 * player.round_points[idx])


    def deal_cards(self):
        self.deck.shuffle()
        for i in range(1):
            for player in self.players:
                player.add_to_hand(self.deck.deal())

