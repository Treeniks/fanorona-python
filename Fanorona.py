from tkinter import *


# creating positions list
positions = []
for i2 in range(5):
    positions.append([])
    for j2 in range(9):
        positions[i2].append(0)
# print(positions)


# ----------------------------------------------------------------------------------------------------------------------
# Rendering:


# starting render process
def render():
    width = correct_width = c.winfo_width()
    height = correct_height = c.winfo_height()

    if width/height > 9 / 5:
        correct_width = height * (9 / 5)
    else:
        correct_height = width * (5 / 9)

    c.delete(ALL)
    draw_lines(round(width / 2), round(height / 2), round(correct_width), round(correct_height))
    draw_pieces(round(width / 2), round(height / 2), round(correct_width), round(correct_height))


# drawing board lines
def draw_lines(x, y, w, h):
    thickness = int(w / 225)
    dw = round(w / 9)
    dh = round(h / 5)

    for i in range(-4, 5):
        c.create_line(x + dw * i, y - 2 * dh - int(w / 450),
                      x + dw * i, y + 2 * dh + round(w / 450), width=thickness)
    for i in range(-2, 3):
        c.create_line(x - dw * 4, y + dh * i,
                      x + dw * 4, y + dh * i, width=thickness)
    for i in range(-4, 1, 2):
        c.create_line(x + dw * i, y - 2 * dh, x + dw * (i + 4), y + 2 * dh, width=thickness)
    for i in range(-4, 1, 2):
        c.create_line(x + dw * i, y + 2 * dh, x + dw * (i + 4), y - 2 * dh, width=thickness)
    for i in range(-2, 3, 4):
        for j in range(-2, 3, 4):
            c.create_line(x + 2 * dw * i, y, x + dw * i, y + dh * j, width=thickness)


# drawing board pieces
def draw_pieces(x, y, w, h):
    thickness = int(w / 225)
    dw = round(w / 9)
    dh = round(h / 5)

    for i in range(5):
        for j in range(9):
            if positions[i][j] == 1:
                c.create_oval(x + dw * (j - 4) - w * (25 / 900),
                              y + dh * (i - 2) - h * (25 / 500),
                              x + dw * (j - 4) + w * (25 / 900),
                              y + dh * (i - 2) + h * (25 / 500), fill="black", width=thickness)
            elif positions[i][j] == 2:
                c.create_oval(x + dw * (j - 4) - w * (25 / 900),
                              y + dh * (i - 2) - h * (25 / 500),
                              x + dw * (j - 4) + w * (25 / 900),
                              y + dh * (i - 2) + h * (25 / 500), fill="white", width=thickness)


# ----------------------------------------------------------------------------------------------------------------------
# Button commands:


def set_positions():
    for i in range(2):
        for j in range(9):
            positions[i][j] = 1
    for i in range(3, 5):
        for j in range(9):
            positions[i][j] = 2
    positions[2] = [1, 2, 1, 2, 0, 1, 2, 1, 2]

    render()


def reset_positions():
    for i in range(5):
        for j in range(9):
            positions[i][j] = 0

    render()


def clear():
    c.delete(ALL)


# ----------------------------------------------------------------------------------------------------------------------
# Events:


def resize(event):
    render()


# ----------------------------------------------------------------------------------------------------------------------
# Interface:


def create_filler(master):
    filler = Frame(master, width=10)
    filler.pack(side=LEFT)


root = Tk()
root.title("Fanorona")
root.minsize(width=600, height=250)

# create_filler(root)

listbox = Listbox(root)
listbox.pack(fill=Y, side=LEFT)

create_filler(root)

menu = Frame(root)
menu.pack(side=LEFT)

clear = Button(menu, text="Clear Everything", command=clear)
clear.pack()
place = Button(menu, text="Place Pieces", command=set_positions)
place.pack()
reset = Button(menu, text="Reset Pieces", command=reset_positions)
reset.pack()

c = Canvas(root, width=900, height=500)
c.pack(fill=BOTH, expand=1, side=LEFT)
c.bind("<Configure>", resize)

root.mainloop()
