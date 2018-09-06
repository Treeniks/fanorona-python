from tkinter import *


pieces = []
movable = []
for i2 in range(5):
    pieces.append([])
    movable.append([])
    for j2 in range(9):
        pieces[i2].append(0)
        movable[i2].append(False)
directions_basic = [(0, 1), (1, 0), (0, -1), (-1, 0)]
directions_advanced = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
directions_advanced.extend(directions_basic)
direction = ()
aw = {}
positions = []
asking = []
ask_player = False


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
    draw_lines(x, y, correct_width, correct_height, thickness)
    draw_arrows(x, y, correct_width, correct_height, thickness)
    draw_pieces(x, y, correct_width, correct_height, thickness)
    draw_movable(x, y, correct_width, correct_height)
    draw_positions(x, y, correct_width, correct_height)
    draw_asking(x, y, correct_width, correct_height)


# drawing board lines
def draw_lines(x, y, w, h, thickness):
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
def draw_pieces(x, y, w, h, thickness):
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


def draw_movable(x, y, w, h):
    for i in range(5):
        for j in range(9):
            if movable[i][j]:
                c.create_oval(x + dw * (j - 4) - w * (10 / 900),
                              y + dh * (i - 2) - h * (10 / 500),
                              x + dw * (j - 4) + w * (10 / 900),
                              y + dh * (i - 2) + h * (10 / 500), fill="blue", width=0)


def draw_positions(x, y, w, h):
    for i in range(len(positions) - 1):
        c.create_oval(x + dw * (positions[i][0] - 4) - w * (10 / 900),
                      y + dh * (positions[i][1] - 2) - h * (10 / 500),
                      x + dw * (positions[i][0] - 4) + w * (10 / 900),
                      y + dh * (positions[i][1] - 2) + h * (10 / 500), fill="red", width=0)


def draw_arrows(x, y, w, h, thickness):
    for i in range(len(positions) - 1):
        # c.create_line(x - (4 - positions[i][0]) * dw,
                      # y - (2 - positions[i][1]) * dh,
                      # x - (4 - positions[i + 1][0]) * dw - w * (10 / 900),
                      # y - (2 - positions[i + 1][1]) * dh - h * (10 / 500), arrow="last", fill="black", width=(thickness + thickness))
        c.create_line(x - (4 - positions[i][0]) * dw,
                      y - (2 - positions[i][1]) * dh,
                      x - (4 - positions[i + 1][0]) * dw,
                      y - (2 - positions[i + 1][1]) * dh, fill="red", width=thickness)
        c.create_line(x - (4 - positions[i][0]) * dw,
                      y - (2 - positions[i][1]) * dh,
                      ((x - (4 - positions[i + 1][0]) * dw) + (x - (4 - positions[i][0]) * dw)) / 2,
                      ((y - (2 - positions[i + 1][1]) * dh) + (y - (2 - positions[i][1]) * dh)) / 2, fill="red", arrow="last", width=thickness)


def draw_asking(x, y, w, h):
    for i in asking:
        c.create_oval(x + dw * (i[0] -4) - w * (10 / 900),
                      y + dh * (i[1] - 2) - h * (10 / 500),
                      x + dw * (i[0] - 4) + w * (10 / 900),
                      y + dh * (i[1] - 2) + h * (10 / 500), fill="yellow", width=0)


# ----------------------------------------------------------------------------------------------------------------------
# GAME LOGIC:


def create_tempdirection(x, y):
    if (x + y) % 2 == 0:
        tempdirection = directions_advanced
    else:
        tempdirection = directions_basic
    return tempdirection


def in_bounce_approach(x, y, i):
    if -1 < x + i[0] + i[0] < 9 and -1 < y + i[1] + i[1] < 5:
        return True
    else:
        return False


def in_bounce_withdrawal(x, y, i):
    if -1 < x - i[0] < 9 and -1 < y - i[1] < 5 and -1 < x + i[0] < 9 and -1 < y + i[1] < 5:
        return True
    else:
        return False


