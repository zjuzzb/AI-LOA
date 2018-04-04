from math import *


class Node:
    def __init__(self, state=None, move=None, parent=None):
        self.player = state.player
        self.untriedMoves = state.getmoves()
        self.move = move
        self.parent = parent
        self.child = []
        self.wins = 0
        self.visits = 0

    def add_child(self, m, s):
        new_node = Node(state=s, move=m, parent=self)
        self.untriedMoves.remove(m)
        self.child.append(new_node)

    def select_child(self):
        self.child.sort(key=lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))
        return self.child[0]

    def update(self, result):
        self.visits += 1
        self.wins += result
