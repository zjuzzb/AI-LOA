from node import Node
import random


def mcts(root_state, iter_max):
    root_node = Node(state=root_state)

    for i in range(iter_max):  # iter_max should be several times larger than the number of moves
        node = root_node
        state = root_state.clone()

        # Select the best evaluated node
        while node.untriedMoves == [] and node.child != []:  # node is fully expanded and non-terminal
            node = node.select_child()
            state.do_move(node.move)

        # Expand a child node from a random chosen move
        if node.untriedMoves:
            move = random.choice(node.untriedMoves)
            state.do_move(move)
            node = node.add_child(move, state)  # add child and descend tree and remove the move

        # Roll out to the game end
        move_count = 0
        while state.win_check() == 0 and move_count <= 200:
            state.do_move(state.quick_move())
            move_count += 1

        # Back propagate from the expanded node and work back to the root node
        game_res = state.win_check() # black -1 white 1 draw 0
        while node:
            node.update((game_res * -node.round + 1) / 2)
            node = node.parent

    selected_node = sorted(root_node.child, key=lambda c: c.wins/c.visits)[-1]
    print(selected_node.wins)
    print(selected_node.visits)
    print(selected_node.wins / selected_node.visits)
    return selected_node.move  # return the move with highest win rate
