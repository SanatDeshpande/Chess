from flask import Flask, render_template, jsonify, request, redirect, url_for
from uuid import uuid4
from Game import Game
import copy

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('chess.html')

@app.route('/init')
def init():
    game_id = Game.create_new_game()

    data = copy.deepcopy(Game.games[game_id])
    data['user'] = data['user'][0]

    return jsonify(data)

@app.route('/game/<user_id>')
def game(user_id):
    return render_template('chess.html')

@app.route('/game_state/<user_id>')
def get_game_state(user_id):

    game_id = Game.users[user_id]
    data = copy.deepcopy(Game.games[game_id])

    #which user?
    index = 0 if data['user'][0]['user_id'] == user_id else 1

    data['user'] = data['user'][index]

    return jsonify(data)

@app.route('/join/<game_id>/')
def join_player(game_id):
    if not Game.games[game_id]['full']:

        data = copy.deepcopy(Game.games[game_id])
        data['user'] = data['user'][1]
        Game.games[game_id]['full'] = True

    return redirect(url_for('game', user_id=data['user']['user_id']))

if __name__ == '__main__':
    app.run()
