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

    def getUserColor(self, user_id):
        if self.users[0]['user_id'] == user_id:
            return self.users[0]['white']
        elif self.users[1]['user_id'] == user_id:
            return self.users[1]['white']
        else:
            return None

    def getBoardState(self, white=True):
        response_board = [[0]*8 for i in range(8)]
        if not white:
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    response_board[i][j] = self.board[7-i][7-j]
        else:
            response_board = self.board

        return {
            "board": response_board,
            "game_id": self.game_id,
            "highlight": self.highlight,
        }

class Piece:
    @classmethod
    def validate(cls, board, move, user_id):
        pass

    @classmethod
    def dispatch(cls, board, move):
        pass

    @classmethod
    def pawn(cls):
        pass

    @classmethod
    def rook(cls):
        pass

    @classmethod
    def bishop(cls):
        pass

    @classmethod
    def knight(cls):
        pass

    @classmethod
    def king(cls):
        pass

    @classmethod
    def queen(cls):
        pass
