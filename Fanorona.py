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
    draw_lines((width - correct_width) / 2, (height - correct_height) / 2, correct_width, correct_height)
    draw_pieces((width - correct_width) / 2, (height - correct_height) / 2, correct_width, correct_height)


# drawing board lines
def draw_lines(x, y, w, h):
    thickness = w/225
    dw = int(w / 18)
    dh = int(h / 10)

    for i in range(9):
        c.create_line(x + dw + 2 * dw * i,
                      y + dh,
                      x + dw + 2 * dw * i,
                      y + 9 * dh,
                      width=thickness)
    for i in range(5):
        c.create_line(x + dw,
                      y + dh + 2 * dh * i,
                      x + 17 * dw,
                      y + dh + 2 * dh * i,
                      width=thickness)
    for i in range(3):
        c.create_line(x + dw + 4 * dw * i,
                      y + dh,
                      x + 9 * dw + 4 * dw * i,
                      y + 9 * dh,
                      width=thickness)
    for i in range(3):
        c.create_line(x + dw + 4 * dw * i,
                      y + 9 * dh,
                      x + 9 * dw + 4 * dw * i,
                      y + dh,
                      width=thickness)
    for i in range(2):
        c.create_line(x + dw,
                      y + 5 * dh,
                      x + 5 * dw,
                      y + dh + 8 * dh * i,
                      width=thickness)
    for i in range(2):
        c.create_line(x + 17 * dw,
                      y + 5 * dh,
                      x + 13 * dw,
                      y + dh + 8 * dh * i,
                      width=thickness)

    # c.create_oval(15, 15, 85, 85, fill="blue")


# drawing board pieces
def draw_pieces(x, y, w, h):
    thickness = w/225
    dw = int(w / 18)
    dh = int(h / 10)

    for i in range(5):
        for j in range(9):
            if positions[i][j] == 1:
                c.create_oval(x + w * (25 / 900) + 2 * dw * j,
                              y + h * (25 / 500) + 2 * dh * i,
                              x + w * (75 / 900) + 2 * dw * j,
                              y + h * (75 / 500) + 2 * dh * i, fill="black", width=thickness)
            elif positions[i][j] == 2:
                c.create_oval(x + w * (25 / 900) + 2 * dw * j,
                              y + h * (25 / 500) + 2 * dh * i,
                              x + w * (75 / 900) + 2 * dw * j,
                              y + h * (75 / 500) + 2 * dh * i, fill="white", width=thickness)


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
