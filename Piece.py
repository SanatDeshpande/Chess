class Piece:
    @classmethod
    def get_moves(cls, data, selected):
        board = data['board']
        piece = board[selected[0]][selected[1]]
        selected = tuple(selected)

        if piece == 0:
            return []
        if piece > 0 and data['white_turn'] == True or piece < -1 and data['white_turn'] == False:
            return [selected]
        else:
            return []
