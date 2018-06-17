import random


class State:
    def __init__(self):
        self.round = -1
        self.board = []
        self.board.append([0, -1, -1, -1, -1, -1, -1, 0])
        for i in range(6):
            self.board.append([1, 0, 0, 0, 0, 0, 0, 1])
        self.board.append([0, -1, -1, -1, -1, -1, -1, 0])
        self.next_loc = [
            (1, 0),     # right
            (1, 1),     # up-right
            (0, 1),     # up
            (-1, 1),    # up-left
            (-1, 0),    # left
            (-1, -1),   # down-left
            (0, -1),    # down
            (1, -1),    # down-right
        ]

# Create a deep clone of this game state.
    def clone(self):
        st = State()
        st.round = self.round
        st.board = [self.board[i][:] for i in range(8)]
        return st

    def get_moves(self):
        # res = ((start_x, start_y), (end_x, end_y))
        res = []
        start_loc = self.get_start_loc()
        for (start_x, start_y) in start_loc:
            end_loc = self.get_end_loc(start_x, start_y)
            for (end_x, end_y) in end_loc:
                res.append(((start_x, start_y), (end_x, end_y)))
        return res

    def do_move(self, move):
        ((start_x, start_y), (end_x, end_y)) = move
        self.board[end_x][end_y] = self.board[start_x][start_y]
        self.board[start_x][start_y] = 0
        # if self.legal_move_check() == 1:
        #     self.round = -self.round
        pass

# get locations of current player's chess, used as a start location of a move.
    def get_start_loc(self):
        result = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == self.round:
                    result.append((i,j))
        return result

# get LEGAL locations of a chess's potential moves, used as a end location of a move.
    def get_end_loc(self, x, y):
        result = []

        for (dx, dy) in self.next_loc:
            step = -1
            (cx, cy) = (x, y)
            while self.in_bound(cx, cy):
                if self.board[cx][cy] != 0:
                    step += 1
                cx += dx; cy += dy
            (cx, cy) = (x, y)
            while self.in_bound(cx, cy):
                if self.board[cx][cy] != 0:
                    step += 1
                cx -= dx; cy -= dy
            (next_x, next_y) = (x + step * dx, y + step * dy)
            if self.in_bound(next_x, next_y):
                flag = True
                for i in range(step):
                    if self.board[x + i * dx][ y + i * dy] == -self.board[x][y]:
                        flag = False
                        break
                if self.board[next_x][next_y] != self.board[x][y] and flag:
                    result.append((next_x, next_y))

        return result

# check the win condition, return 1 for white win, -1 for black win, 0 for game continue
    def win_check(self):
        def recursion_flag(color, x, y):
            check_board[x][y] = color
            for (dx, dy) in self.next_loc:
                if self.in_bound(x + dx, y + dy):
                    if self.board[x + dx][y + dy] == color and check_board[x+dx][y+dy] == 0:
                        recursion_flag(color, x+dx, y+dy)

        check_board = [[0 for _ in range(8)] for _ in range(8)]
        black_win = True
        white_win = True
        black_flag = True
        white_flag = True
        black_count = 0
        white_count = 0

        for i in range(8):
            if not white_flag and not black_flag:
                break
            for j in range(8):
                if not white_flag and not black_flag:
                    break
                if self.board[i][j] == 1 and white_flag:
                    recursion_flag(1, i, j)
                    white_flag = False
                elif self.board[i][j] == -1 and black_flag:
                    recursion_flag(-1, i, j)
                    black_flag = False

        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 1:
                    white_count += 1
                    if check_board[i][j] != 1:
                        white_win = False
                if self.board[i][j] == -1:
                    black_count += 1
                    if check_board[i][j] != -1:
                        black_win = False

        if white_count <= 1:
            return -1
        elif black_count <= 1:
            return 1

        if black_win and white_win:
            return self.round
        elif black_win and not white_win:
            return -1
        elif not black_win and white_win:
            return 1
        else:
            return 0

    @staticmethod
    def in_bound(x, y):
        if x > 7 or x < 0 or y > 7 or y < 0:
            return False
        else:
            return True

# return 1 for there are legal moves for next player
# -1 for there is no legal move for next player, but there are legal moves for current player
# 0 for there is no legal move for both two players, end the game
    def legal_move_check(self):
        # check whether there is legal moves or not
        moves = []
        for i in range(8):
            for j in range(8):
                # all next player's chess
                if self.board[i][j] == -self.round:
                    moves.append(self.get_end_loc(i, j))
        if not moves:
            # check whether there is legal moves or not for current player
            moves = []
            for i in range(8):
                for j in range(8):
                    # all current player's chess
                    if self.board[i][j] == self.round:
                        moves.append(self.get_end_loc(i, j))
            if not moves:
                return 0
            else:
                return -1
        else:
            self.round = -self.round
            return 1

    # def get_result(self):
    #     if self.legal_move_check() == 0:
    #         return 0
    #     return self.win_check()

    def quick_move(self):
        (start_x, start_y) = random.choice(self.get_start_loc())
        end_loc = self.get_end_loc(start_x,start_y)
        while not end_loc:
            (start_x, start_y) = random.choice(self.get_start_loc())
            end_loc = self.get_end_loc(start_x, start_y)
        (end_x, end_y) = random.choice(end_loc)

        return (start_x, start_y), (end_x, end_y)


