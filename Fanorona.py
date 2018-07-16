from tkinter import *

class Filler:
    def __init__(self, master):
        self.filler = Frame(master, width=10)
        self.filler.pack(side=LEFT)

def draw_lines(x, y, w, h):
    for i in range(9):
        c.create_line(x+(w/18) + (w/9)*i, y + (h/10), x+(w/18) + (w/9)*i, y + h - (h/10), width=2)
    for i in range(5):
        c.create_line(x + (w/18), y+(h/10) + (h/5)*i, x + w - (w/18), y+(h/10) + (h/5)*i, width=2)
    for i in range(3):
        c.create_line(x+(w/18) + (w/4.5)*i, y + (h/10), x+(w/18) + w*(4/9) + (w/4.5)*i, y + h - (h/10), width=2)
    for i in range(3):
        c.create_line(x+(w/18) + (w/4.5)*i, y + h - (h/10), x+(w/18) + w*(4/9) + (w/4.5)*i, y + (h/10), width=2)
    for i in range(2):
        c.create_line(x+(w/18) + w*(6/9)*i, y+(h/10)+h*(2/5) - h*(2/5)*i, x+(w/18)+w*(2/9) + w*(6/9)*i, y+h-(h/10) - h*(2/5)*i, width=2)
    for i in range(2):
        c.create_line(x+(w/18) + w*(6/9)*i, y+(h/10)+h*(2/5) + h*(2/5)*i, x+(w/18)+w*(2/9) + w*(6/9)*i, y+(h/10) + h*(2/5)*i, width=2)
    c.create_oval(15, 15, 85, 85, fill="blue")

def render(event):
    width = correct_width = c.winfo_width()
    height = correct_height = c.winfo_height()

    if width/height > 9 / 5:
        correct_width = height * (9 / 5)
    else:
        correct_height = width * (5 / 9)

    c.delete(ALL)
    draw_lines((width - correct_width) / 2, (height - correct_height) / 2, correct_width, correct_height)

root = Tk()
root.title("Fanorona")

#filler = Filler(root)

list = Listbox(root)
list.pack(fill=Y, side=LEFT)

filler2 = Filler(root)

menu = Frame(root)
menu.pack(side=LEFT)

reset = Button(menu, text="Reset Pieces")
reset.pack()
place = Button(menu, text="Place Pieces")
place.pack()

c = Canvas(root, width = 900, height = 500)
c.pack(fill=BOTH, expand=1, side=LEFT)
c.bind("<Configure>", render)

root.mainloop()