def in_bounce_paika(x, y, i):
    if -1 < x + i[0] < 9 and -1 < y + i[1] < 5:
        return True
    else:
        return False


def reset_movable():
    for i in range(5):
        for j in range(9):
            movable[i][j] = False


def mark_all_movables():
    global paika
    reset_movable()
    for i in range(5):
        for j in range(9):
            if pieces[i][j] == turn:
                movable[i][j] = check_single_movable(j, i)
    if no_movables():
        paika = True
        for i in range(5):
            for j in range(9):
                if pieces[i][j] == turn:
                    movable[i][j] = check_single_paika(j, i)
    else:
        paika = False


def mark_to_movables(x, y):
    tempdirection = create_tempdirection(x, y)
    if not paika:
        for i in tempdirection:
            # print(positions)
            # print(direction)
            # print(x, y, i)
            if possible_approach(x, y, i) and (x + i[0], y + i[1]) not in positions and not direction == i:
                # print(True)
                movable[y + i[1]][x + i[0]] = True
                aw[(x + i[0], y + i[1])] = "approach"
            if possible_withdrawal(x, y, i) and (x + i[0], y + i[1]) not in positions and not direction == i:
                # print(True)
                movable[y + i[1]][x + i[0]] = True
                if (x + i[0], y + i[1]) in aw:
                    aw[(x + i[0], y + i[1])] = "both"
                else:
                    aw[(x + i[0], y + i[1])] = "withdrawal"
            # print(aw)
    else:
        for i in tempdirection:
            if possible_paika(x, y, i):
                movable[y + i[1]][x + i[0]] = True


def check_single_movable(x, y):
    tempdirection = create_tempdirection(x, y)
    for i in tempdirection:
        if possible_approach(x, y, i) or possible_withdrawal(x, y, i):
            return True
    return False


def check_single_paika(x, y):
    tempdirection = create_tempdirection(x, y)
    for i in tempdirection:
        if possible_paika(x, y, i):
            return True
    return False


def possible_approach(x, y, i):
    if in_bounce_approach(x, y, i) and pieces[y + i[1]][x + i[0]] == 0 and pieces[y + i[1] + i[1]][x + i[0] + i[0]] == notturn:
        # print(x, i[0], y, i[1])
        return True


def possible_withdrawal(x, y, i):
    if in_bounce_withdrawal(x, y, i) and pieces[y + i[1]][x + i[0]] == 0 and pieces[y - i[1]][x - i[0]] == notturn:
        return True


def possible_paika(x, y, i):
    if in_bounce_paika(x, y, i) and pieces[y + i[1]][x + i[0]] == 0:
        return True


def no_movables():
    for i in range(5):
        for j in range(9):
            if movable[i][j]:
                return False
    return True


def paika_single_check(x, y):
    tempdirection = create_tempdirection(x, y)
    for i in tempdirection:
        if (possible_approach(x, y, i) and (x + i[0], y + i[1]) not in positions and not direction == i) or (
                possible_withdrawal(x, y, i) and (x + i[0], y + i[1]) not in positions and not direction == i):
            return False
    return True


def switch_turn():
    global turn, notturn
    if turn == 1:
        turn = 2
        notturn = 1
    elif turn == 2:
        turn = 1
        notturn = 2
    else:
        print("Error: Unknown turns")


def remove_pieces(x1, y1, x2, y2):
    global ask_player, asking
    for i in range(-1, 2):
        for j in range(-1, 2):
            if x2 - x1 == j and y2 - y1 == i:
                k1 = 0
                k2 = 0
                if aw[x2, y2] == "both":
                    asking = [(x2 + j, y2 + i), (x1 - j, y1 - i)]
                    ask_player = True
                    render()
                elif aw[x2, y2] == "approach":
                    # print("approach")
                    # print(x2, j, k2, "and", y2, i, k1)
                    while -1 < x2 + j + k2 < 9 and -1 < y2 + i + k1 < 5 and pieces[y2 + i + k1][x2 + j + k2] == notturn:
                        pieces[y2 + i + k1][x2 + j + k2] = 0
                        k1 += i
                        k2 += j
                elif aw[x2, y2] == "withdrawal":
                    # print("withdrawal")
                    while -1 < x1 - j - k2 < 9 and -1 < y1 - i - k1 < 5 and pieces[y1 - i - k1][x1 - j - k2] == notturn:
                        pieces[y1 - i - k1][x1 - j - k2] = 0
                        k1 += i
                        k2 += j


