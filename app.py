from flask import Flask
from flask import redirect
from flask import request
from flask import render_template

app = Flask(__name__)

from inc.game import Game
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/hotseat/form', methods=['GET', 'POST'])
def solo_form():
    if request.method == 'POST':
        players = [x for x in request.form.getlist('names') if x]
        if len(players)==4:
            return solo_phase0(players)
    return render_template('hotseat/form.html')

def solo_phase0(name):
    global game
    game = Game(name)
    return redirect('/hotseat/phase1', code=302)

@app.route('/hotseat/phase1')
def hotseat_phase1():
    if len([player for player in game.players if player.count_player_cards()>0])==0 and game.round < 7:
        game.new_round()
        game.deal_cards()
        game.active_player = (game.round - 1)%4
        for player in game.players:
            player.sort_hand()
    game.table.cards = []
    return render_template('hotseat/phase1.html', game=game)

@app.route('/hotseat/table')
def table():
    if game.table.count_cards()<4:
        return render_template('hotseat/throw_card.html', game=game)
    if game.table.count_cards() == 4:
        strongest_card = game.table.cards[0]
        player_index = -1
        for card in game.table.cards:
            if card.value > strongest_card.value and card.color==game.table.cards[0].color:
                strongest_card=card
        for i in range(4):
            if strongest_card in game.players[i].thrown_cards:
                game.players[i].add_to_taken(game.table.cards)
                player_index = i
            game.players[i].thrown_cards = []
        game.active_player = player_index
        return render_template('hotseat/table.html', game=game, player_index=player_index)

@app.route('/hotseat/throw_card/<int:index>')
def throw_card(index):
    if game.table.count_cards()!=0 and game.players[game.active_player].hand[index].color!=game.table.cards[0].color:
       if [card for card in game.players[game.active_player].hand if card.color==game.table.cards[0].color]:
        return render_template('hotseat/throw_card.html', game=game)
    game.table.put_on_table(game.players[game.active_player].hand[index])
    game.players[game.active_player].add_to_thrown(game.players[game.active_player].hand[index])
    game.players[game.active_player].throw(index)
    return redirect('/hotseat/next_player', code=302)

@app.route('/hotseat/next_player')
def next_player():
    game.active_player += 1
    game.active_player %= 4
    return redirect('/hotseat/table', code=302)

if __name__ == '__main__':
    app.run(host='wierzba.wzks.uj.edu.pl', port=5103, debug=True)
