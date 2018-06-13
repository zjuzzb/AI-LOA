class State:
    def __init__(self):
        self.player = 1
        self.board = []
        self.board.append([0, -1, -1, -1, -1, -1, -1, 0])
        for i in range(6):
            self.board.append([1, 0, 0, 0, 0, 0, 0, 1])
        self.board.append([0, -1, -1, -1, -1, -1, -1, 0])

    def get_moves(self):

# get locations of current player's chess, used as a start location of a move.
    def get_start_loc(self):
        result = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == self.player:
                    result.append((i,j))
        return result

# get LEGAL locations of a chess's potential moves, used as a end location of a move.
    def get_end_loc(self, x, y):
        result = []
        next_loc = [
            (1,0),   # right
            (1,1),   # up-right
            (0,1),   # up
            (-1,1),  # up-left
            (-1,0),  # left
            (-1,-1), # down-left
            (0,-1),  # down
            (1,-1),  # down-right
        ]
        for (dx, dy) in next_loc:
            step = 0
            (cx, cy) = (x, y)
            while self.in_bound(cx, cy):
                if self.board[cx][cy] != 0:
                    step += 1
                cx += dx; cy += dy
            (next_x, next_y) = (x + step * dx, y + step * dy)
            if self.in_bound(next_x, next_y) and self.is_legal_loc(next_x, next_y):
                result.append((next_x, next_y))

        return result

    @staticmethod
    def in_bound(x, y):
        if x > 7 | x < 0 | y > 7 | y < 0:
            return False
        else:
            return True

    def is_legal_loc(self, x ,y):
        if self.board[x][y] == self.player:
            return False
        else:
            return True


