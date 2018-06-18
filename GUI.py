from tkinter import *
from tkinter import messagebox
import threading
import time
from state import State


class LOAModel(State):
    def __init__(self):
        super(LOAModel, self).__init__()
        # timing
        self.time_white = 0
        self.time_black = 0
        self.step_time = 0
        # stored the location of selected chess
        self.chess_selected = ()
        # for coloring
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
        self.time_text_black = StringVar(self, 'Black Total: 00:00   Step: 00')
        self.time_text_white = StringVar(self, 'White Total: 00:00   Step: 00')
        self.round_text = StringVar(self, 'Current Player: Black')
        # load components
        self.create_widgets()
        # add thread for white timing
        self.t_white = threading.Thread(target=self.update_time_text_white, args=(), name='thread-refresh')
        self.t_white.setDaemon(True)
        self.t_white.start()
        # add thread for black timing
        self.t_black = threading.Thread(target=self.update_time_text_black, args=(), name='thread-refresh')
        self.t_black.setDaemon(True)
        self.t_black.start()

    def on_click(self, x, y):
        if self.model.board[x][y] == self.model.round:
            if self.model.round == -1:
                icon_s = self.black_selected_icon
                icon = self.black_icon
            else:
                icon_s = self.white_selected_icon
                icon = self.white_icon
            if self.model.chess_selected == ():
                self.chessButton[x][y].config(image=icon_s)
                self.model.chess_selected = (x, y)
                self.model.legal_move = self.model.get_end_loc(x, y)
                self.highlight_button(False)
            else:
                (prev_x, prev_y) = self.model.chess_selected
                self.chessButton[prev_x][prev_y].config(image=icon)
                self.model.legal_move = self.model.get_end_loc(prev_x, prev_y)
                self.highlight_button(True)
                self.chessButton[x][y].config(image=icon_s)
                self.model.chess_selected = (x, y)
                self.model.legal_move = self.model.get_end_loc(x, y)
                self.highlight_button(False)
        elif self.model.chess_selected != ():
            if self.model.round == -1:
                icon = self.black_icon
            else:
                icon = self.white_icon
            if (x, y) in self.model.legal_move:
                # move the chess to a new location
                (prev_x, prev_y) = self.model.chess_selected
                self.chessButton[prev_x][prev_y].config(image=self.empty_icon)
                self.chessButton[x][y].config(image=icon)
                self.model.board[x][y] = self.model.round
                self.model.board[prev_x][prev_y] = 0
                self.highlight_button(True)
                # clear step timing
                self.model.step_time = 0
                # clear selected chess
                self.model.chess_selected = ()
                self.game_end_check()
            else:
                msg = messagebox.showwarning('Warning', 'Illegal move!')
                print(msg)

    def create_widgets(self):
        self.time_label_white = Label(self, textvariable=self.time_text_white)
        self.time_label_white.grid(row=0, column=0, columnspan=3)
        self.time_label_black = Label(self, textvariable=self.time_text_black)
        self.time_label_black.grid(row=0, column=5, columnspan=3)
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

    def update_time_text_white(self):
        while True:
            if self.model.round == 1:
                minutes = int(self.model.time_white / 60)
                seconds = int(self.model.time_white - minutes * 60.0)
                self.time_text_white.set('White Total: %.2d:%.2d   Step: %.2d' % (minutes, seconds, self.model.step_time))
                self.model.time_white += 1
                self.model.step_time += 1
                time.sleep(1)
                if self.model.step_time >= 60:
                    msg = messagebox.showwarning('Oops', 'White timeout. Black wins!')
                    print(msg)
                    self.initialize()

    def update_time_text_black(self):
        while True:
            if self.model.round == -1:
                minutes = int(self.model.time_black / 60)
                seconds = int(self.model.time_black - minutes * 60.0)
                self.time_text_black.set('Black Total: %.2d:%.2d   Step: %.2d' % (minutes, seconds, self.model.step_time))
                self.model.time_black += 1
                self.model.step_time += 1
                time.sleep(1)
                if self.model.step_time >= 60:
                    msg = messagebox.showwarning('Oops', 'Black timeout. White wins!')
                    print(msg)
                    self.initialize()

    def highlight_button(self, clear):
        # highlight or de-highlight legal locations
        for (hx, hy) in self.model.legal_move:
            if self.model.board[hx][hy] == 1:
                if clear:
                    icon_h = self.white_icon
                else:
                    icon_h = self.white_highlighted_icon
            elif self.model.board[hx][hy] == -1:
                if clear:
                    icon_h = self.black_icon
                else:
                    icon_h = self.black_highlighted_icon
            else:
                if clear:
                    icon_h = self.empty_icon
                else:
                    icon_h = self.empty_highlighted_icon
            self.chessButton[hx][hy].config(image=icon_h)

# check if the game end and if need to skip a player's round
    def game_end_check(self):
        # check win condition
        winner = self.model.win_check()
        if winner == 1:
            msg = messagebox.showwarning('Congratulations', 'White wins!')
            print(msg)
            self.initialize()
        elif winner == -1:
            msg = messagebox.showwarning('Congratulations', 'Black wins!')
            print(msg)
            self.initialize()
        else:
            legal_move_res = self.model.legal_move_check()
            if legal_move_res == -1:
                if self.model.round == 1:
                    player = 'White'
                else:
                    player = 'Black'
                msg = messagebox.showwarning('Warning', player + ' has no legal move!')
                print(msg)
            elif legal_move_res == 1:
                if self.model.round == 1:
                    self.round_text.set('Current Player: White')
                else:
                    self.round_text.set('Current Player: Black')
            else:
                msg = messagebox.showwarning('Oops', 'There is no legal move. Draw!')
                print(msg)
                self.initialize()

    def initialize(self):
        self.model.__init__()
        # initialize components
        self.chessButton = []
        self.time_text_black = StringVar(self, 'Black Total: 00:00   Step: 00')
        self.time_text_white = StringVar(self, 'White Total: 00:00   Step: 00')
        self.round_text = StringVar(self, 'Current Player: Black')
        # load components
        self.create_widgets()

