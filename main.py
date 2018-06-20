from GUI import *
from MCTS import mcts
import time


def thread_black():
    while True:
        if m.round == -1:
            ((start_x, start_y), (end_x, end_y)) = m.quick_move()
            app.chessButton[start_x][start_y].invoke()
            time.sleep(1)
            app.chessButton[end_x][end_y].invoke()


def thread_white():
    while True:
        if m.round == 1:
            ((start_x, start_y), (end_x, end_y)) = mcts(m, 2000, 50, 35)
            app.chessButton[start_x][start_y].invoke()
            time.sleep(1)
            app.chessButton[end_x][end_y].invoke()


m = LOAModel()
app = Application(m)
app.master.title('LOA')
# add thread for black
# t_black = threading.Thread(target=thread_black, args=())
# t_black.setDaemon(True)
# t_black.start()
# add thread for white
t_white = threading.Thread(target=thread_white, args=())
t_white.setDaemon(True)
t_white.start()
app.mainloop()
