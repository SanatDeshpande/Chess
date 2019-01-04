from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Game, Piece

# Create your views here.

@csrf_exempt
def home(request):
    return render(request, "chess.html")

@csrf_exempt
def game(request, user_id):
    return render(request, "chess.html")

@csrf_exempt
def init(request):
    game = Game.initialize()
    game.users[0]['registered'] = True
    response = game.getBoardState()
    response['user'] = game.users[0]
    return JsonResponse(response)

@csrf_exempt
def game_state(request, user_id):
    game = Game.getGameByUserId(user_id)
    return JsonResponse(game.getBoardState(
                        white=game.getUser(user_id)["white"]))


@csrf_exempt
def register_user(request, user_id):
    user_id = json.loads(request.body)['user_id']
    game = Game.getGameByUserId(user_id)
    print(user_id)
    if user_id == '':
        for i in range(2):
            if not game.users[i]['registered']:
                game.users[i]['registered'] = True
                return JsonResponse(game.users[i])
    return HttpResponse(status=400)

@csrf_exempt
def join(request, game_id):
    game = Game.getGameByGameId(game_id)
    if game.users[1]['registered']:
        return HttpResponse("YOU CANNOT HAVE MORE THAN 2 PLAYERS") #error

    game.users[1]['registered'] = True

    return redirect("http://localhost:8000/game/" + game.users[1]['user_id'])

@csrf_exempt
def action(request, user_id):
    game = Game.getGameByUserId(user_id)
    move = json.loads(request.body)['selected']
    user = game.getUser(user_id)
    board = game.board

    if Piece.canSelect(board, move, user_id):
        moves = Piece.dispatch(board, move, user_id)

        #get other user_id
        #simulate one of moves
        #

        if len(moves) > 0:
            for m in moves:
                game.highlight[m[0]][m[1]] = 1

            if not user["white"]:
                game.hightlight = Piece.reverse(game.highlight)

            user["idle"] = False
            game.active = move
    elif Piece.canMove(game.highlight, move, user_id):
        if not user["white"]:
            game.board = Piece.reverse(game.board)

        #moves piece
        game.board[move[0]][move[1]] = game.board[game.active[0]][game.active[1]]
        game.board[game.active[0]][game.active[1]] = 0
        game.white_turn = not game.white_turn

        #resets states
        game.highlight = [[0]*8 for i in range(8)]
        user["idle"] = True

        if not user["white"]:
            game.board = Piece.reverse(game.board)
    elif game.active == move:
        if not user["white"]:
            game.board = Piece.reverse(game.board)
        #resets states
        game.highlight = [[0]*8 for i in range(8)]
        user["idle"] = True
        if not user["white"]:
            game.board = Piece.reverse(game.board)

    return JsonResponse(game.getBoardState(white=user["white"]))
