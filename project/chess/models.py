from django.db import models
import uuid

# Create your models here.
class Game:
    games = {}
    def __init__(self):
        self.board = [
            [-3, -5, -4, -1, -2, -4, -5, -3],
            [-6, -6, -6, -6, -6, -6, -6, -6],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [6, 6, 6, 6, 6, 6, 6, 6],
            [3, 5, 4, 1, 2, 4, 5, 3],
        ]
        self.highlight = [[0]*8 for i in range(8)]
        self.white_turn = True
        self.idle = True
        self.id = str(uuid.uuid4())

    @classmethod
    def initialize(cls):
        g = cls()
        cls.games[g.id] = {
            "board": g.board,
            "white_turn": g.white_turn,
            "idle": g.idle,
            "highlight": g.highlight,
        }
        return g

    def getJsonState(self):
        return {
            "board": self.board,
            "white_turn": self.white_turn,
            "idle": self.idle,
            "id": self.id,
            "highlight": self.highlight,
        }
