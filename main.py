from GUI import *
from MCTS import mcts
import time
import random

def thread_ai():
    while True:
        if m.round == -1:
            ((start_x, start_y), (end_x, end_y)) = mcts(m, 400)
            app.chessButton[start_x][start_y].invoke()
            time.sleep(1)
            app.chessButton[end_x][end_y].invoke()

def thread_rnd():
    while True:
        if m.round == 1:
            ((start_x, start_y), (end_x, end_y)) = m.quick_move()
            app.chessButton[start_x][start_y].invoke()
            time.sleep(1)
            app.chessButton[end_x][end_y].invoke()


m = LOAModel()
app = Application(m)
app.master.title('LOA')
# add thread for AI
t_ai = threading.Thread(target=thread_ai, args=())
t_ai.setDaemon(True)
t_ai.start()
# add thread for random moves
t_rnd = threading.Thread(target=thread_rnd, args=())
t_rnd.setDaemon(True)
t_rnd.start()
app.mainloop()
