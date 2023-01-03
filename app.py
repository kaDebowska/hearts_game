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

    def add_to_hand(self, card):
        self.hand.append(card)

    def sort_hand(self):
        self.hand = sorted(self.hand, key=lambda card: (card.color, card.value))


class Game:
    def __init__(self, name='Anonymous'):
        self.players = list()
        self.players.append(Player(name, 'human')),
        self.players.append(Player('komputer1', 'computer')),
        self.players.append(Player('komputer2', 'computer')),
        self.players.append(Player('komputer3', 'computer'))
        self.active_player = 0
        self.deck = Deck()

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
    game.players[game.active_player].sort_hand()
    return render_template('solo/phase1.html', game=game)


if __name__ == '__main__':
    app.run(host='wierzba.wzks.uj.edu.pl', port=5103, debug=True)
