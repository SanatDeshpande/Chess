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
        self.active = None
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
    def canSelect(cls, board, move, user_id):
        game = Game.getGameByUserId(user_id)
        user = game.getUser(user_id)

        if not user["white"]:
            move = [7-m for m in move]

        if game.white_turn == user["white"] and user["idle"]:
            if board[move[0]][move[1]] == 0:
                return False
            selected = True if board[move[0]][move[1]] > 0 else False
            if user["white"] == selected:
                return True
        return False

    @classmethod
    def canMove(cls, board, move, user_id):
        game = Game.getGameByUserId(user_id)
        user = game.getUser(user_id)

        if game.white_turn == user["white"] and not user["idle"]:
            if board[move[0]][move[1]] == 1:
                return True

        return False

    @classmethod
    def dispatch(cls, board, move, user_id):
        game = Game.getGameByUserId(user_id)
        user = game.getUser(user_id)

        if not user["white"]:
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
    def otherTeamMoves(cls, board, user_id):
        #get other user_id
        game = Game.getGameByUserId(user_id)
        user = game.getUser(user_id)
        other_user_id = game.users[0]["user_id"]
        if game.users[0]["user_id"] == user_id:
            other_user_id = game.users[1]["user_id"]
        other_user = game.getUser(other_user_id)

        if not other_user["white"]:
            board = Piece.reverse(board)

        moves = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] < 0 and not other_user["white"] or board[i][j] > 0 and other_user["white"]:
                    moves += cls.dispatch(board, [i,j], other_user_id)
        return moves


    @classmethod
    def pawn(cls, board, move):
        print("pawn")
        moves = []
        if move[0] == 6:
            if board[move[0] - 1][move[1]] == 0:
                moves.append([move[0] - 1, move[1]])
                if board[move[0] - 2][move[1]] == 0:
                    moves.append([move[0] - 2, move[1]])

        if Piece.inBounds(board, move, x=-1, y=-1) and Piece.isOtherColor(board, move, x=-1, y=-1):
            moves.append([move[0] - 1, move[1] - 1])
        if Piece.inBounds(board, move, x=-1, y=1) and Piece.isOtherColor(board, move, x=-1, y=1):
            moves.append([move[0] - 1, move[1] + 1])
        if Piece.inBounds(board, move, x=-1, y=0) and Piece.isOtherColor(board, move, x=-1, y=0) is None:
            moves.append([move[0]-1, move[1]])
        return moves

    @classmethod
    def rook(cls, board, move):
        print("rook")
        moves = []
        for i in range(1, 8):
            if Piece.inBounds(board, move, x=i, y=0):
                other = Piece.isOtherColor(board, move, x=i, y=0)
                if other or other is None:
                    moves.append([move[0]+i, move[1]])
                if other is not None:
                    break
        for i in range(-1, -8, -1):
            if Piece.inBounds(board, move, x=i, y=0):
                other = Piece.isOtherColor(board, move, x=i, y=0)
                if other or other is None:
                    moves.append([move[0]+i, move[1]])
                if other is not None:
                    break
        for i in range(1, 8):
            if Piece.inBounds(board, move, x=0, y=i):
                other = Piece.isOtherColor(board, move, x=0, y=i)
                if other or other is None:
                    moves.append([move[0], move[1]+i])
                if other is not None:
                    break
        for i in range(-1, -8, -1):
            if Piece.inBounds(board, move, x=0, y=i):
                other = Piece.isOtherColor(board, move, x=0, y=i)
                if other or other is None:
                    moves.append([move[0], move[1]+i])
                if other is not None:
                    break
        return moves

    @classmethod
    def bishop(cls, board, move):
        print("bishop")
        moves = []
        for i in range(1, 8):
            if Piece.inBounds(board, move, x=i, y=i):
                other = Piece.isOtherColor(board, move, x=i, y=i)
                if other or other is None:
                    moves.append([move[0]+i, move[1]+i])
                if other is not None:
                    break
        for i in range(1, 8):
            if Piece.inBounds(board, move, x=-1*i, y=-1*i):
                other = Piece.isOtherColor(board, move, x=-1*i, y=-1*i)
                if other or other is None:
                    moves.append([move[0]-i, move[1]-i])
                if other is not None:
                    break
        for i in range(1, 8):
            if Piece.inBounds(board, move, x=-1*i, y=i):
                other = Piece.isOtherColor(board, move, x=-1*i, y=i)
                if other or other is None:
                    moves.append([move[0]-i, move[1]+i])
                if other is not None:
                    break
        for i in range(1, 8):
            if Piece.inBounds(board, move, x=i, y=-1*i):
                other = Piece.isOtherColor(board, move, x=i, y=-1*i)
                if other or other is None:
                    moves.append([move[0]+i, move[1]-i])
                if other is not None:
                    break
        return moves

    @classmethod
    def knight(cls, board, move):
        print("knight")
        change = [-2, 2, -1, 1]
        moves = []
        for i in change:
            for j in change:
                if abs(i) != abs(j):
                    if Piece.inBounds(board, move, x=i, y=j):
                        other = Piece.isOtherColor(board, move, x=i, y=j)
                        if other or other is None:
                            moves.append([move[0]+i, move[1]+j])
        return moves

    @classmethod
    def king(cls, board, move):
        print("king")
        change = [-1, 0, 1]
        moves = []
        for i in change:
            for j in change:
                if not (i == 0 and j == 0):
                    if Piece.inBounds(board, move, x=i, y=j):
                        other = Piece.isOtherColor(board, move, x=i, y=j)
                        if other or other is None:
                            moves.append([move[0]+i, move[1]+j])
        return moves

    @classmethod
    def queen(cls, board, move):
        print("queen")
        moves = []
        moves += cls.bishop(board, move)
        moves += cls.rook(board, move)
        return moves

    @classmethod
    def reverse(cls, board):
        response_board = [[0]*8 for i in range(8)]
        for i in range(len(board)):
            for j in range(len(board[0])):
                response_board[i][j] = board[7-i][7-j]
        return response_board

    @classmethod
    def inBounds(cls, board, move, x=0, y=0):
        new_pos = [move[0]+x, move[1]+y]
        if new_pos[0] < 0 or new_pos[0] > 7 or new_pos[1] < 0 or new_pos[1] > 7:
            return False
        return True

    @classmethod
    def isOtherColor(cls, board, move, x=0, y=0):
        new_pos = [move[0]+x, move[1]+y]
        if board[new_pos[0]][new_pos[1]] * board[move[0]][move[1]] == 0:
            return None
        return board[new_pos[0]][new_pos[1]] * board[move[0]][move[1]] < 0
