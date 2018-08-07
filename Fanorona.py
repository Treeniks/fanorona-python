from tkinter import *


# creating pieces list
pieces = []
movable = []
for i2 in range(5):
    pieces.append([])
    movable.append([])
    for j2 in range(9):
        pieces[i2].append(0)
        movable[i2].append(False)
# print(pieces)
# print(movable)


# ----------------------------------------------------------------------------------------------------------------------
# RENDERING:


# starting render process
def render():
    global width, correct_width, height, correct_height, dw, dh
    width = correct_width = c.winfo_width()
    height = correct_height = c.winfo_height()

    if (width / height) > 9 / 5:
        correct_width = round(height * (9 / 5))
    else:
        correct_height = round(width * (5 / 9))

    dw = round(correct_width / 9)
    dh = round(correct_height / 5)
    thickness = int(correct_width / 225)

    x = round(width / 2)
    y = round(height / 2)

    c.delete(ALL)
    draw_lines(x, y, correct_width, correct_height, dw, dh, thickness)
    draw_pieces(x, y, correct_width, correct_height, dw, dh, thickness)
    draw_movable(x, y, correct_width, correct_height, dw, dh)


# drawing board lines
def draw_lines(x, y, w, h, dw, dh, thickness):
    for i in range(-4, 5):
        c.create_line(x + dw * i, y - 2 * dh - int(w / 450),
                      x + dw * i, y + 2 * dh + round(w / 450), width=thickness)
    for i in range(-2, 3):
        c.create_line(x - dw * 4, y + dh * i,
                      x + dw * 4, y + dh * i, width=thickness)
    for i in range(-4, 1, 2):
        c.create_line(x + dw * i, y - 2 * dh,
                      x + dw * (i + 4), y + 2 * dh, width=thickness)
    for i in range(-4, 1, 2):
        c.create_line(x + dw * i, y + 2 * dh,
                      x + dw * (i + 4), y - 2 * dh, width=thickness)
    for i in range(-2, 3, 4):
        for j in range(-2, 3, 4):
            c.create_line(x + 2 * dw * i, y,
                          x + dw * i, y + dh * j, width=thickness)


# drawing board pieces
def draw_pieces(x, y, w, h, dw, dh, thickness):
    for i in range(5):
        for j in range(9):
            if pieces[i][j] == 1:
                c.create_oval(x + dw * (j - 4) - w * (25 / 900),
                              y + dh * (i - 2) - h * (25 / 500),
                              x + dw * (j - 4) + w * (25 / 900),
                              y + dh * (i - 2) + h * (25 / 500), fill="black", width=thickness)
            elif pieces[i][j] == 2:
                c.create_oval(x + dw * (j - 4) - w * (25 / 900),
                              y + dh * (i - 2) - h * (25 / 500),
                              x + dw * (j - 4) + w * (25 / 900),
                              y + dh * (i - 2) + h * (25 / 500), fill="white", width=thickness)
            elif pieces[i][j] == 3:
                c.create_oval(x + dw * (j - 4) - w * (25 / 900),
                              y + dh * (i - 2) - h * (25 / 500),
                              x + dw * (j - 4) + w * (25 / 900),
                              y + dh * (i - 2) + h * (25 / 500), fill="blue", width=thickness)
            elif pieces[i][j] == 4:
                c.create_oval(x + dw * (j - 4) - w * (25 / 900),
                              y + dh * (i - 2) - h * (25 / 500),
                              x + dw * (j - 4) + w * (25 / 900),
                              y + dh * (i - 2) + h * (25 / 500), fill="red", width=thickness)


def draw_movable(x, y, w, h, dw, dh):
    for i in range(5):
        for j in range(9):
            if movable[i][j]:
                c.create_oval(x + dw * (j - 4) - w * (10 / 900),
                                        y + dh * (i - 2) - h * (10 / 500),
                                        x + dw * (j - 4) + w * (10 / 900),
                                        y + dh * (i - 2) + h * (10 / 500), fill="blue", width=0)


# ----------------------------------------------------------------------------------------------------------------------
# GAME LOGIC:


def test_all_for_movability():
    for i in range(5):
        for j in range(9):
            movable[i][j] = is_movable(j, i)


def is_movable(x, y):
    if is_movable_by_approach(x, y) or is_movable_by_withdrawal(x, y):
        return True
    else:
        return False


