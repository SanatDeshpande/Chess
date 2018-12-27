from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.

def home(request):
    return render(request, "chess.html")

def test(request):
    response = {"response_data": "it worked"}
    return JsonResponse(response)
