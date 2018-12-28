from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Game

# Create your views here.

def home(request):
    return render(request, "chess.html")

def init(request):
    game = Game.initialize()
    return JsonResponse(game.getJsonState())

@csrf_exempt
def action(request):
    print(json.loads(request.body))
    pass
