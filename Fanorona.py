from tkinter import *

class Filler:
    def __init__(self, master):
        self.filler = Frame(master, width=10)
        self.filler.pack(side=LEFT)

def draw_lines(x, y, w, h):
    thickness = w/400
    for i in range(9):
        c.create_line(x + (w / 18) + (w / 9) * i, y + (h / 10),
                      x + (w / 18) + (w / 9) * i, y + h - (h / 10), width=thickness)
    for i in range(5):
        c.create_line(x + (w / 18), y + (h / 10) + (h / 5) * i,
                      x + w - (w / 18), y + (h / 10) + (h / 5) * i, width=thickness)
    for i in range(3):
        c.create_line(x + (w / 18) + (w / 4.5) * i, y + (h / 10),
                      x + (w / 18) + w * (4 / 9) + (w / 4.5) * i, y + h - (h / 10), width=thickness)
    for i in range(3):
        c.create_line(x + (w / 18) + (w / 4.5) * i, y + h - (h / 10),
                      x + (w / 18) + w * (4 / 9) + (w / 4.5) * i, y + (h / 10), width=thickness)
    for i in range(2):
        c.create_line(x + (w / 18) + w * (6 / 9) * i, y + (h / 10) + h * (2 / 5) - h * (2 / 5) * i,
                      x + (w / 18) + w * (2 / 9) + w * (6 / 9) * i, y + h - (h / 10) - h * (2 / 5) * i, width=thickness)
    for i in range(2):
        c.create_line(x + (w / 18) + w * (6 / 9) * i, y + (h / 10) + h * (2 / 5) + h * (2 / 5) * i,
                      x + (w / 18) + w * (2 / 9) + w * (6 / 9) * i, y + (h / 10) + h * (2 / 5) * i, width=thickness)
    #c.create_oval(15, 15, 85, 85, fill="blue")

def draw_pieces(x, y, w, h):
    for i in range(5):
        for j in range(9):
            if positions[i][j] == 1:
                c.create_oval(x + (w * (15 / 900)) + (w / 9) * j, y + h * (15 / 500) + (h / 5) * i,
                              x + (w * (85 / 900)) + (w / 9) * j, y + h * (85 / 500) + (h / 5) * i, fill="black")
            elif positions[i][j] == 2:
                c.create_oval(x + (w * (15 / 900)) + (w / 9) * j, y + h * (15 / 500) + (h / 5) * i,
                              x + (w * (85 / 900)) + (w / 9) * j, y + h * (85 / 500) + (h / 5) * i, fill="white")

def render(event):
    width = correct_width = c.winfo_width()
    height = correct_height = c.winfo_height()

    if width/height > 9 / 5:
        correct_width = height * (9 / 5)
    else:
        correct_height = width * (5 / 9)

    c.delete(ALL)
    draw_lines((width - correct_width) / 2, (height - correct_height) / 2, correct_width, correct_height)
    draw_pieces((width - correct_width) / 2, (height - correct_height) / 2, correct_width, correct_height)

def set_positions():
    width = correct_width = c.winfo_width()
    height = correct_height = c.winfo_height()

    if width/height > 9 / 5:
        correct_width = height * (9 / 5)
    else:
        correct_height = width * (5 / 9)

    for i in range(2):
        for j in range(9):
            positions[i][j] = 1

    for i in range(2):
        for j in range(9):
            positions[i+3][j] = 2

    positions[2] = [1, 2, 1, 2, 0, 1, 2, 1, 2]
    draw_pieces((width - correct_width) / 2, (height - correct_height) / 2, correct_width, correct_height)
    #print(positions)

positions = []
for i in range(5):
    positions.append([])
    for j in range(9):
        positions[i].append(0)
#print(positions)

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
place = Button(menu, text="Place Pieces", command=set_positions)
place.pack()

c = Canvas(root, width=900, height=500)
c.pack(fill=BOTH, expand=1, side=LEFT)
c.bind("<Configure>", render)

root.mainloop()