def is_movable_by_approach(x, y):
    if pieces[y][x] == turn:
        if ((x < 7 and pieces[y][x + 1] == 0 and pieces[y][x + 2] == notturn)
                or (x > 1 and pieces[y][x - 1] == 0 and pieces[y][x - 2] == notturn)
                or (y < 3 and pieces[y + 1][x] == 0 and pieces[y + 2][x] == notturn)
                or (y > 1 and pieces[y - 1][x] == 0 and pieces[y - 2][x] == notturn)
                or (x + y) % 2 == 0 and (
                    (x < 7 and y < 3 and pieces[y + 1][x + 1] == 0 and pieces[y + 2][x + 2] == notturn)
                    or (x < 7 and y > 1 and pieces[y - 1][x + 1] == 0 and pieces[y - 2][x + 2] == notturn)
                    or (x > 1 and y > 1 and pieces[y - 1][x - 1] == 0 and pieces[y - 2][x - 2] == notturn)
                    or (x > 1 and y < 3 and pieces[y + 1][x - 1] == 0 and pieces[y + 2][x - 2] == notturn))):
            return True
        else:
            return False
    else:
        return False


def is_movable_by_withdrawal(x, y):
    if pieces[y][x] == turn:
        if ((0 < x < 8 and (
                    (pieces[y][x + 1] == 0 and pieces[y][x - 1] == notturn)
                    or (pieces[y][x - 1] == 0 and pieces[y][x + 1] == notturn)))
                or (0 < y < 4 and (
                    (pieces[y + 1][x] == 0 and pieces[y - 1][x] == notturn)
                    or (pieces[y - 1] == 0 and pieces[y + 1][x] == notturn)))
                or ((x + y) % 2 == 0 and 0 < x < 4 and 0 < y < 4 and (
                    (pieces[y + 1][x + 1] == 0 and pieces[y - 1][x - 1] == notturn)
                    or (pieces[y - 1][x + 1] == 0 and pieces[y + 1][x - 1] == notturn)
                    or (pieces[y - 1][x - 1] == 0 and pieces[y + 1][x + 1] == notturn)
                    or (pieces[y + 1][x - 1] == 0 and pieces[y - 1][x + 1] == notturn)))):
            return True
        else:
            return False
    else:
        return False


def how_movable(x, y):
    by = "none"
    if is_movable_by_approach(x, y):
        by = "approach"
    if is_movable_by_withdrawal(x, y):
        if by == "approach":
            by = "both"
        else:
            by = "withdrawal"
    return by


# movable_to_by_approach(piece_x, piece_y)
# -> possibilities dictionary {(dx1, dy1): "approach", (dx2, dy2): "approach"}
def movable_to_by_approach(x, y):
    possibilities_approach = {}
    if pieces[y][x] == turn:
        for i in range(-1, 2):  # vertical
            for j in range(-1, 2):  # horizontal
                if not (j == 0 and i == 0) and ((j == 0 and
                            ((i < 0 and y > 1) or (i > 0 and y < 3))
                            and pieces[y + i][x] == 0 and pieces[y + i + i][x] == notturn)
                        or (i == 0 and
                            ((j < 0 and x > 1) or (j > 0 and x < 7))
                            and pieces[y][x + j] == 0 and pieces[y][x + j + j] == notturn)
                        or ((x + y) % 2 == 0 and (
                            (i < 0 and j < 0 and x > 1 and y > 1)
                            or (i > 0 and j > 0 and x < 7 and y < 3)
                            or (j < 0 < i and x > 1 and y < 3)
                            or (i < 0 < j and x < 7 and y > 1))
                            and pieces[y + i][x + j] == 0 and pieces[y + i + i][x + j + j] == notturn)):
                    possibilities_approach[(j, i)] = "approach"
    return possibilities_approach


# movable_to_by_withdrawal(piece_x, piece_y)
# -> possibilities dictionary {(dx1, dy1): "withdrawal", (dx2, dy2): "withdrawal"}
def movable_to_by_withdrawal(x, y):
    possibilities_withdrawal = {}
    if pieces[y][x] == turn:
        for i in range(-1, 2):  # vertical
            for j in range(-1, 2):  # horizontal
                if not (j == 0 and i == 0) and (
                            (j == 0 < y < 4 and not i == 0
                            and pieces[y + i][x] == 0 and pieces[y - i][x] == notturn)
                        or (i == 0 < x < 8 and not j == 0
                            and pieces[y][x + j] == 0 and pieces[y][x - j] == notturn)
                        or ((x + y) % 2 == 0 and (
                            0 < x < 8 and 0 < y < 4
                            and pieces[y + i][x + j] == 0 and pieces[y - i][x - j] == notturn))):
                    possibilities_withdrawal[(j, i)] = "withdrawal"
    return possibilities_withdrawal


