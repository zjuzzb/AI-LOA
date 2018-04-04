class State:
    def __init__(self):
        self.player = 1
        self.board = []
        self.board.append([0, -1, -1, -1, -1, -1, -1, 0])
        for i in range(6):
            self.board.append([1, 0, 0, 0, 0, 0, 0, 1])
        self.board.append([0, -1, -1, -1, -1, -1, -1, 0])

    def getmoves(self):


