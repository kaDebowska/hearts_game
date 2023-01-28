from flask import Flask
from flask import redirect
from flask import request
from flask import render_template

app = Flask(__name__)

from inc.game import Game
@app.route('/')
def home():
    return render_template('home.html')

#  SOLO ########################################################################################

@app.route('/solo/form', methods=['GET', 'POST'])
def solo_form():
    if request.method == 'POST':
        players = [x for x in request.form.getlist('names') if x]
        if len(players)==4:
            return solo_new_game(players)
    return render_template('solo/form.html')

def solo_new_game(name):
    global game
    game = Game(name, 'solo')
    return redirect('/solo/phase1', code=302)


@app.route('/solo/phase1')
def solo_phase1():
    if (len([player for player in game.players if player.count_player_cards() > 0])==0 and 7 >= game.round) or game.round==0:
        return redirect('/solo/end_of_round', code=302)
    if game.table.count_cards() == 4:
        game.table.cards = []
    if game.players[game.active_player].mode == 'computer':
        if game.table.count_cards() != 0:
            for card in game.players[game.active_player].hand:
                if card.color == game.table.cards[0].color:
                    if game.round == 7:
                        index = game.players[game.active_player].tactic_have_color[game.round](game.table.cards, card, game.played_cards)
                        game.play(index)
                        return redirect('/solo/next_player', code=302)
                    index = game.players[game.active_player].tactic_have_color[game.round](game.table.cards, card)
                    game.play(index)
                    return redirect('/solo/next_player', code=302)
            index = game.players[game.active_player].tactic_lack_of_color[game.round]()
            game.play(index)
            return redirect('/solo/next_player', code=302)
        else:
            index = game.players[game.active_player].tactic_start[game.round](game.played_cards)
            game.play(index)

            return redirect('/solo/next_player', code=302)
    else:
        return render_template('solo/throw_card.html', game=game)

@app.route('/solo/throw_card/<int:index>')
def solo_throw_card(index):
    if game.table.count_cards()!=0 and game.players[game.active_player].hand[index].color!=game.table.cards[0].color:
       if [card for card in game.players[game.active_player].hand if card.color==game.table.cards[0].color]:
        return render_template('solo/throw_card.html', game=game)
    game.play(index)
    return redirect('/solo/next_player', code=302)

@app.route('/solo/table')
def solo_table():
    if game.table.count_cards()<4:
        return redirect('/solo/phase1', code=302)
    else:
        game.count_played_cards()
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
        return render_template('solo/table.html', game=game, player_index=player_index)

@app.route('/solo/end_of_round')
def solo_end_of_round():
    if game.round ==0:
        game.new_round()
        game.deal_cards()
        for player in game.players:
            player.sort_hand()
        return redirect('/solo/phase1', code=302)
    game.rounds_points[game.round](game.round-1)
    for player in game.players:
        player.hand = []
    if game.round < 7:
        game.new_round()
        game.deal_cards()
        game.active_player = (game.round - 1) % 4
        for player in game.players:
            player.taken_cards = []
            player.sort_hand()
        return render_template('solo/end_of_round.html', game=game)
    else:
        return redirect('/solo/end_of_game', code=302)

@app.route('/solo/end_of_game')
def solo_end_of_game():
    winners = []
    max_points = 0
    for player in game.players:
        if player.total_points > max_points:
            max_points = player.total_points
            winners = [player]
        elif player.total_points == max_points:
            winners.append(player)
    return render_template('solo/end_of_game.html', game=game, winners=winners)

@app.route('/solo/next_player')
def solo_next_player():
    game.active_player += 1
    game.active_player %= 4
    return redirect('/solo/table', code=302)

# HOTSEAT ##################################################################################
@app.route('/hotseat/form', methods=['GET', 'POST'])
def hotseat_form():
    if request.method == 'POST':
        players = [x for x in request.form.getlist('names') if x]
        if len(players)==4:
            return hotseat_new_game(players)
    return render_template('hotseat/form.html')

def hotseat_new_game(name):
    global game
    game = Game(name, 'hotseat')
    return redirect('/hotseat/phase1', code=302)

@app.route('/hotseat/phase1')
def hotseat_phase1():
    if game.round ==0:
        game.new_round()
        game.deal_cards()
        for player in game.players:
            player.sort_hand()
    if len([player for player in game.players if player.count_player_cards() > 0])==0 and 7 >= game.round > 0:
        return redirect('/hotseat/end_of_round', code=302)
    game.table.cards = []
    return render_template('hotseat/throw_card.html', game=game)

@app.route('/hotseat/table')
def hotseat_table():
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
def hotseat_throw_card(index):
    if game.table.count_cards()!=0 and game.players[game.active_player].hand[index].color!=game.table.cards[0].color:
       if [card for card in game.players[game.active_player].hand if card.color==game.table.cards[0].color]:
        return render_template('hotseat/throw_card.html', game=game)
    game.table.put_on_table(game.players[game.active_player].hand[index])
    game.players[game.active_player].add_to_thrown(game.players[game.active_player].hand[index])
    game.players[game.active_player].throw(index)
    return redirect('/hotseat/next_player', code=302)

@app.route('/hotseat/end_of_round')
def hotseat_end_of_round():
    game.rounds_points[game.round](game.round-1)
    for player in game.players:
        player.hand = []
    if game.round < 7:
        game.new_round()
        game.deal_cards()
        game.active_player = (game.round - 1) % 4
        for player in game.players:
            player.taken_cards = []
            player.sort_hand()
        return render_template('hotseat/end_of_round.html', game=game)
    else:
        return redirect('/hotseat/end_of_game', code=302)

@app.route('/hotseat/end_of_game')
def hotsea_end_of_game():
    winners = []
    max_points = 0
    for player in game.players:
        if player.total_points > max_points:
            max_points = player.total_points
            winners = [player]
        elif player.total_points == max_points:
            winners.append(player)
    return render_template('hotseat/end_of_game.html', game=game, winners=winners)

@app.route('/hotseat/next_player')
def hotsea_next_player():
    game.active_player += 1
    game.active_player %= 4
    return redirect('/hotseat/table', code=302)

if __name__ == '__main__':
    app.run(host='wierzba.wzks.uj.edu.pl', port=5103, debug=True)

