from inc.card import Card
import random
minCardVal = 2
maxCardVal = 15

class Deck:
    def __init__(self):
        self.deck = []
        self.cards_colors = ('karo', 'kier', 'pik', 'trefl')
        for i in range(minCardVal, maxCardVal):
            for color in self.cards_colors:
                self.deck.append(Card(color, i, image=f'{i}_{color}.png'))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
      return self.deck.pop(0)
