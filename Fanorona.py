from tkinter import *


positions = []
for i2 in range(5):
    positions.append([])
    for j2 in range(9):
        positions[i2].append(0)
print(positions)


# ----------------------------------------------------------------------------------------------------------------------


def render(move=False, x=0, y=0):
    width = correct_width = c.winfo_width()
    height = correct_height = c.winfo_height()

    if width/height > 9 / 5:
        correct_width = height * (9 / 5)
    else:
        correct_height = width * (5 / 9)

    c.delete(ALL)
    # c.create_rectangle(1,1,width-1,height-1, width=5)
    if move:
        c.create_oval(x, y, x + 50, y + 50, fill="blue")
    draw_lines((width - correct_width) / 2, (height - correct_height) / 2, correct_width, correct_height)
    draw_pieces((width - correct_width) / 2, (height - correct_height) / 2, correct_width, correct_height)


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
    # c.create_oval(15, 15, 85, 85, fill="blue")


def draw_pieces(x, y, w, h):
    for i in range(5):
        for j in range(9):
            if positions[i][j] == 1:
                c.create_oval(x + (w * (25 / 900)) + (w / 9) * j,
                              y + h * (25 / 500) + (h / 5) * i,
                              x + (w * (75 / 900)) + (w / 9) * j,
                              y + h * (75 / 500) + (h / 5) * i, fill="black", width=w/400)
                # print(w,x + (w * (75 / 900)) + (w / 9) * j + w/400)
            elif positions[i][j] == 2:
                c.create_oval(x + (w * (25 / 900)) + (w / 9) * j,
                              y + h * (25 / 500) + (h / 5) * i,
                              x + (w * (75 / 900)) + (w / 9) * j,
                              y + h * (75 / 500) + (h / 5) * i, fill="white", width=w/400)
                # print(w,x + (w * (75 / 900)) + (w / 9) * j + w/400)


# ----------------------------------------------------------------------------------------------------------------------


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
    c.delete("all")


# ----------------------------------------------------------------------------------------------------------------------


def resize(event):
    render()


def mouse(event):
    # c.create_oval(event.x, event.y, event.x+50, event.y+50, fill="blue")
    render(True, event.x, event.y)


# ----------------------------------------------------------------------------------------------------------------------


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
c.bind("<Motion>", mouse)

root.mainloop()
