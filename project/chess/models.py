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
        self.game_id = str(uuid.uuid4())
        self.users = [{"user_id": str(uuid.uuid4()), "white": True, "registered": False, "idle": True},
                      {"user_id": str(uuid.uuid4()), "white": False, "registered": False, "idle": True}]

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

    def getUser(self, user_id):
        if self.users[0]['user_id'] == user_id:
            return self.users[0]
        elif self.users[1]['user_id'] == user_id:
            return self.users[1]
        else:
            return None

    def getBoardState(self, white=True):
        #ONLY FOR DISPLAY PURPOSES
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
    def isValid(cls, board, move, user_id):
        game = Game.getGameByUserId(user_id)
        user = game.getUser(user_id)

        if not user["white"]:
            board = Piece.reverse()

        if game.white_turn == user["white"] and user["idle"] and board[move[0]][move[1]] > 0:
            return True

        return False

    @classmethod
    def dispatch(cls, board, move):
        if board[move[0]][move[1]] < 0:
            board = Piece.reverse(board)

        pieces = {
            6: Piece.pawn,
            3: Piece.rook,
            4: Piece.bishop,
            5: Piece.knight,
            1: Piece.queen,
            2: Piece.king
        }
        tile = abs(board[move[0]][move[1]])
        return pieces[tile](board, move)

    @classmethod
    def pawn(cls, board, move):
        print("pawn")
        moves = []
        if move[0] == 6:
            if board[move[0] - 1][move[1]] == 0:
                moves.append([move[0] - 1, move[1]])
                if board[move[0] - 2][move[1]] == 0:
                    moves.append([move[0] - 2, move[1]])
        else:
            if Piece.diffSign(board[move[0] - 1][move[1] - 1], board[move[0]][move[1]]):
                moves.append([move[0] - 1, move[1] - 1])
            if Piece.diffSign(board[move[0] - 1][move[1] + 1], board[move[0]][move[1]]):
                moves.append([move[0] - 1, move[1] + 1])
        return moves

    @classmethod
    def rook(cls, board, movels):
        print("rook")
        pass

    @classmethod
    def bishop(cls, board, move):
        print("bishop")
        pass

    @classmethod
    def knight(cls, board, move):
        print("knight")
        pass

    @classmethod
    def king(cls, board, move):
        print("king")
        pass

    @classmethod
    def queen(cls, board, move):
        print("queen")
        pass

    @classmethod
    def reverse(cls, board):
        response_board = [[0]*8 for i in range(8)]
        for i in range(len(board)):
            for j in range(len(board[0])):
                response_board[i][j] = board[7-i][7-j]
        return response_board

    @classmethod
    def diffSign(cls, x, y):
        if x < 0 and y < 0 or x > 0 and y > 0:
            return False
        return True
