from django.db import models
import uuid

# Create your models here.
class Game:
    games = {}
    user_to_game = {}
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
        self.game_id = str(uuid.uuid4())
        self.users = [{"user_id": str(uuid.uuid4()), "white": True, "registered": False},
                      {"user_id": str(uuid.uuid4()), "white": False, "registered": False}]
        print(self.users[0]['user_id'], self.users[1]['user_id'], self.game_id)
    @classmethod
    def initialize(cls):
        g = cls()

        cls.user_to_game[g.users[0]['user_id']] = g.game_id
        cls.user_to_game[g.users[1]['user_id']] = g.game_id

        cls.games[g.game_id] = g
        return g

    @classmethod
    def getGameByUserId(cls, user_id):
        return cls.games[cls.user_to_game[user_id]]

    @classmethod
    def getGameByGameId(cls, game_id):
        return cls.games[game_id]

    def getBoardState(self):
        return {
            "board": self.board,
            "game_id": self.game_id,
            "highlight": self.highlight,
        }
