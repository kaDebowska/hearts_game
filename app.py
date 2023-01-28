from flask import Flask
from flask import redirect
from flask import request
from flask import render_template
from flask import session
import uuid

app = Flask(__name__)
app.secret_key = 'v%Ftf2Sf3yl7'

games = {}
multiplayer_games = {}

from inc.game import Game


@app.route('/')
def home():
    if 'key' not in session:
        session['key'] = uuid.uuid4()
    return render_template('home.html')

def check_simple():
    if session.get('key') and 'games' in globals():
        return True
    return False

def check():
    if session.get('key') and 'games' in globals() and session.get('key') in games:
        return True
    return False

#  SOLO ########################################################################################

@app.route('/solo/form', methods=['GET', 'POST'])
def solo_form():
    if not check_simple():
        return redirect('/', code=302)
    if request.method == 'POST':
        players = [x for x in request.form.getlist('names') if x]
        if len(players) == 4:
            return solo_new_game(players)
    return render_template('solo/form.html')


def solo_new_game(name):
    if not check_simple():
        return redirect('/', code=302)
    games[session['key']] = Game(name, 'solo')
    return redirect('/solo/phase1', code=302)


@app.route('/solo/phase1')
def solo_phase1():
    if not check():
        return redirect('/', code=302)
    if len([player for player in games[session['key']] .players if player.count_player_cards() > 0]) == 0 and games[session['key']] .round <= 7:
        return redirect('/solo/end_of_round', code=302)
    if games[session['key']] .table.count_cards() == 4:
        games[session['key']] .table.cards = []
    if games[session['key']] .players[games[session['key']] .active_player].mode == 'computer':
        if games[session['key']] .table.count_cards() != 0:
            for card in games[session['key']] .players[games[session['key']] .active_player].hand:
                if card.color == games[session['key']] .table.cards[0].color:
                    if games[session['key']] .round == 7:
                        index = games[session['key']] .players[games[session['key']] .active_player].tactic_have_color[games[session['key']] .round](games[session['key']] .table.cards, card,
                                                                                               games[session['key']] .played_cards)
                        games[session['key']] .play(index)
                        return redirect('/solo/next_player', code=302)
                    index = games[session['key']] .players[games[session['key']] .active_player].tactic_have_color[games[session['key']] .round](games[session['key']] .table.cards, card)
                    games[session['key']] .play(index)
                    return redirect('/solo/next_player', code=302)
            index = games[session['key']] .players[games[session['key']] .active_player].tactic_lack_of_color[games[session['key']] .round]()
            games[session['key']] .play(index)
            return redirect('/solo/next_player', code=302)
        else:
            index = games[session['key']] .players[games[session['key']] .active_player].tactic_start[games[session['key']] .round](games[session['key']] .played_cards)
            games[session['key']] .play(index)

            return redirect('/solo/next_player', code=302)
    else:
        return render_template('solo/throw_card.html', game=games[session['key']] )


@app.route('/solo/throw_card/<int:index>')
def solo_throw_card(index):
    if not check():
        return redirect('/', code=302)
    if games[session['key']] .table.count_cards() != 0 and games[session['key']].players[games[session['key']].active_player].hand[index].color != games[session['key']].table.cards[0].color:
        if [card for card in games[session['key']] .players[games[session['key']] .active_player].hand if card.color == games[session['key']] .table.cards[0].color]:
            return render_template('solo/throw_card.html', game=games[session['key']])
    games[session['key']].play(index)
    return redirect('/solo/next_player', code=302)


@app.route('/solo/table')
def solo_table():
    if not check():
        return redirect('/', code=302)
    if games[session['key']].table.count_cards() < 4:
        return redirect('/solo/phase1', code=302)
    else:
        games[session['key']].count_played_cards()
        strongest_card = games[session['key']].table.cards[0]
        player_index = -1
        for card in games[session['key']].table.cards:
            if card.value > strongest_card.value and card.color == games[session['key']].table.cards[0].color:
                strongest_card = card
        for i in range(4):
            if strongest_card in games[session['key']].players[i].thrown_cards:
                games[session['key']].players[i].add_to_taken(games[session['key']].table.cards)
                player_index = i
            games[session['key']].players[i].thrown_cards = []
        games[session['key']].active_player = player_index
        return render_template('solo/table.html', game=games[session['key']], player_index=player_index)


@app.route('/solo/end_of_round')
def solo_end_of_round():
    if not check():
        return redirect('/', code=302)
    if games[session['key']].round == 0:
        games[session['key']].new_round()
        games[session['key']].deal_cards()
        for player in games[session['key']].players:
            player.sort_hand()
        return redirect('/solo/phase1', code=302)
    games[session['key']].rounds_points[games[session['key']].round](games[session['key']].round - 1)
    for player in games[session['key']].players:
        player.hand = []
    if games[session['key']].round < 7:
        games[session['key']].new_round()
        games[session['key']].deal_cards()
        games[session['key']].active_player = (games[session['key']].round - 1) % 4
        for player in games[session['key']].players:
            player.taken_cards = []
            player.sort_hand()
        return render_template('solo/end_of_round.html', game=games[session['key']])
    else:
        return redirect('/solo/end_of_game', code=302)


