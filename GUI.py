from tkinter import *
from tkinter import messagebox
import threading
import time
from state import State


class LOAModel(State):
    def __init__(self):
        super(LOAModel, self).__init__()
        self.round = -1
        # timing
        self.time_ai = 0
        self.time_p = 0
        # 0 for select a chess, 1 for jump to another location
        self.stage = 0
        # stored the location of selected chess
        self.chess_selected = (0, 0)
        self.legal_move = []


class Application(Frame):
    def __init__(self, model, master=None):
        # load model
        self.model = model
        # add root frame
        Frame.__init__(self, master, height=500, width=500)
        self.pack()
        # load icons
        self.empty_icon = PhotoImage(file='empty.png')
        self.black_icon = PhotoImage(file='black_chess.png')
        self.white_icon = PhotoImage(file='white_chess.png')
        self.black_selected_icon = PhotoImage(file='black_chess_selected.png')
        self.white_selected_icon = PhotoImage(file='white_chess_selected.png')
        self.black_highlighted_icon = PhotoImage(file='black_chess_highlighted.png')
        self.white_highlighted_icon = PhotoImage(file='white_chess_highlighted.png')
        self.empty_highlighted_icon = PhotoImage(file='empty_highlighted.png')
        # initialize components
        self.chessButton = []
        self.time_text_p = StringVar(self, 'Black Time: 00:00')
        self.time_text_ai = StringVar(self, 'White Time: 00:00')
        self.round_text = StringVar(self, 'Current Player: Black')
        # load components
        self.create_widgets()
        # add thread for AI timing
        self.t_ai = threading.Thread(target=self.update_time_text_ai, args=(), name='thread-refresh')
        self.t_ai.setDaemon(True)
        self.t_ai.start()
        # add thread for player timing
        self.t_p = threading.Thread(target=self.update_time_text_p, args=(), name='thread-refresh')
        self.t_p.setDaemon(True)
        self.t_p.start()

    def on_click(self, x, y):
        if self.model.stage == 0:
            if self.model.board[x][y] == self.model.round:
                if self.model.round == -1:
                    icon = self.black_selected_icon
                else:
                    icon = self.white_selected_icon
                self.chessButton[x][y] = Button(self, height=80, width=80, bg='#EBCEAC', image=icon,
                                                command=(lambda x, y: lambda: self.on_click(x, y))(x, y))
                self.chessButton[x][y].grid(row=x + 1, column=y)
                self.model.stage = 1
                self.model.chess_selected = (x, y)
                self.model.legal_move = self.model.get_end_loc(x, y)
                # highlight legal locations
                for (hx,hy) in self.model.legal_move:
                    if self.model.board[hx][hy] == 1:
                        icon_h = self.white_highlighted_icon
                    elif self.model.board[hx][hy] == -1:
                        icon_h = self.black_highlighted_icon
                    else:
                        icon_h = self.empty_highlighted_icon
                    self.chessButton[hx][hy] = Button(self, height=80, width=80, bg='#EBCEAC', image=icon_h,
                                                    command=(lambda x, y: lambda: self.on_click(x, y))(hx, hy))
                    self.chessButton[hx][hy].grid(row=hx + 1, column=hy)
        else:
            if self.model.round == -1:
                icon = self.black_icon
            else:
                icon = self.white_icon
            if (x, y) in self.model.legal_move:
                # move the chess to a new location
                (prevx, prevy) = self.model.chess_selected
                self.chessButton[prevx][prevy] = Button(self, height=80, width=80, bg='#EBCEAC', image=self.empty_icon,
                                                        command=(lambda x, y: lambda: self.on_click(x, y))(prevx, prevy))
                self.chessButton[prevx][prevy].grid(row=prevx + 1, column=prevy)
                self.chessButton[x][y] = Button(self, height=80, width=80, bg='#EBCEAC', image=icon,
                                                        command=(lambda x, y: lambda: self.on_click(x, y))(x, y))
                self.chessButton[x][y].grid(row=x + 1, column=y)
                self.model.board[x][y] = self.model.round
                self.model.board[prevx][prevy] = 0
                self.model.stage = 0
                # de-highlight legal locations
                for (hx,hy) in self.model.legal_move:
                    if self.model.board[hx][hy] == 1:
                        icon_h = self.white_icon
                    elif self.model.board[hx][hy] == -1:
                        icon_h = self.black_icon
                    else:
                        icon_h = self.empty_icon
                    self.chessButton[hx][hy] = Button(self, height=80, width=80, bg='#EBCEAC', image=icon_h,
                                                    command=(lambda x, y: lambda: self.on_click(x, y))(hx, hy))
                    self.chessButton[hx][hy].grid(row=hx + 1, column=hy)
                # check whether there is legal moves or not
                moves = []
                for i in range(8):
                    for j in range(8):
                        # all next player's chess
                        if self.model.board[i][j] == -self.model.round:
                            moves.append(self.model.get_end_loc(i, j))
                if not moves:
                    if self.model.round == 1:
                        player = 'White'
                    else:
                        player = 'Black'
                    msg = messagebox.showwarning('Warning', player + ' has no legal move!')
                    print(msg)
                else:
                    self.model.round = -self.model.round
                    if self.model.round == 1:
                        self.round_text.set('Current Player: White')
                    else:
                        self.round_text.set('Current Player: Black')
            elif (x, y) == self.model.chess_selected:
                # cancel the selection
                self.chessButton[x][y] = Button(self, height=80, width=80, bg='#EBCEAC', image=icon,
                                                        command=(lambda x, y: lambda: self.on_click(x, y))(x, y))
                self.chessButton[x][y].grid(row=x + 1, column=y)
                self.model.stage = 0
                # de-highlight legal locations
                for (hx,hy) in self.model.legal_move:
                    if self.model.board[hx][hy] == 1:
                        icon_h = self.white_icon
                    elif self.model.board[hx][hy] == -1:
                        icon_h = self.black_icon
                    else:
                        icon_h = self.empty_icon
                    self.chessButton[hx][hy] = Button(self, height=80, width=80, bg='#EBCEAC', image=icon_h,
                                                    command=(lambda x, y: lambda: self.on_click(x, y))(hx, hy))
                    self.chessButton[hx][hy].grid(row=hx + 1, column=hy)
            else:
                msg = messagebox.showwarning('Warning', 'Illegal move!')
                print(msg)

    def create_widgets(self):
        self.time_label_ai = Label(self, textvariable=self.time_text_ai)
        self.time_label_ai.grid(row=0, column=0, columnspan=2)
        self.time_label_p = Label(self, textvariable=self.time_text_p)
        self.time_label_p.grid(row=0, column=6, columnspan=2)
        self.round_label = Label(self, textvariable=self.round_text)
        self.round_label.grid(row=0, column=3, columnspan=2)
        for i in range(8):
            row = []
            if i == 0 or i == 7:
                row.append(Button(self, height=80, width=80, bg='#EBCEAC', image=self.empty_icon,
                                  command=(lambda x, y: lambda: self.on_click(x, y))(i, 0)))
                for j in range(6):
                    row.append(Button(self, height=80, width=80, bg='#EBCEAC', image=self.black_icon,
                                      command=(lambda x, y: lambda: self.on_click(x, y))(i, j + 1)))
                row.append(Button(self, height=80, width=80, bg='#EBCEAC', image=self.empty_icon,
                                  command=(lambda x, y: lambda: self.on_click(x, y))(i, 7)))
            else:
                row.append(Button(self, height=80, width=80, bg='#EBCEAC', image=self.white_icon,
                                  command=(lambda x, y: lambda: self.on_click(x, y))(i, 0)))
                for j in range(6):
                    row.append(Button(self, height=80, width=80, bg='#EBCEAC', image=self.empty_icon,
                                      command=(lambda x, y: lambda: self.on_click(x, y))(i, j + 1)))
                row.append(Button(self, height=80, width=80, bg='#EBCEAC', image=self.white_icon,
                                  command=(lambda x, y: lambda: self.on_click(x, y))(i, 7)))
            self.chessButton.append(row)
        for i in range(8):
            for j in range(8):
                self.chessButton[i][j].grid(row=i + 1, column=j)

    def update_time_text_ai(self):
        while True:
            if self.model.round == 1:
                minutes = int(self.model.time_ai / 60)
                seconds = int(self.model.time_ai - minutes * 60.0)
                self.time_text_ai.set('White Time: %.2d:%.2d' % (minutes, seconds))
                self.model.time_ai += 1
                time.sleep(1)

    def update_time_text_p(self):
        while True:
            if self.model.round == -1:
                minutes = int(self.model.time_p / 60)
                seconds = int(self.model.time_p - minutes * 60.0)
                self.time_text_p.set('Black Time: %.2d:%.2d' % (minutes, seconds))
                self.model.time_p += 1
                time.sleep(1)


m = LOAModel()
app = Application(m)
# 设置窗口标题:
app.master.title('LOA')
# 主消息循环:
app.mainloop()
