from GUI import *
from MCTS import mcts
import time

def thread_ai():
    while True:
        if m.round == 1:
            ((start_x, start_y), (end_x, end_y)) = mcts(m, 100)
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
app.mainloop()
