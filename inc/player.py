
class Player:
    def __init__(self, name='Anonymous', mode='computer'):
        self.name = name
        self.mode = mode
        self.hand = []
        self.taken_cards = []
        self.thrown_cards = []
        self.round_points = [0,0,0,0,0,0,0]
        self.total_points = 0
        self.tactic_have_color = {
            1: self.have_color1,
            2: self.have_color2,
            3: self.have_color3,
            4: self.have_color4,
            5: self.have_color5,
            6: self.have_color1,
            7: self.have_color7
        }
        self.tactic_lack_of_color = {
            1: self.lack_of_color1,
            2: self.lack_of_color2,
            3: self.lack_of_color3,
            4: self.lack_of_color4,
            5: self.lack_of_color5,
            6: self.lack_of_color6,
            7: self.lack_of_color7
        }
        self.tactic_start = {
            1: self.start,
            2: self.start2,
            3: self.start,
            4: self.start,
            5: self.start,
            6: self.start,
            7: self.start7

        }

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

    def count_by_color(self, color):
        n = 0
        for card in self.hand:
            if card.color == color:
                n += 1
        return n
    def min_color(self, color):
        min_card = self.hand[0]
        for card in self.hand:
            if card.color == color:
                if card.value < min_card.value:
                    min_card=card
        return min_card

    def max_color(self, color):
        max_card = self.hand[0]
        for card in self.hand:
            if card.color == color:
                if card.value > max_card.value:
                    max_card=card
        return max_card
    def lack_of_color1(self):
        colors_count={}
        for color in ['karo', 'kier', 'pik', 'trefl']:
            if self.count_by_color(color)>0:
                colors_count[color]=self.count_by_color(color)
        choosen_color=min(colors_count, key=colors_count.get)
        choosen_card=self.max_color(choosen_color)
        return self.hand.index(choosen_card)

    def lack_of_color2(self):
        if self.count_by_color('kier') > 0:
            choosen_card = self.max_color('kier')
            index =  self.hand.index(choosen_card)
        else:
          index =  self.lack_of_color1()
        return index

    def lack_of_color3(self):
        for card in self.hand:
            if card.value == 12:
                choosen_card=card
                index = self.hand.index(choosen_card)
                return index
        index = self.lack_of_color1()
        return index

    def lack_of_color4(self):
        for card in self.hand:
            if card.value == 13:
                choosen_card=card
                index = self.hand.index(choosen_card)
                return index
            elif card.value == 11:
                choosen_card = card
                index = self.hand.index(choosen_card)
                return index
        index = self.lack_of_color1()
        return index

    def lack_of_color5(self):
        for card in self.hand:
            if card.value == 13 and card.color == 'kier':
                choosen_card=card
                index = self.hand.index(choosen_card)
                return index
        index = self.lack_of_color1()
        return index

    def lack_of_color6(self):
        for card in self.hand:
            if card.color == 'kier':
                if card.value == 13:
                    choosen_card=card
                    return self.hand.index(choosen_card)
                if card.value == 12:
                    choosen_card = card
                    return self.hand.index(choosen_card)
                if card.value == 11:
                    choosen_card = card
                    return self.hand.index(choosen_card)
            if card.value == 12:
                if card.value == 12:
                    choosen_card = card
                    return self.hand.index(choosen_card)
            if card.value == 13:
                choosen_card = card
                return self.hand.index(choosen_card)
            if card.value == 11:
                choosen_card = card
                return self.hand.index(choosen_card)
            if card.color == 'kier':
                choosen_card = self.max_color('kier')
                return self.hand.index(choosen_card)
        index = self.lack_of_color1()
        return index

    def lack_of_color7(self):
        colors_count = {}
        colors = ['karo', 'pik', 'trefl']
        for color in colors:
            if self.count_by_color(color) > 0:
                colors_count[color] = self.count_by_color(color)
        if len(colors_count) == 0:
            choosen_card = self.min_color('kier')
        else:
            choosen_color = max(colors_count, key=colors_count.get)
            choosen_card = self.min_color(choosen_color)
        return self.hand.index(choosen_card)


    def have_color1(self, table, card):
        index = self.hand.index(card)
        i = index
        strongest = 0
        for c in table:
            if c.value > strongest:
                strongest=c.value
        while self.hand[index].color == table[0].color and self.hand[index].value < strongest:
            if index < self.count_player_cards() - 2:
                index += 1
            break
        if i != index and index > 0:
            index -= 1
        if len(table)==3 and self.hand[index].value > strongest:
            index = self.hand.index(self.max_color(card.color))
        return index

    def have_color2(self, table, card):
        if [x for x in table if x.color == 'kier']:
           index = self.have_color1(table, card)
        else:
            index = self.hand.index(self.max_color(card.color))
        return index

    def have_color3(self, table, card):
        if [x for x in table if x.value == 12]:
            index = self.hand.index(self.min_color(card.color))
        else:
            index = self.hand.index(self.max_color(card.color))
            while self.hand[index].value >= 12 and self.hand[index].color == card.color and index > 0:
                index -= 1
            if self.hand[index].color != card.color:
                index += 1
        return index

    def have_color4(self, table, card):
        if [x for x in table if x.value == 13 or x.value == 11]:
            index = self.hand.index(self.min_color(card.color))
        else:
            index = self.hand.index(self.max_color(card.color))
            while self.hand[index].value >= 11 and self.hand[index].color == card.color and index > 0:
                index -= 1
            if self.hand[index].color != card.color:
                index +=1
        return index

    def have_color5(self, table, card):
        if [x for x in table if x.value == 13 or x.color == 'kier'] or len(table) < 3:
            index = self.have_color1(table, card)
        else:
            index = self.hand.index(self.max_color(card.color))
        return index

    def have_color7(self, table, card, played_cards):
        index = self.hand.index(card)
        strongest = 0
        for c in table:
            if c.value > strongest:
                strongest=c.value
        while self.hand[index].color == table[0].color and self.hand[index].value < strongest:
            if index < self.count_player_cards() - 2:
                index += 1
            break
        if len(table) < 3 and self.max_color(card.color) != 13:
            i = 0
            diff = 13 - self.max_color(card.color).value
            for card in played_cards[card.color]:
                if card.value > self.hand[index].value:
                    i += 1
            if i != diff:
                index = self.hand.index(self.min_color(card.color))

        return index
    def start(self, played_cards):
        colors_count = {}
        all_colors = ['karo', 'kier', 'pik', 'trefl']
        colors = all_colors.copy()
        for i in range(len(colors)):
            if len(played_cards[colors[i]]) + self.count_by_color(colors[i]) == 13:
                colors[i] = 0
        colors = [i for i in colors if i != 0]
        if len(colors) == 0 or len([x for x in self.hand if x.color in colors]) == 0:
            colors = all_colors
        for color in colors:
            if self.count_by_color(color) > 0:
                colors_count[color] = self.count_by_color(color)
        choosen_color = min(colors_count, key=colors_count.get)
        choosen_card = self.min_color(choosen_color)
        if choosen_card.value > 10:
            options = []
            for color in colors:
                options.append(self.min_color(color))
            options = sorted(options, key=lambda card: card.value)
            choosen_card=options[0]
        return self.hand.index(choosen_card)

    def start2(self, played_cards):
        index = self.start(played_cards)
        all_colors = ['karo', 'kier', 'pik', 'trefl']
        colors = all_colors.copy()
        if self.hand[index].color == 'kier' and self.hand[index].value > 4:
            colors.remove('kier')
            if len(colors) == 0:
                return index
            colors_count = {}
            for i in range(len(colors)):
                if len(played_cards[colors[i]]) + self.count_by_color(colors[i]) == 13:
                    colors[i] = 0
            colors = [i for i in colors if i != 0]
            if len(colors) == 0 or len([x for x in self.hand if x.color in colors]) == 0:
                colors = all_colors
            for color in colors:
                if self.count_by_color(color) > 0:
                    colors_count[color] = self.count_by_color(color)
            choosen_color = min(colors_count, key=colors_count.get)
            if len(played_cards[choosen_color]) < 10 and self.count_by_color(choosen_color) < 5:
                choosen_card = self.max_color(choosen_color)
                index = self.hand.index(choosen_card)
            else:
                choosen_card = self.min_color(choosen_color)
                index = self.hand.index(choosen_card)
        return index

    def start7(self, played_cards):
        choosen_card = None
        i = 0
        diff = 0
        colors_count = {}
        all_colors = ['karo', 'kier', 'pik', 'trefl']
        colors = all_colors.copy()
        for color in colors:
            if len(played_cards[color]) + self.count_by_color(color) == 13:
                choosen_card = self.min_color(color)
                return self.hand.index(choosen_card)
        for color in colors:
            if self.count_by_color(color) > 0:
                colors_count[color] = self.count_by_color(color)
        for key in colors_count:
            choosen_card = self.max_color(key)
            i = 0
            diff = 13 - choosen_card.value
            for card in played_cards[key]:
                if card.value > choosen_card.value:
                    i += 1
            if i == diff:
                break
        if i != diff:
            choosen_color = max(colors_count, key=colors_count.get)
            choosen_card = self.max_color(choosen_color)
        return self.hand.index(choosen_card)