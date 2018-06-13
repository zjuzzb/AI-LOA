class State:
    def __init__(self):
        self.player = 1
        self.board = []
        self.board.append([0, -1, -1, -1, -1, -1, -1, 0])
        for i in range(6):
            self.board.append([1, 0, 0, 0, 0, 0, 0, 1])
        self.board.append([0, -1, -1, -1, -1, -1, -1, 0])

    def get_moves(self):

# get location of current player's chess, used as a start location of a move.
    def get_prev_loc(self):
        result = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == self.player:
                    result.append((i,j))
        return result

# get location of a chess's potential moves, used as a end location of a move.
    def get_next_loc(self, x, y):
        result = []
        # move to right --direction = 1
        # move to top-right --direction = 2
        # move to top --direction = 3
        # move to top-left --direction = 4
        # move to left --direction = 5
        # move to down-left --direction = 6
        # move to down --direction = 7
        # move to down-right --direction = 8

# according to the input direction to calculate the chess number, which used as step length.
    def count_chess_number(self, x, y, direction):
        count = 0; cx = x; cy = y

        next_loc = {
            'right': (1,0),
            'top-right': (1,1),
            'top': (0,1),
            'top-left': (-1,1),
            'left': (-1,0),
            'down-left': (-1,-1),
            'down': (0,-1),
            'down-right': (1,-1),
        }
        while not self.out_of_bound(self, cx, cy):
            if self.board[cx][cy] != 0:
                count += 1
            (dx,dy) = next_loc[direction]
            cx += dx; cy += dy
        return count

    @staticmethod
    def out_of_bound(self, x, y):
        if x > 7 | x < 0 | y > 7 | y < 0:
            return True
        else:
            return False



