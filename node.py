from math import *


class Node:
    def __init__(self, state=None, move=None, parent=None):
        self.round = state.round
        self.untriedMoves = state.get_moves()
        self.move = move  # the move that got us to this node - "None" for the root node
        self.parent = parent
        self.child = []
        self.wins = 0
        self.visits = 0
        self.score = (state.evaluate_state(-self.round) - state.evaluate_state(self.round))/16

    def add_child(self, m, s):
        new_node = Node(state=s, move=m, parent=self)
        self.untriedMoves.remove(m)
        self.child.append(new_node)
        return new_node

    def select_child(self):
        self.child.sort(key=lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits) + c.score)
        return self.child[-1]

    def update(self, result):
        self.visits += 1
        self.wins += result

