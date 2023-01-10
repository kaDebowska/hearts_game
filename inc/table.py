class Table:
    def __init__(self):
        self.cards = []
    def put_on_table(self, card):
        self.cards.append(card)

    def count_cards(self):
        return len(self.cards)
