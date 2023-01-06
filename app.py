from flask import Flask
from flask import redirect
from flask import request
from flask import render_template

import random

app = Flask(__name__)

class Card:
    def __init__(self, color, value, image='',  points=0):
        self.color = color
        self.value = value
        self.points = points
        self.image = image

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

class Player:
    def __init__(self, name='Anonymous', mode='computer'):
        self.player_name = name
        self.mode = mode
        self.hand = []
        self.taken_cards = []
        self.points = 0

    def add_to_hand(self, card):
        self.hand.append(card)

    def sort_hand(self):
        self.hand = sorted(self.hand, key=lambda card: (card.color, card.value))

    def draw(self, index):
        if self.hand:
            self.hand.pop(index)

    def count_player_cards(self):
        return len(self.hand)

class Table:
    def __init__(self):
        self.cards = []
    def put_on_table(self, card):
        self.cards.append(card)

    def count_cards(self):
        return len(self.cards)
class Game:
    def __init__(self, name='Anonymous'):
        self.players = list()
        self.players.append(Player(name, 'human')),
        self.players.append(Player('komputer1', 'computer')),
        self.players.append(Player('komputer2', 'computer')),
        self.players.append(Player('komputer3', 'computer'))
        self.active_player = 0
        self.deck = Deck()
        self.table = Table()

    def deal_cards(self):
        self.deck.shuffle()
        for i in range(13):
            for player in self.players:
                player.add_to_hand(self.deck.deal())

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/solo/form', methods=['GET', 'POST'])
def solo_form():
    if request.method == 'POST':
       return solo_phase0(request.form.get('name'))
    return render_template('solo/form.html')

def solo_phase0(name):
    global game
    game = Game(name)
    return redirect('/solo/phase1', code=302)

@app.route('/solo/phase1')
def solo_phase1():
    game.deal_cards()
    for player in game.players:
        player.sort_hand()
    return render_template('solo/phase1.html', game=game)

@app.route('/solo/table')
def table():
    if game.table.count_cards()<4:
        return render_template('solo/throw_card.html', game=game)
    else:
        return render_template('solo/table.html', game=game)
@app.route('/solo/throw_card/<int:index>')
def throw_card(index):
    if game.table.count_cards()!=0 and game.players[game.active_player].hand[index].color!=game.table.cards[0].color:
       if [card for card in game.players[game.active_player].hand if card.color==game.table.cards[0].color]:
        return render_template('solo/throw_card.html', game=game)
    game.table.put_on_table(game.players[game.active_player].hand[index])
    game.players[game.active_player].draw(index)
    return redirect('/solo/next_player', code=302)

@app.route('/solo/next_player')
def next_player():
    game.active_player += 1
    game.active_player %= 4
    return redirect('/solo/table', code=302)

if __name__ == '__main__':
    app.run(host='wierzba.wzks.uj.edu.pl', port=5103, debug=True)