# combine_possibilities(approach_dictionary, withdrawal_dictionary)
# -> possibilities dictionary {(dx1, dy1): "approach", (dx2, dy2): "withdrawal", (dx3, dy3): "both"}
def combine_possibilities(approach, withdrawal):
    possibilities = {}
    for i in approach:
        for j in withdrawal:
            if i == j:
                possibilities[i] = "both"
        if i not in possibilities:
            possibilities[i] = "approach"
    for i in withdrawal:
        if i not in possibilities:
            possibilities[i] = "withdrawal"
    return possibilities


def remove_pieces(x1, y1, x2, y2, possibilities):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if x2 - x1 == j and y2 - y1 == i:
                k1 = 0
                k2 = 0
                if possibilities[j, i] == "approach":
                    while -1 < x2 + j + k2 < 9 and -1 < y2 + i + k1 < 5 and pieces[y2 + i + k1][x2 + j + k2] == notturn:
                        pieces[y2 + i + k1][x2 + j + k2] = 0
                        k1 += i
                        k2 += j
                elif possibilities[j, i] == "withdrawal":
                    while -1 < x1 - j - k2 < 9 and -1 < y1 - i - k1 < 5 and pieces[y1 - i - k1][x1 - j - k2] == notturn:
                        pieces[y1 - i - k1][x1 - j - k2] = 0
                        k1 += i
                        k2 += j


# ----------------------------------------------------------------------------------------------------------------------
# BUTTON COMMANDS:


def set_pieces():
    global turn, notturn, is_moving, pieces
    for i in range(2):
        for j in range(9):
            pieces[i][j] = 1
    for i in range(3, 5):
        for j in range(9):
            pieces[i][j] = 2
    pieces[2] = [1, 2, 1, 2, 0, 1, 2, 1, 2]
    # pieces = [[1, 1, 1, 0, 1, 0, 1, 0, 1], [2, 0, 2, 1, 2, 1, 2, 1, 2], [0, 1, 1, 1, 1, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2]]
    # pieces = [[1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2]]
    # pieces = [[1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 2, 1, 0, 0, 0, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2]]
    pieces = [[1, 1, 1, 1, 1, 1, 1, 1, 1], [2, 0, 2, 1, 2, 1, 2, 1, 2], [0, 1, 1, 1, 1, 0, 1, 1, 1], [0, 1, 0, 2, 1, 0, 0, 0, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2]]
    # pieces = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 2, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    turn = 2
    notturn = 1
    is_moving = False

    test_all_for_movability()

    render()


def reset_pieces():
    for i in range(5):
        for j in range(9):
            pieces[i][j] = 0
            movable[i][j] = 0

    render()


def clear():
    c.delete(ALL)


# ----------------------------------------------------------------------------------------------------------------------
# EVENTS:


def resize(event):
    render()


def click(event):
    # global width, correct_width, height, correct_height, dw, dh
    global moving_x, moving_y, is_moving, possibilities
    if (event.x < (width - correct_width) / 2
            or event.x > ((width - correct_width) / 2) + correct_width
            or event.y < (height - correct_height) / 2
            or event.y > ((height - correct_height) / 2) + correct_height):
        return
    selected_x = int((event.x - (width - correct_width) / 2) / dw)
    selected_y = int((event.y - (height - correct_height) / 2) / dh)
    if not is_moving:
        moving_x = selected_x
        moving_y = selected_y
        possibilities = combine_possibilities(movable_to_by_approach(selected_x, selected_y), movable_to_by_withdrawal(selected_x, selected_y))
        pieces[selected_y][selected_x] = 3
        is_moving = True
    else:
        remove_pieces(moving_x, moving_y, selected_x, selected_y, possibilities)
    # print(is_movable_by_approach(selected_x, selected_y))
    # print(is_movable_by_withdrawal(selected_x, selected_y))
    # print(movable_to_by_approach(selected_x, selected_y))
    # print(movable_to_by_withdrawal(selected_x, selected_y))
    # print(combine_possibilities(movable_to_by_approach(selected_x, selected_y), movable_to_by_withdrawal(selected_x, selected_y)))
    # for i in movable_to_by_approach(selected_x, selected_y):
        # print(i)
        # movable[selected_y + i[1]][selected_x + i[0]] = True
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
place = Button(menu, text="Start Game", command=set_pieces)
place.pack()
reset = Button(menu, text="Reset Pieces", command=reset_pieces)
reset.pack()

c = Canvas(root, width=900, height=500)
c.pack(fill=BOTH, expand=1, side=LEFT)
c.bind("<Configure>", resize)
c.bind("<Button-1>", click)

root.mainloop()
