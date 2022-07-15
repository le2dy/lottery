from tkinter import *


class exam(Frame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.pack(fill=BOTH, expand=1)
        canvas = Canvas(self)
        canvas.create_line(0, 0, 300, 300)

        canvas.pack(fill=BOTH, expand=1)


def main():
    root = Tk()
    root.title('Tic Tac Toe')
    w = str(int(root.winfo_screenwidth() / 2) - 150)
    h = str(int(root.winfo_screenheight() / 2) - 150)
    root.geometry("300x300+" + w + "+" + h)
    root.mainloop()


if __name__ == '__main__':
    main()
