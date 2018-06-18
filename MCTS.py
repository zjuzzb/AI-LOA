from node import Node
import random
import time
import threading


def mcts(root_state, iter_max, sec_max):
    root_node = Node(state=root_state)
    args = [sec_max, 1]

    def thread_time(args):
        while True:
            time.sleep(1)
            args[0] -= 1
            if args[0] == 0:
                args[1] = 0
                break

    # add thread for timing
    t_ai = threading.Thread(target=thread_time, args=([args]))
    t_ai.setDaemon(True)
    t_ai.start()

    for i in range(iter_max):  # iter_max should be several times larger than the number of moves
        if args[1] == 0:
            break
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
        move = []
        while state.win_check() == 0 and move_count <= 100:
            move = state.quick_move()
            state.do_move(move)
            move_count += 1

        # Only need one step to win, skip to move
        if move_count == 1:
            return move
        # Back propagate from the expanded node and work back to the root node
        if move_count > 100:
            game_res = (state.evaluate_state(1) - state.evaluate_state(-1))/16
        else:
            game_res = state.win_check() # black -1 white 1 draw 0
        while node:
            node.update((game_res * -node.round + 1) / 2)
            node = node.parent

    selected_node = sorted(root_node.child, key=lambda c: c.visits)[-1]
    print(selected_node.wins)
    print(selected_node.visits)
    print(selected_node.wins / selected_node.visits)
    return selected_node.move  # return the move with highest win rate
