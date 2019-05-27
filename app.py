from flask import Flask, render_template, jsonify, request, redirect, url_for
from uuid import uuid4
from Game import Game
from Piece import Piece
import requests
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

    data = Game.filter_user(data, user_id)

    if not data['user']['white']:
        data['board'] = Game.flip_board(data['board'])

    return jsonify(data)

@app.route('/join/<game_id>/')
def join_player(game_id):
    if not Game.games[game_id]['full']:

        data = copy.deepcopy(Game.games[game_id])
        data['user'] = data['user'][1]
        Game.games[game_id]['full'] = True

    return redirect(url_for('game', user_id=data['user']['user_id']))

@app.route('/action/<user_id>/', methods=['POST'])
def get_action(user_id):
    game_id = Game.users[user_id]
    data = copy.deepcopy(Game.games[game_id])
    data = Game.filter_user(data, user_id)

    #don't do anything if it's not your turn
    if data['white_turn'] != data['user']['white']:
        return jsonify(data)

    #if black, flip both boards
    if not data['user']['white']:
        data['board'] = Game.flip_board(data['board'])
        data['highlight'] = Game.flip_board(data['highlight'])

    x, y = request.json['selected'][0], request.json['selected'][1]
    prev_x, prev_y = data['user']['prev']

    print(prev_x, prev_y)
    #if highlighted, move there, else get highlights
    if data['highlight'][x][y] == 1:
        data['board'][x][y] = 0
        data['highlight'] = Game.clear_highlight()
        data['board'][x][y] = data['board'][prev_x][prev_y]
        data['board'][prev_x][prev_y] = 0
        data['white_turn'] = not data['white_turn']
    else:

        moves = Piece.get_moves(data, (x, y))

        data['highlight'] = Game.clear_highlight()
        if len(moves) > 0:
            data['user']['prev'] = (x, y)
        for m in moves:
            data['highlight'][m[0]][m[1]] = 1

        #checks for moves that would result in checkmate
        for m in moves:
            data_copy = copy.deepcopy(data)
            board_copy = data_copy['board']

            board_copy[m[0]][m[1]] = board_copy[x][y]
            board_copy[x][y] = 0
            data_copy['white_turn'] = not data_copy['white_turn']
            counter_moves = []
            for i, b_i in enumerate(board_copy):
                for j, b_j in enumerate(b_i):
                    counter_moves += Piece.get_moves(data_copy, (i, j))

            for c in counter_moves:
                if abs(board_copy[c[0]][c[1]]) == 2:
                    data['highlight'][m[0]][m[1]] = 2


    data_to_send = copy.deepcopy(data)

    #if black, flip both boards for saving
    if not data['user']['white']:
        data['board'] = Game.flip_board(data['board'])
        data['highlight'] = Game.flip_board(data['highlight'])

    #changing permanently
    index = 0 if Game.games[game_id]['user'][0]['user_id'] == user_id else 1

    Game.games[game_id]['user'][index] = data['user']
    for key, value in data.items():
        if key == 'user':
            continue
        Game.games[game_id][key] = data[key]
    Game.games[game_id]['user'][index]['prev'] = data['user']['prev']

    return jsonify(data_to_send)

@app.route('/checkmate/<user_id>/')
def check_checkmate(user_id):
    game_id = Game.users[user_id]
    data = copy.deepcopy(Game.games[game_id])
    data = Game.filter_user(data, user_id)
    board = data['board']

    my_moves = []
    for i, b_i in enumerate(board):
        for j, b_j in enumerate(b_i):
            my_moves += Piece.get_moves(data, (i, j))

    for m in my_moves:
        if abs(board[m[0]][m[1]]) == 2:
            data['white_checkmate'] = data['white_turn']
            return jsonify(data)

    return jsonify(data)


if __name__ == '__main__':
    app.run()
