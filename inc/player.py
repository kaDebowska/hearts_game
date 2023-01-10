class Player:
    def __init__(self, name='Anonymous', mode='computer'):
        self.name = name
        self.mode = mode
        self.hand = []
        self.taken_cards = []
        self.thrown_cards = []
        self.points = 0

    def add_to_hand(self, card):
        self.hand.append(card)

    def add_to_thrown(self, card):
        self.thrown_cards.append(card)

    def add_to_taken(self,cards):
        self.taken_cards.extend(cards)

    def sort_hand(self):
        self.hand = sorted(self.hand, key=lambda card: (card.color, card.value))

    def throw(self, index):
        if self.hand:
            self.hand.pop(index)

    def count_player_cards(self):
        return len(self.hand)
