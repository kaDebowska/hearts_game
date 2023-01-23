from inc.player import Player
from inc.deck import Deck
from inc.table import Table

class Game:
    def __init__(self, names, mode):
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
        self.played_cards = {
            'karo': [],
            'kier': [],
            'pik': [],
            'trefl': []

        }
        if mode == 'solo':
            first = True
            for name in names:
                if first:
                    self.players.append(Player(name, 'human'))
                    first = False
                else:
                    self.players.append(Player(name, 'computer'))
        elif mode == 'hotseat':
            for name in names:
                self.players.append(Player(name, 'human'))
        else:
            exit()

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
        for i in range(13):
            for player in self.players:
                player.add_to_hand(self.deck.deal())

    def play(self, index):
        self.table.put_on_table(self.players[self.active_player].hand[index])
        self.players[self.active_player].add_to_thrown(self.players[self.active_player].hand[index])
        self.players[self.active_player].throw(index)

    def count_played_cards(self):
        for key in self.played_cards:
            for card in self.table.cards:
                if card.color == key:
                    self.played_cards[key].append(card)
