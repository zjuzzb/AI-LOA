from tkinter import *


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, height=500, width=500)
        self.pack()
        self.empty_icon = PhotoImage(file='empty.png')
        self.black_icon = PhotoImage(file='black_chess.png')
        self.white_icon = PhotoImage(file='white_chess.png')
        self.chessButton = []
        self.create_widgets()

    def on_click(self, x, y):
        self.chessButton[x][y] = Button(self, height=80, width=80, bg='#EBCEAC', image = self.black_icon, command=(lambda x, y: lambda: self.on_click(x, y))(x, y))
        self.chessButton[x][y].grid(row=x,column=y)

    def create_widgets(self):
        for i in range(8):
            row = []
            for j in range(8):
                row.append(Button(self, height=80, width=80, bg='#EBCEAC', image = self.empty_icon, command=(lambda x, y: lambda: self.on_click(x, y))(i, j)))
            self.chessButton.append(row)
        for i in range(8):
            for j in range(8):
                self.chessButton[i][j].grid(row=i, column=j)

app = Application()
# 设置窗口标题:
app.master.title('Hello World')
# 主消息循环:
app.mainloop()