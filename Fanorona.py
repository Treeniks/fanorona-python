from tkinter import *


# creating positions list
positions = []
for i2 in range(5):
    positions.append([])
    for j2 in range(9):
        positions[i2].append(0)
# print(positions)
movable = []
for i2 in range(5):
    movable.append([])
    for j2 in range(9):
        movable[i2].append(False)
# print(moveable)
is_moving = False
turn = 2


# ----------------------------------------------------------------------------------------------------------------------
# Rendering:


# starting render process
def render():
    global width, height, correct_width, correct_height, dw, dh
    width = correct_width = c.winfo_width()
    height = correct_height = c.winfo_height()

    if width/height > 9 / 5:
        correct_width = round(height * (9 / 5))
    else:
        correct_height = round(width * (5 / 9))

    dw = round(correct_width / 9)
    dh = round(correct_height / 5)

    c.delete(ALL)
    draw_lines(round(width / 2), round(height / 2), correct_width, correct_height)
    draw_pieces(round(width / 2), round(height / 2), correct_width, correct_height)
    draw_moveable(round(width / 2), round(height / 2), correct_width, correct_height)


# drawing board lines
def draw_lines(x, y, w, h):
    thickness = int(w / 225)

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
            elif positions[i][j] == 3:
                c.create_oval(x + dw * (j - 4) - w * (25 / 900),
                              y + dh * (i - 2) - h * (25 / 500),
                              x + dw * (j - 4) + w * (25 / 900),
                              y + dh * (i - 2) + h * (25 / 500), fill="blue", width=thickness)


# drawing blue movable dots
def draw_moveable(x, y, w, h):
    if not is_moving:
        for i in range(5):
            for j in range(9):
                test_movable(j, i)
    else:
        test_movable_selected(movingx, movingy)

    for i in range(5):
        for j in range(9):
            if movable[i][j]:
                c.create_oval(x + dw * (j - 4) - w * (10 / 900),
                              y + dh * (i - 2) - h * (10 / 500),
                              x + dw * (j - 4) + w * (10 / 900),
                              y + dh * (i - 2) + h * (10 / 500), fill="blue", width=0)


# ----------------------------------------------------------------------------------------------------------------------
# Button commands + Game Logic:


def set_positions():
    global is_moving, turn, positions
    '''for i in range(2):
        for j in range(9):
            positions[i][j] = 1
    for i in range(3, 5):
        for j in range(9):
            positions[i][j] = 2
    positions[2] = [1, 2, 1, 2, 0, 1, 2, 1, 2]'''
    positions = [[1, 1, 1, 0, 1, 0, 1, 0, 1], [2, 0, 2, 1, 2, 1, 2, 1, 2], [1, 1, 1, 0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2]]
    is_moving = False
    turn = 2
    render()


def reset_positions():
    global is_moving, turn
    for i in range(5):
        for j in range(9):
            positions[i][j] = 0
    is_moving = False
    turn = 2
    render()


def clear():
    c.delete(ALL)


def test_movable(x, y):
    if positions[y][x] == turn:
        if y > 0 and positions[y-1][x] == 0:
            if test_movable_selected(x, y, True):
                movable[y][x] = True
            else:
                movable[y][x] = False
        elif y < 4 and positions[y+1][x] == 0:
            if test_movable_selected(x, y, True):
                movable[y][x] = True
            else:
                movable[y][x] = False
        elif x > 0 and positions[y][x-1] == 0:
            if test_movable_selected(x, y, True):
                movable[y][x] = True
            else:
                movable[y][x] = False
        elif x < 8 and positions[y][x+1] == 0:
            if test_movable_selected(x, y, True):
                movable[y][x] = True
            else:
                movable[y][x] = False
        elif (x + y) % 2 == 0:
            if x > 0 and y > 0 and positions[y-1][x-1] == 0:
                if test_movable_selected(x, y, True):
                    movable[y][x] = True
                else:
                    movable[y][x] = False
            elif x < 8 and y > 0 and positions[y-1][x+1] == 0:
                if test_movable_selected(x, y, True):
                    movable[y][x] = True
                else:
                    movable[y][x] = False
            elif x > 0 and y < 4 and positions[y+1][x-1] == 0:
                if test_movable_selected(x, y, True):
                    movable[y][x] = True
                else:
                    movable[y][x] = False
            elif x < 8 and y < 4 and positions[y+1][x+1] == 0:
                if test_movable_selected(x, y, True):
                    movable[y][x] = True
                else:
                    movable[y][x] = False
        else:
            movable[y][x] = False
    else:
        movable[y][x] = False