# ----------------------------------------------------------------------------------------------------------------------
# BUTTON COMMANDS:


def set_pieces():
    global turn, notturn, is_moving, pieces, positions, aw, direction, ask_player, asking
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
    # pieces = [[1, 1, 1, 1, 0, 1, 1, 1, 1], [2, 0, 2, 1, 2, 1, 2, 1, 2], [0, 1, 1, 1, 1, 0, 1, 1, 1], [2, 1, 0, 2, 1, 0, 0, 0, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2]]
    # pieces = [[1, 0, 2, 1, 0, 0, 0, 0, 0], [2, 0, 1, 2, 0, 0, 0, 0, 1], [0, 0, 1, 0, 2, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    turn = 2
    notturn = 1
    is_moving = False
    positions = []
    aw = {}
    direction = ()
    ask_player = False
    asking = []

    mark_all_movables()
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
    global is_moving, moving_x, moving_y, direction, aw, positions, ask_x, ask_y, ask_player, asking
    if (event.x < (width - correct_width) / 2
            or event.x > ((width - correct_width) / 2) + correct_width
            or event.y < (height - correct_height) / 2
            or event.y > ((height - correct_height) / 2) + correct_height):
        return
    x = int((event.x - (width - correct_width) / 2) / dw)
    y = int((event.y - (height - correct_height) / 2) / dh)
    if not ask_player:
        if pieces[y][x] == 3 and len(positions) == 1:
            pieces[y][x] = turn
            mark_all_movables()
            is_moving = False
            direction = ()
            aw = {}
            positions = []
            render()
            return
        if not movable[y][x]:
            return
        # player selects a piece to move
        if not is_moving:
            reset_movable()
            mark_to_movables(x, y)
            moving_x = x
            moving_y = y
            is_moving = True
            pieces[y][x] = 3
            positions.append((x, y))
        else:  # player selects where to move to
            pieces[moving_y][moving_x] = 0
            positions.append((x, y))
            direction = (x - moving_x, y - moving_y)
            if (x, y) in aw and aw[(x, y)] == "both":
                pieces[y][x] = 3
                remove_pieces(moving_x, moving_y, x, y)
                ask_x = moving_x
                ask_y = moving_y
                moving_x = x
                moving_y = y
                return
            if not paika:
                remove_pieces(moving_x, moving_y, x, y)
            moving_x = x
            moving_y = y
            aw = {}
            if paika_single_check(x, y) or paika:
                is_moving = False
                pieces[y][x] = turn
                switch_turn()
                direction = ()
                positions = []
                mark_all_movables()
                render()
                return
            pieces[y][x] = 3
            reset_movable()
            mark_to_movables(x, y)
        render()
    else:
        if (x, y) not in asking:
            return
        if x - moving_x == 1 or x - moving_x == -1 or y - moving_y == 1 or y - moving_y == -1:
            aw[moving_x, moving_y] = "approach"
        else:
            aw[moving_x, moving_y] = "withdrawal"
        remove_pieces(ask_x, ask_y, moving_x, moving_y)
        aw = {}
        ask_player = False
        asking = []
        if paika_single_check(moving_x, moving_y) or paika:
            is_moving = False
            pieces[moving_y][moving_x] = turn
            switch_turn()
            direction = ()
            positions = []
            mark_all_movables()
            render()
            return
        reset_movable()
        mark_to_movables(moving_x, moving_y)
        render()


# ----------------------------------------------------------------------------------------------------------------------
# INTERFACE:


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