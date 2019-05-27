from uuid import uuid4

class Game:
    games = {}
    users = {}

    @classmethod
    def create_new_game(cls):
        #template for new game
        data = {
            'user': [
                {
                    'white': True,
                    'user_id': str(uuid4()),
                    'prev': (-1, -1)
                },
                {
                    'white': False,
                    'user_id': str(uuid4()),
                    'prev': (-1, -1)
                }
            ],
            'white_turn': True,
            'game_id': str(uuid4()),
            'board': [
                [-3, -5, -4, -1, -2, -4, -5, -3],
                [-6, -6, -6, -6, -6, -6, -6, -6],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [6, 6, 6, 6, 6, 6, 6, 6],
                [3, 5, 4, 1, 2, 4, 5, 3],
            ],
            'full': False,
            'white_checkmate': None,
            'highlight': Game.clear_highlight() #all zeros
        }

        #generate new id and map it to game data
        game_id = data['game_id']
        cls.games[game_id] = data

        #same with users to game for fast lookup
        cls.users[data['user'][0]['user_id']] = game_id
        cls.users[data['user'][1]['user_id']] = game_id

        return game_id

    @staticmethod
    def filter_user(data, user_id):
        #which user?
        index = 0 if data['user'][0]['user_id'] == user_id else 1

        data['user'] = data['user'][index]
        return data

    @staticmethod
    def flip_board(board):
        board = board[::-1]
        for i, b in enumerate(board):
            board[i] = b[::-1]
        return board

    @staticmethod
    def clear_highlight():
        return [[0 for i in range(8)] for i in range(8)]

    @staticmethod
    def in_bounds(position):
        x = position[0]
        y = position[1]
        if x > 7 or x < 0 or y > 7 or y < 0:
            return False
        return True