def test_movable_selected(x, y, checking=False):
    if y > 1 and positions[y-1][x] == 0 and not positions[y-2][x] == turn and not positions[y-2][x] == 0:  # North
        if checking:
            return True
        else:
            movable[y-1][x] = True
    if y < 3 and positions[y+1][x] == 0 and not positions[y+2][x] == turn and not positions[y+2][x] == 0:  # South
        if checking:
            return True
        else:
            movable[y+1][x] = True
    if x > 1 and positions[y][x-1] == 0 and not positions[y][x-2] == turn and not positions[y][x-2] == 0:  # West
        if checking:
            return True
        else:
            movable[y][x-1] = True
    if x < 7 and positions[y][x+1] == 0 and not positions[y][x+2] == turn and not positions[y][x+2] == 0:  # East
        if checking:
            return True
        else:
            movable[y][x+1] = True
    if (x + y) % 2 == 0:
        if x > 1 and y > 1 and positions[y-1][x-1] == 0 and not positions[y-2][x-2] == turn and not positions[y-2][x-2] == 0:  # North-West
            if checking:
                return True
            else:
                movable[y-1][x-1] = True
        if x < 7 and y > 1 and positions[y-1][x+1] == 0 and not positions[y-2][x+2] == turn and not positions[y-2][x+2] == 0:  # North-East
            if checking:
                return True
            else:
                movable[y-1][x+1] = True
        if x > 1 and y < 3 and positions[y+1][x-1] == 0 and not positions[y+2][x-2] == turn and not positions[y+2][x-2] == 0:  # South-West
            if checking:
                return True
            else:
                movable[y+1][x-1] = True
        if x < 7 and y < 3 and positions[y+1][x+1] == 0 and not positions[y+2][x+2] == turn and not positions[y+2][x+2] == 0:  # South-East
            if checking:
                return True
            else:
                movable[y+1][x+1] = True
    if checking:
        return False


def remove_in_direction(direction, x, y):
    print(direction)
    i = 1
    if direction == "N":
        while y - i > -1 and not positions[y - i][x] == turn and not positions[y - i][x] == 0:
            positions[y - i][x] = 0
            i += 1
    elif direction == "E":
        while x + i < 9 and not positions[y][x + i] == turn and not positions[y][x + i] == 0:
            positions[y][x + i] = 0
            i += 1
    elif direction == "S":
        while y + i < 5 and not positions[y + i][x] == turn and not positions[y + i][x] == 0:
            positions[y + i][x] = 0
            i += 1
    elif direction == "W":
        while x - i > -1 and not positions[y][x - i] == turn and not positions[y][x - i] == 0:
            positions[y][x - i] = 0
            i += 1
    elif direction == "NE":
        while y - i > -1 and x + i < 9 and not positions[y - i][x + i] == turn and not positions[y - i][x + i] == 0:
            positions[y - i][x + i] = 0
            i += 1
    elif direction == "SE":
        while y + i < 5 and x + i < 9 and not positions[y + i][x + i] == turn and not positions[y + i][x + i] == 0:
            positions[y + i][x + i] = 0
            i += 1
    elif direction == "SW":
        while y + i < 5 and x - i > -1 and not positions[y + i][x - i] == turn and not positions[y + i][x - i] == 0:
            positions[y + i][x - i] = 0
            i += 1
    elif direction == "NW":
        while y - i > -1 and x - i > -1 and not positions[y - i][x - i] == turn and not positions[y - i][x - i] == 0:
            positions[y - i][x - i] = 0
            i += 1


# ----------------------------------------------------------------------------------------------------------------------
# Events:


def resize(event):
    render()


def click(event):
    global is_moving, movingx, movingy, turn
    if event.x < (width - correct_width) / 2 or event.x > ((width - correct_width) / 2) + correct_width or event.y < (height - correct_height) / 2 or event.y > ((height - correct_height) / 2) + correct_height: return
    piecex = int((event.x - (width - correct_width) / 2) / dw)
    piecey = int((event.y - (height - correct_height) / 2) / dh)
    print(piecex, piecey)
    # print(x, y)
    if not is_moving:
            # if test_movable(True, x, y):
        if movable[piecey][piecex]:
            positions[piecey][piecex] = 3
            movingx = piecex
            movingy = piecey
            is_moving = True
            for i in range(5):
                for j in range(9):
                    movable[i][j] = False
            # print(movingx, movingy)
            render()
    else:
        if movable[piecey][piecex]:
            # print(movingx, movingy)
            positions[piecey][piecex] = turn
            positions[movingy][movingx] = 0
            if piecey == movingy - 1 and piecex == movingx:
                direction = "N"
            elif piecey == movingy and piecex == movingx + 1:
                direction = "E"
            elif piecey == movingy + 1 and piecex == movingx:
                direction = "S"
            elif piecey == movingy and piecex == movingx - 1:
                direction = "W"
            elif piecey == movingy - 1 and piecex == movingx + 1:
                direction = "NE"
            elif piecey == movingy + 1 and piecex == movingx + 1:
                direction = "SE"
            elif piecey == movingy + 1 and piecex == movingx - 1:
                direction = "SW"
            elif piecey == movingy - 1 and piecex == movingx - 1:
                direction = "NW"
            remove_in_direction(direction, piecex, piecey)
            is_moving = False
            if turn == 2: turn = 1
            else: turn = 2
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
place = Button(menu, text="Start Game", command=set_positions)
place.pack()
reset = Button(menu, text="Reset Pieces", command=reset_positions)
reset.pack()

c = Canvas(root, width=900, height=500)
c.pack(fill=BOTH, expand=1, side=LEFT)
c.bind("<Configure>", resize)
c.bind("<Button-1>", click)

root.mainloop()