@app.route('/solo/end_of_game')
def solo_end_of_game():
    if not check():
        return redirect('/', code=302)
    winners = []
    max_points = 0
    for player in games[session['key']].players:
        if player.total_points > max_points:
            max_points = player.total_points
            winners = [player]
        elif player.total_points == max_points:
            winners.append(player)
    return render_template('solo/end_of_game.html', game=games[session['key']], winners=winners)


@app.route('/solo/next_player')
def solo_next_player():
    if not check():
        return redirect('/', code=302)
    games[session['key']].active_player += 1
    games[session['key']].active_player %= 4
    return redirect('/solo/table', code=302)


# HOTSEAT ##################################################################################
@app.route('/hotseat/form', methods=['GET', 'POST'])
def hotseat_form():
    if not check_simple():
        return redirect('/', code=302)
    if request.method == 'POST':
        players = [x for x in request.form.getlist('names') if x]
        if len(players) == 4:
            return hotseat_new_game(players)
    return render_template('hotseat/form.html')

def hotseat_new_game(name):
    if not check_simple():
        return redirect('/', code=302)
    games[session['key']] = Game(name, 'hotseat')
    return redirect('/hotseat/phase1', code=302)

@app.route('/hotseat/phase1')
def hotseat_phase1():
    if not check():
        return redirect('/', code=302)
    if len([player for player in games[session['key']].players if player.count_player_cards() > 0]) == 0 and games[session['key']].round <= 7:
        return redirect('/solo/end_of_round', code=302)
    if games[session['key']].table.count_cards() == 4:
        games[session['key']].table.cards = []
    return render_template('hotseat/throw_card.html', game=games[session['key']])

@app.route('/hotseat/throw_card/<int:index>')
def hotseat_throw_card(index):
    if not check():
        return redirect('/', code=302)
    if games[session['key']].table.count_cards() != 0 and games[session['key']].players[games[session['key']].active_player].hand[index].color != games[session['key']].table.cards[0].color:
        if [card for card in games[session['key']].players[games[session['key']].active_player].hand if card.color == games[session['key']].table.cards[0].color]:
            return render_template('hotseat/throw_card.html', game=games[session['key']])
    games[session['key']].play(index)
    return redirect('/hotseat/next_player', code=302)
@app.route('/hotseat/table')
def hotseat_table():
    if not check():
        return redirect('/', code=302)
    if games[session['key']].table.count_cards() < 4:
        return render_template('hotseat/throw_card.html', game=games[session['key']])
    if games[session['key']].table.count_cards() == 4:
        strongest_card = games[session['key']].table.cards[0]
        player_index = -1
        for card in games[session['key']].table.cards:
            if card.value > strongest_card.value and card.color == games[session['key']].table.cards[0].color:
                strongest_card = card
        for i in range(4):
            if strongest_card in games[session['key']].players[i].thrown_cards:
                games[session['key']].players[i].add_to_taken(games[session['key']].table.cards)
                player_index = i
            games[session['key']].players[i].thrown_cards = []
        games[session['key']].active_player = player_index
        return render_template('hotseat/table.html', game=games[session['key']], player_index=player_index)


@app.route('/hotseat/end_of_round')
def hotseat_end_of_round():
    if not check():
        return redirect('/', code=302)
    if games[session['key']].round == 0:
        games[session['key']].new_round()
        games[session['key']].deal_cards()
        for player in games[session['key']].players:
            player.sort_hand()
        return redirect('/hotseat/phase1', code=302)
    games[session['key']].rounds_points[games[session['key']].round](games[session['key']].round-1)
    for player in games[session['key']].players:
        player.hand = []
    if games[session['key']].round < 7:
        games[session['key']].new_round()
        games[session['key']].deal_cards()
        games[session['key']].active_player = (games[session['key']].round - 1) % 4
        for player in games[session['key']].players:
            player.taken_cards = []
            player.sort_hand()
        return render_template('hotseat/end_of_round.html', game=games[session['key']])
    else:
        return redirect('/hotseat/end_of_game', code=302)

@app.route('/hotseat/end_of_game')
def hotseat_end_of_game():
    if not check():
        return redirect('/', code=302)
    winners = []
    max_points = 0
    for player in games[session['key']].players:
        if player.total_points > max_points:
            max_points = player.total_points
            winners = [player]
        elif player.total_points == max_points:
            winners.append(player)
    return render_template('hotseat/end_of_game.html', game=games[session['key']], winners=winners)


@app.route('/hotseat/next_player')
def hotseat_next_player():
    if not check():
        return redirect('/', code=302)
    games[session['key']].active_player += 1
    games[session['key']].active_player %= 4
    return redirect('/hotseat/table', code=302)


if __name__ == '__main__':
    app.run(host='wierzba.wzks.uj.edu.pl', port=5103, debug=True)
