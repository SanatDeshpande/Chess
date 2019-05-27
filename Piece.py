import copy
from Game import Game

class Piece:

    @classmethod
    def get_moves(cls, data, selected):
        piece_moves = {
            6: cls.pawn_moves,
            1: cls.queen_moves,
            2: cls.king_moves,
            3: cls.rook_moves,
            4: cls.bishop_moves,
            5: cls.knight_moves
        }

        data = copy.deepcopy(data) #we are manipulating the board

        board = data['board']
        piece = board[selected[0]][selected[1]]
        x, y = selected

        if piece == 0:
            return []
        if piece > 0 and data['white_turn'] == True or piece < 0 and data['white_turn'] == False:
            if not data['white_turn']:
                board = [[i * -1 for i in b] for b in board] #flip board

            moves = piece_moves[board[x][y]](board, x, y)

            return moves

        return [] #return no moves if conditions are not met

    #this is only a class method so that it can be accessed from the map
    @classmethod
    def pawn_moves(cls, board, x, y):
        moves = []
        if Game.in_bounds((x-1, y)) and board[x-1][y] == 0:
            moves.append((x-1, y))
            if x == 6 and board[x-2][y] == 0:
                moves.append((x-2, y))
        if Game.in_bounds((x-1, y-1)) and board[x-1][y-1] < 0:
            moves.append((x-1, y-1))
        if Game.in_bounds((x-1, y+1)) and board[x-1][y+1] < 0:
            moves.append((x-1, y+1))
        return moves

    @classmethod
    def rook_moves(cls, board, x, y):
        moves = []
        moves += cls.line(board, x, y, (0, 1))
        moves += cls.line(board, x, y, (0, -1))
        moves += cls.line(board, x, y, (1, 0))
        moves += cls.line(board, x, y, (-1, 0))
        return moves

    @classmethod
    def bishop_moves(cls, board, x, y):
        moves = []
        moves += cls.line(board, x, y, (1, 1))
        moves += cls.line(board, x, y, (-1, -1))
        moves += cls.line(board, x, y, (1, -1))
        moves += cls.line(board, x, y, (-1, 1))
        return moves

    @classmethod
    def knight_moves(cls, board, x, y):
        moves = []
        small = [1, -1]
        big = [2, -2]

        for s in small:
            for b in big:
                if Game.in_bounds((x+s, y+b)) and board[x+s][y+b] <= 0:
                    moves.append((x+s, y+b))
                if Game.in_bounds((x+b, y+s)) and board[x+b][y+s] <= 0:
                    moves.append((x+b, y+s))

        return moves

    @classmethod
    def king_moves(cls, board, x, y):
        moves = []
        shift = [-1, 0, 1]
        for i in shift:
            for j in shift:
                if i == 0 and j == 0:
                    continue
                if Game.in_bounds((x+i, y+j)) and board[x+i][y+j] <= 0:
                    moves.append((x+i, y+j))
        return moves

    @classmethod
    def queen_moves(cls, board, x, y):
        return cls.rook_moves(board, x, y) + cls.bishop_moves(board, x, y)

    @staticmethod
    def line(board, x, y, direction):
        moves = []
        x_move, y_move = direction
        x += x_move
        y += y_move

        if not Game.in_bounds((x, y)):
            return moves

        while board[x][y] == 0:
            moves.append((x, y))
            x += x_move
            y += y_move
            if not Game.in_bounds((x, y)):
                return moves

        if board[x][y] < 0:
            moves.append((x, y))
        return moves
