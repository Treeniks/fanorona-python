from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import colorchooser
import copy
import random
import time


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
gamelist = []
ai_moves = []
depth = 2
menu_pos = 0
ask_player = False
ai_game = False
menu_select1 = False
menu_select2 = False
menu_aiselect1 = False
menu_aiselect2 = False
menu_aiselect3 = False
menu_aiselect4 = False
menu_aiselect5 = False
p1color = (None, "white")
p2color = (None, "black")


# ----------------------------------------------------------------------------------------------------------------------
# RENDERING:


# starting render process
def render():
    global width, correct_width, height, correct_height, dw, dh, x, y
    width = correct_width = c.winfo_width()
    height = correct_height = c.winfo_height()

    if (width / height) > 9 / 5:
        correct_width = round(height * (9 / 5))
    else:
        correct_height = round(width * (5 / 9))

    dw = round(correct_width / 9)
    dh = round(correct_height / 5)
    thickness = int(correct_width / 225) + 1

    x = round(width / 2)
    y = round(height / 2)

    c.delete(ALL)
    if menu_pos == 2:
        draw_lines(x, y, correct_width, correct_height, thickness)
        draw_arrows(x, y, correct_width, correct_height, thickness)
        draw_positions(x, y, correct_width, correct_height)
        draw_aimove(x, y, correct_width, correct_height, thickness)
        draw_pieces(x, y, correct_width, correct_height, thickness)
        draw_movable(x, y, correct_width, correct_height, thickness)
        draw_asking(x, y, correct_width, correct_height, thickness)
        # c.update()
    elif menu_pos == 0:
        draw_menu(x, y, correct_width, correct_height, thickness)
    elif menu_pos == 1:
        draw_menu_ai(x, y, correct_width, correct_height, thickness)


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
                              y + dh * (i - 2) + h * (25 / 500),
                              fill=p2color[1], width=thickness)
            elif pieces[i][j] == 2:
                c.create_oval(x + dw * (j - 4) - w * (25 / 900),
                              y + dh * (i - 2) - h * (25 / 500),
                              x + dw * (j - 4) + w * (25 / 900),
                              y + dh * (i - 2) + h * (25 / 500),
                              fill=p1color[1], width=thickness)
            elif pieces[i][j] == 3:
                if len(positions) == 1:
                    if turn == 1:
                        c.create_oval(x + dw * (j - 4) - w * (25 / 900),
                                      y + dh * (i - 2) - h * (25 / 500),
                                      x + dw * (j - 4) + w * (25 / 900),
                                      y + dh * (i - 2) + h * (25 / 500),
                                      fill="#292929", activefill="#3D3D3D", outline="#004CFF", width=thickness)
                    else:
                        c.create_oval(x + dw * (j - 4) - w * (25 / 900),
                                      y + dh * (i - 2) - h * (25 / 500),
                                      x + dw * (j - 4) + w * (25 / 900),
                                      y + dh * (i - 2) + h * (25 / 500),
                                      fill="#EBEBEB", activefill="#D6D6D6", outline="blue", width=thickness)
                else:
                    if turn == 1:
                        c.create_oval(x + dw * (j - 4) - w * (25 / 900),
                                      y + dh * (i - 2) - h * (25 / 500),
                                      x + dw * (j - 4) + w * (25 / 900),
                                      y + dh * (i - 2) + h * (25 / 500),
                                      fill="#292929", outline="#004CFF", width=thickness)
                    else:
                        c.create_oval(x + dw * (j - 4) - w * (25 / 900),
                                      y + dh * (i - 2) - h * (25 / 500),
                                      x + dw * (j - 4) + w * (25 / 900),
                                      y + dh * (i - 2) + h * (25 / 500),
                                      fill="#EBEBEB", outline="blue", width=thickness)


def draw_movable(x, y, w, h, thickness):
    for i in range(5):
        for j in range(9):
            if movable[i][j]:
                if pieces[i][j] == 1:
                    c.create_oval(x + dw * (j - 4) - w * (25 / 900),
                                  y + dh * (i - 2) - h * (25 / 500),
                                  x + dw * (j - 4) + w * (25 / 900),
                                  y + dh * (i - 2) + h * (25 / 500),
                                  fill=p2color[1], outline="#004CFF", activefill="#292929", width=thickness)

                elif pieces[i][j] == 2:
                    c.create_oval(x + dw * (j - 4) - w * (25 / 900),
                                  y + dh * (i - 2) - h * (25 / 500),
                                  x + dw * (j - 4) + w * (25 / 900),
                                  y + dh * (i - 2) + h * (25 / 500),
                                  fill=p1color[1], outline="blue", activefill="#EBEBEB", width=thickness)
                else:
                    if turn == 1:
                        c.create_oval(x + dw * (j - 4) - w * (10 / 900),
                                      y + dh * (i - 2) - h * (10 / 500),
                                      x + dw * (j - 4) + w * (10 / 900),
                                      y + dh * (i - 2) + h * (10 / 500),
                                      fill=p2color[1], outline="#004CFF", activefill="#292929", width=thickness - 2)
                    else:
                        c.create_oval(x + dw * (j - 4) - w * (10 / 900),
                                      y + dh * (i - 2) - h * (10 / 500),
                                      x + dw * (j - 4) + w * (10 / 900),
                                      y + dh * (i - 2) + h * (10 / 500),
                                      fill=p1color[1], outline="blue", activefill="#EBEBEB", width=thickness - 2)


def draw_positions(x, y, w, h):
    for i in range(len(positions) - 1):
        c.create_oval(x + dw * (positions[i][0] - 4) - w * (10 / 900),
                      y + dh * (positions[i][1] - 2) - h * (10 / 500),
                      x + dw * (positions[i][0] - 4) + w * (10 / 900),
                      y + dh * (positions[i][1] - 2) + h * (10 / 500),
                      fill="red", width=0)


def draw_arrows(x, y, w, h, thickness):
    for i in range(len(positions) - 1):
        c.create_line(x - (4 - positions[i][0]) * dw,
                      y - (2 - positions[i][1]) * dh,
                      x - (4 - positions[i + 1][0]) * dw,
                      y - (2 - positions[i + 1][1]) * dh,
                      fill="red", width=thickness)
        c.create_line(x - (4 - positions[i][0]) * dw,
                      y - (2 - positions[i][1]) * dh,
                      ((x - (4 - positions[i + 1][0]) * dw) + (x - (4 - positions[i][0]) * dw)) / 2,
                      ((y - (2 - positions[i + 1][1]) * dh) + (y - (2 - positions[i][1]) * dh)) / 2,
                      fill="red", arrow="last", width=thickness)


def draw_aimove(x, y, w, h, thickness):
    for i in range(len(ai_moves) - 1):
        c.create_oval(x + dw * (ai_moves[i][0] - 4) - w * (10 / 900),
                      y + dh * (ai_moves[i][1] - 2) - h * (10 / 500),
                      x + dw * (ai_moves[i][0] - 4) + w * (10 / 900),
                      y + dh * (ai_moves[i][1] - 2) + h * (10 / 500),
                      fill="red", width=0)

    for i in range(len(ai_moves) - 1):
        c.create_line(x - (4 - ai_moves[i][0]) * dw,
                      y - (2 - ai_moves[i][1]) * dh,
                      x - (4 - ai_moves[i + 1][0]) * dw,
                      y - (2 - ai_moves[i + 1][1]) * dh,
                      fill="red", width=thickness)
        c.create_line(x - (4 - ai_moves[i][0]) * dw,
                      y - (2 - ai_moves[i][1]) * dh,
                      ((x - (4 - ai_moves[i + 1][0]) * dw) + (x - (4 - ai_moves[i][0]) * dw)) / 2,
                      ((y - (2 - ai_moves[i + 1][1]) * dh) + (y - (2 - ai_moves[i][1]) * dh)) / 2,
                      fill="red", arrow="last", width=thickness)


def draw_asking(x, y, w, h, thickness):
    for i in asking:
        if pieces[i[1]][i[0]] == 1:
            c.create_oval(x + dw * (i[0] - 4) - w * (25 / 900),
                          y + dh * (i[1] - 2) - h * (25 / 500),
                          x + dw * (i[0] - 4) + w * (25 / 900),
                          y + dh * (i[1] - 2) + h * (25 / 500),
                          fill="black", outline="red", activefill="#292929", width=thickness)
        else:
            c.create_oval(x + dw * (i[0] - 4) - w * (25 / 900),
                          y + dh * (i[1] - 2) - h * (25 / 500),
                          x + dw * (i[0] - 4) + w * (25 / 900),
                          y + dh * (i[1] - 2) + h * (25 / 500),
                          fill="white", outline="red", activefill="#EBEBEB", width=thickness)


def draw_menu(x, y, w, h, thickness):
    fontsize = round(w / 20)
    color1 = "white"
    color2 = "white"
    if menu_select1:
        color1 = "grey"
    if menu_select2:
        color2 = "grey"
    c.create_rectangle(x - 3.5 * dw, y - 0.5 * dh,
                       x - 0.5 * dw, y + 0.5 * dh, fill=color1, width=thickness)
    c.create_rectangle(x + 3.5 * dw, y - 0.5 * dh,
                       x + 0.5 * dw, y + 0.5 * dh, fill=color2, width=thickness)
    c.create_text(x - 2 * dw, y,
                  text="1 Player", font=("Arial", fontsize))
    c.create_text(x + 2 * dw, y,
                  text="2 Player", font=("Arial", fontsize))


def draw_menu_ai(x, y, w, h, thickness):
    fontsize = round(w / 20)
    fontsize2 = round(w / 40)
    color1 = "white"
    color2 = "white"
    color3 = "white"
    color4 = "white"
    color5 = "white"
    if menu_aiselect1:
        color1 = "grey"
    if menu_aiselect2:
        color2 = "grey"
    if menu_aiselect3:
        color3 = "grey"
    if menu_aiselect4:
        color4 = "grey"
    if menu_aiselect5:
        color5 = "grey"
    c.create_rectangle(x - 2 * dw, y - 2 * dh,
                       x + 2 * dw, y - 1.25 * dh, fill=color1, width=thickness)
    c.create_rectangle(x - 2 * dw, y - 1 * dh,
                       x + 2 * dw, y - 0.25 * dh, fill=color2, width=thickness)
    c.create_rectangle(x - 2 * dw, y,
                       x + 2 * dw, y + 0.75 * dh, fill=color3, width=thickness)
    c.create_rectangle(x - 2 * dw, y + 1.25 * dh,
                       x + 2 * dw, y + 2 * dh, fill=color4, width=thickness)
    c.create_rectangle(x - 4 * dw, y + 1.25 * dh,
                       x - 2.5 * dw, y + 2 * dh, fill=color5, width=thickness)
    c.create_text(x, y - 1.625 * dh,
                  text="Easy - 1", font=("Arial", fontsize))
    c.create_text(x, y - 0.625 * dh,
                  text="Normal - 2", font=("Arial", fontsize))
    c.create_text(x, y + 0.375 * dh,
                  text="Hard - 3", font=("Arial", fontsize))
    c.create_text(x, y + 1.625 * dh,
                  text="Custom", font=("Arial", fontsize))
    c.create_text(x - 3.25 * dw, y + 1.625 * dh,
                  text="◄ Back", font=("Arial", fontsize2))





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


def reset_movable(movablelist=movable):
    for i in range(5):
        for j in range(9):
            movablelist[i][j] = False


def mark_all_movables(pieceslist=pieces, movablelist=movable):
    global paika
    reset_movable(movablelist)
    for i in range(5):
        for j in range(9):
            if pieceslist[i][j] == turn:
                movablelist[i][j] = check_single_movable(j, i, pieceslist)
    if no_movables():
        paika = True
        for i in range(5):
            for j in range(9):
                if pieceslist[i][j] == turn:
                    movablelist[i][j] = check_single_paika(j, i, pieceslist)
    else:
        paika = False


def mark_to_movables(x, y, directiontuple, pieceslist=pieces, movablelist=movable, positionslist=positions, awdict=aw):
    tempdirection = create_tempdirection(x, y)
    if not paika:
        for i in tempdirection:
            if possible_approach(x, y, i, pieceslist) and (x + i[0], y + i[1]) not in positionslist and not directiontuple == i:
                movablelist[y + i[1]][x + i[0]] = True
                awdict[(x + i[0], y + i[1])] = "approach"
            if possible_withdrawal(x, y, i, pieceslist) and (x + i[0], y + i[1]) not in positionslist and not directiontuple == i:
                movablelist[y + i[1]][x + i[0]] = True
                if (x + i[0], y + i[1]) in awdict:
                    awdict[(x + i[0], y + i[1])] = "both"
                else:
                    awdict[(x + i[0], y + i[1])] = "withdrawal"
    else:
        for i in tempdirection:
            if possible_paika(x, y, i, pieceslist):
                movablelist[y + i[1]][x + i[0]] = True


def check_single_movable(x, y, pieceslist=pieces, notturnvar=0):
    tempdirection = create_tempdirection(x, y)
    if notturnvar == 0:
        notturnvar = notturn
    for i in tempdirection:
        if possible_approach(x, y, i, pieceslist, notturnvar) or possible_withdrawal(x, y, i, pieceslist, notturnvar):
            return True
    return False


def check_single_paika(x, y, pieceslist=pieces):
    tempdirection = create_tempdirection(x, y)
    for i in tempdirection:
        if possible_paika(x, y, i, pieceslist):
            return True
    return False


def possible_approach(x, y, i, pieceslist=pieces, notturnvar=0):
    if notturnvar == 0:
        notturnvar = notturn
    if in_bounce_approach(x, y, i) and pieceslist[y + i[1]][x + i[0]] == 0 and pieceslist[y + i[1] + i[1]][x + i[0] + i[0]] == notturnvar:
        return True


def possible_withdrawal(x, y, i, pieceslist=pieces, notturnvar=0):
    if notturnvar == 0:
        notturnvar = notturn
    if in_bounce_withdrawal(x, y, i) and pieceslist[y + i[1]][x + i[0]] == 0 and pieceslist[y - i[1]][x - i[0]] == notturnvar:
        return True


def possible_paika(x, y, i, pieceslist=pieces):
    if in_bounce_paika(x, y, i) and pieceslist[y + i[1]][x + i[0]] == 0:
        return True


def no_movables(movablelist=movable):
    for i in range(5):
        for j in range(9):
            if movablelist[i][j]:
                return False
    return True


def paika_single_check(x, y, directiontuple, pieceslist=pieces, positionslist=positions, notturnvar=0):
    tempdirection = create_tempdirection(x, y)
    if notturnvar == 0:
        notturnvar = notturn
    for i in tempdirection:
        if (possible_approach(x, y, i, pieceslist, notturnvar) and (x + i[0], y + i[1]) not in positionslist and not directiontuple == i) or (
                possible_withdrawal(x, y, i, pieceslist, notturnvar) and (x + i[0], y + i[1]) not in positionslist and not directiontuple == i):
            return False
    return True


def switch_turn():
    global turn, notturn
    if turn == 1:
        turn = 2
        notturn = 1
    else:
        turn = 1
        notturn = 2


def remove_pieces(x1, y1, x2, y2, pieceslist=pieces, awdict=aw, notturnvar=0):
    global ask_player, asking
    if notturnvar == 0:
        notturnvar = notturn
    for i in range(-1, 2):
        for j in range(-1, 2):
            if x2 - x1 == j and y2 - y1 == i:
                k1 = 0
                k2 = 0
                if awdict[x2, y2] == "both":
                    # if not ai_asking:
                    asking.clear()
                    asking.append((x2 + j, y2 + i))
                    asking.append((x1 - j, y1 - i))
                    ask_player = True
                elif awdict[x2, y2] == "approach":
                    while -1 < x2 + j + k2 < 9 and -1 < y2 + i + k1 < 5 and pieceslist[y2 + i + k1][x2 + j + k2] == notturnvar:
                        pieceslist[y2 + i + k1][x2 + j + k2] = 0
                        k1 += i
                        k2 += j
                elif awdict[x2, y2] == "withdrawal":
                    while -1 < x1 - j - k2 < 9 and -1 < y1 - i - k1 < 5 and pieceslist[y1 - i - k1][x1 - j - k2] == notturnvar:
                        pieceslist[y1 - i - k1][x1 - j - k2] = 0
                        k1 += i
                        k2 += j


def win_check():
    if check_black_win():
        msg = messagebox.askyesno("Black Won!", "Black Won!\nDo you want a rematch?")
        if msg:
            set_pieces()
            return True
    elif check_white_win():
        msg = messagebox.askyesno("White Won!", "White Won!\nDo you want a rematch?")
        if msg:
            set_pieces()
            return True


def check_white_win():
    for i in pieces:
        for j in i:
            if j == 1:
                return False
    return True


def check_black_win():
    for i in pieces:
        for j in i:
            if j == 2:
                return False
    return True


# ----------------------------------------------------------------------------------------------------------------------
# AI


def find_all_movables(pieceslist, movablelist, lvl):
    global paika
    movablelist.clear()
    if lvl % 2 == 0:
        local_turn = turn
        local_notturn = notturn
    else:
        local_turn = notturn
        local_notturn = turn
    for i in range(5):
        for j in range(9):
            if pieceslist[i][j] == local_turn and check_single_movable(j, i, pieceslist, local_notturn):
                movablelist.append((j, i))
    if not movablelist:
        paika = True
        for i in range(5):
            for j in range(9):
                if pieceslist[i][j] == local_turn and check_single_paika(j, i, pieceslist):
                    movablelist.append((j, i))
    else:
        paika = False


def create_to_movables(x, y, pieceslist, moveslist, n, lvl, positionslist=[], directiontuple=()):
    global ai_pieces, ai_moveslist, tree
    local_pieces = copy.deepcopy(pieceslist)
    local_positions = copy.deepcopy(positionslist)
    local_direction = copy.deepcopy(directiontuple)
    local_moves = copy.deepcopy(moveslist)
    if lvl % 2 == 0:
        local_turn = turn
        local_notturn = notturn
    else:
        local_turn = notturn
        local_notturn = turn

    tempdirection = create_tempdirection(x, y)
    for i in tempdirection:

        x2 = x + i[0]
        y2 = y + i[1]

        if possible_approach(x, y, i, pieceslist, local_notturn) and (x2, y2) not in local_positions and not local_direction == i:
            local_pieces[y][x] = 0
            local_pieces[y2][x2] = local_turn

            local_positions.append((x, y))
            local_direction = i
            local_moves.append((x2, y2))

            remove_pieces(x, y, x2, y2, local_pieces, {(x2, y2): "approach"}, local_notturn)

            if not paika_single_check(x2, y2, local_direction, local_pieces, local_positions, local_notturn):
                create_to_movables(x2, y2, local_pieces, local_moves, n, lvl, local_positions, local_direction)
            else:  # END OF SEQUENCE
                ai_pieces.append(local_pieces)
                tree.append([len(ai_pieces) - 1, n, lvl, valuation(local_pieces)])
                ai_moveslist.append(local_moves)
            local_pieces = copy.deepcopy(pieceslist)
            local_positions = copy.deepcopy(positionslist)
            local_direction = copy.deepcopy(directiontuple)
            local_moves = copy.deepcopy(moveslist)

        if possible_withdrawal(x, y, i, pieceslist, local_notturn) and (x2, y2) not in local_positions and not local_direction == i:
            local_pieces[y][x] = 0
            local_pieces[y2][x2] = local_turn

            local_positions.append((x, y))
            local_direction = i
            local_moves.append((x2, y2))

            remove_pieces(x, y, x2, y2, local_pieces, {(x2, y2): "withdrawal"}, local_notturn)

            if not paika_single_check(x2, y2, local_direction, local_pieces, local_positions, local_notturn):
                create_to_movables(x2, y2, local_pieces, local_moves, n, lvl, local_positions, local_direction)
            else:  # END OF SEQUENCE
                ai_pieces.append(local_pieces)
                tree.append([len(ai_pieces) - 1, n, lvl, valuation(local_pieces)])
                ai_moveslist.append(local_moves)
            local_pieces = copy.deepcopy(pieceslist)
            local_positions = copy.deepcopy(positionslist)
            local_direction = copy.deepcopy(directiontuple)
            local_moves = copy.deepcopy(moveslist)


def create_to_paika(x, y, pieceslist, n, lvl):
    global ai_pieces, ai_moveslist, tree
    local_pieces = copy.deepcopy(pieceslist)

    tempdirection = create_tempdirection(x, y)
    for i in tempdirection:
        x2 = x + i[0]
        y2 = y + i[1]

        if possible_paika(x, y, i, local_pieces):
            local_pieces[y][x] = 0
            if lvl % 2 == 0:
                local_pieces[y2][x2] = turn
            else:
                local_pieces[y2][x2] = notturn
            ai_pieces.append(local_pieces)
            tree.append([len(ai_pieces) - 1, n, lvl, valuation(local_pieces)])
            ai_moveslist.append([(x, y), (x2, y2)])
        local_pieces = copy.deepcopy(pieceslist)


def valuation(valpieces):
    score_white = 0
    score_black = 0
    for i in valpieces:
        for j in i:
            if j == 1:
                score_black += 1
            elif j == 2:
                score_white += 1
    score = score_black - score_white
    return score


def ai():
    global pieces, ai_moves, ai_pieces, ai_moveslist, tree
    ai_moves.clear()
    ai_pieces = [copy.deepcopy(pieces)]
    ai_moveslist = []
    ai_movable = []
    tree = []

    temp = 0
    for lvl in range(depth):
        temp2 = temp
        temp = len(ai_pieces)
        for j in range(temp2, temp):
            ai_movable.clear()
            find_all_movables(ai_pieces[j], ai_movable, lvl)

            if not paika:
                for i in ai_movable:
                    create_to_movables(i[0], i[1], ai_pieces[j], [i], j, lvl)
            else:
                for i in ai_movable:
                    create_to_paika(i[0], i[1], ai_pieces[j], j, lvl)
        if len(ai_pieces) < 3:
            break

    '''
    # printing ai_pieces:
    n = 0
    for i in range(len(ai_pieces)):
        for j in range(len(ai_pieces[i])):
            if j % 5 == 0:
                print(n)
                n += 1
                print(ai_pieces[i][j])
            else:
                print(ai_pieces[i][j])
    '''

    score = copy.deepcopy(tree[-1])

    rndm = []
    for i in range(len(tree)):
        k = tree[-i - 1]
        if score[1] == k[1]:
            if k[2] % 2 == 0:
                if turn == 1:
                    if k[3] > score[3]:
                        score = copy.deepcopy(k)
                        if k[2] == 0 and len(rndm) > 0:
                            rndm.clear()
                    elif k[2] == 0 and k[3] == score[3]:
                        if len(rndm) == 0:
                            rndm.append(copy.deepcopy(score))
                        rndm.append(copy.deepcopy(k))

                else:
                    if k[3] < score[3]:
                        score = copy.deepcopy(k)
                        if k[2] == 0 and len(rndm) > 0:
                            rndm.clear()
                    elif k[2] == 0 and k[3] == score[3]:
                        if len(rndm) == 0:
                            rndm.append(copy.deepcopy(score))
                        rndm.append(copy.deepcopy(k))
            else:
                if notturn == 1:
                    if k[3] > score[3]:
                        score = copy.deepcopy(k)
                        if k[2] == 0 and len(rndm) > 0:
                            rndm.clear()
                    elif k[2] == 0 and k[3] == score[3]:
                        if len(rndm) == 0:
                            rndm.append(copy.deepcopy(score))
                        rndm.append(copy.deepcopy(k))

                else:
                    if k[3] < score[3]:
                        score = copy.deepcopy(k)
                        if k[2] == 0 and len(rndm) > 0:
                            rndm.clear()
                    elif k[2] == 0 and k[3] == score[3]:
                        if len(rndm) == 0:
                            rndm.append(copy.deepcopy(score))
                        rndm.append(copy.deepcopy(k))
        else:
            tree[score[1] - 1][3] = score[3]
            score = copy.deepcopy(k)

    if len(rndm) > 0:
        temprndm = random.randrange(len(rndm))
        score = copy.deepcopy(rndm[temprndm])

    for i in range(5):
        for j in range(9):
            pieces[i][j] = ai_pieces[score[0]][i][j]

    for i in ai_moveslist[score[0] - 1]:
        ai_moves.append(i)

    switch_turn()

    gamelist.append([])
    gamelist[-1].append(copy.deepcopy(pieces))
    gamelist[-1].append(turn)
    gamelist[-1].append(notturn)

    listbox.insert(END, "Move #" + str(len(gamelist)))

    mark_all_movables()
    render()
    win_check()


# ----------------------------------------------------------------------------------------------------------------------
# BUTTON COMMANDS:


def undo():
    global turn, notturn, is_moving, pieces, positions, aw, direction, ask_player, asking, gamelist
    if len(positions) > 0:
        return
    if len(gamelist) < 2:
        set_pieces()
    else:
        for i in range(5):
            for j in range(9):
                pieces[i][j] = copy.deepcopy(gamelist[-2][0][i][j])
        turn = gamelist[-2][1]
        notturn = gamelist[-2][2]
        is_moving = False
        positions.clear()
        ai_moves.clear()
        aw.clear()
        direction = ()
        ask_player = False
        asking.clear()
        gamelist.pop(-1)

        mark_all_movables()
        render()
        listbox.delete(len(gamelist), END)

    if ai_game:
        if len(positions) > 0:
            return
        if len(gamelist) < 2:
            set_pieces()
        else:
            for i in range(5):
                for j in range(9):
                    pieces[i][j] = copy.deepcopy(gamelist[-2][0][i][j])
            turn = gamelist[-2][1]
            notturn = gamelist[-2][2]
            is_moving = False
            positions.clear()
            ai_moves.clear()
            aw.clear()
            direction = ()
            ask_player = False
            asking.clear()
            gamelist.pop(-1)

            mark_all_movables()
            render()
            listbox.delete(len(gamelist), END)


def set_pieces():
    global turn, notturn, is_moving, pieces, positions, aw, direction, ask_player, asking, gamelist, menu_pos
    for i in range(2):
        for j in range(9):
            pieces[i][j] = 1
    for i in range(3, 5):
        for j in range(9):
            pieces[i][j] = 2
    pieces[2] = [1, 2, 1, 2, 0, 1, 2, 1, 2]

    '''
    o = [[0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0], [2, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 2, 0, 0, 0]]
    for i in range(5):
        for j in range(9):
            pieces[i][j] = o[i][j]
    '''

    '''
    for i in range(2):
        pieces[4][i] = 2
        pieces[0][i] = 1
    '''

    '''
    pieces[0][0] = 1
    pieces[0][4] = 1
    pieces[0][8] = 1
    pieces[1][5] = 1
    pieces[2][4] = 1
    pieces[4][0] = 2
    pieces[4][1] = 2
    '''

    turn = 2
    notturn = 1
    is_moving = False
    positions.clear()
    ai_moves.clear()
    aw.clear()
    direction = ()
    ask_player = False
    asking.clear()
    gamelist.clear()
    listbox.delete(0, END)
    menu_pos = 2

    mark_all_movables()
    render()


def start_two_player_game():
    global ai_game
    ai_game = False
    set_pieces()


def start_ai_game():
    global depth, ai_game
    if depth == 0:
        messagebox.showinfo(title="Difficulty not set yet", message="Difficulty set to Normal (2)")
        depth = 2
    ai_game = True
    set_pieces()


def reset_pieces():
    for i in range(5):
        for j in range(9):
            pieces[i][j] = 0
            movable[i][j] = 0
    render()


def clear():
    c.delete(ALL)


def listboxselect():
    global turn, notturn, is_moving, pieces, positions, aw, direction, ask_player, asking, gamelist
    k = listbox.curselection()[0]
    for i in range(5):
        for j in range(9):
            pieces[i][j] = copy.deepcopy(gamelist[k][0][i][j])
    turn = gamelist[k][1]
    notturn = gamelist[k][2]
    is_moving = False
    positions.clear()
    ai_moves.clear()
    aw.clear()
    direction = ()
    ask_player = False
    asking.clear()
    for i in range(len(gamelist) - k - 1):
        gamelist.pop(k + 1)

    mark_all_movables()
    render()
    listbox.delete(k + 1, END)


def set_depth_one():
    global depth
    depth = 1


def set_depth_two():
    global depth
    depth = 2


def set_depth_three():
    global depth
    depth = 3


def custom_depth():
    global depth
    cstm = messagebox.askokcancel(title="Warning", message="Setting the calculation depth anything above 4 might result in very long waiting-times!")
    if cstm:
        cstmdpth = simpledialog.askinteger(title="Custom Depth", prompt="Depth:", minvalue=1, maxvalue=10)
        depth = cstmdpth


def canvas_color_pick():
    color = colorchooser.askcolor()
    c.config(bg=color[1])


def canvas_color_reset():
    c.config(bg="SystemButtonFace")


def p1_color_pick():
    global p1color
    p1color = colorchooser.askcolor()
    render()


def p2_color_pick():
    global p2color
    p2color = colorchooser.askcolor()
    render()


def menubar_back():
    global menu_pos
    menu_pos = 0
    listbox.delete(0, END)
    render()


def menubar_ai_game():
    global menu_pos
    menu_pos = 1
    listbox.delete(0, END)
    render()


# ----------------------------------------------------------------------------------------------------------------------
# EVENTS:


def resize(event):
    render()


def click(event):
    global is_moving, moving_x, moving_y, direction, aw, positions, ask_x, ask_y, ask_player, asking, menu_pos
    if menu_pos == 2:
        if (event.x < (width - correct_width) / 2
                or event.x > ((width - correct_width) / 2) + correct_width
                or event.y < (height - correct_height) / 2
                or event.y > ((height - correct_height) / 2) + correct_height):
            return
        xx = int((event.x - (width - correct_width) / 2) / dw)
        yy = int((event.y - (height - correct_height) / 2) / dh)
        if not ask_player:  # if not aw == both
            if pieces[yy][xx] == 3 and len(positions) == 1:  # deselect piece
                pieces[yy][xx] = turn
                mark_all_movables()
                is_moving = False
                direction = ()
                aw.clear()
                positions.clear()
                ai_moves.clear()
                render()
                return
            if not movable[yy][xx]:  # is it even a movable place/piece?
                return
            if not is_moving:  # first selection of a piece to move
                reset_movable()
                mark_to_movables(xx, yy, direction)
                moving_x = xx
                moving_y = yy
                is_moving = True
                pieces[yy][xx] = 3
                positions.append((xx, yy))
                ai_moves.clear()
            else:  # player selects where to move to
                pieces[moving_y][moving_x] = 0
                positions.append((xx, yy))
                direction = (xx - moving_x, yy - moving_y)
                if (xx, yy) in aw and aw[(xx, yy)] == "both":  # will we have to ask the player which piece to remove?
                    pieces[yy][xx] = 3
                    remove_pieces(moving_x, moving_y, xx, yy)
                    ask_x = moving_x
                    ask_y = moving_y
                    moving_x = xx
                    moving_y = yy
                    reset_movable()
                    render()
                    return
                if not paika:  # only remove pieces if it's not a paika
                    remove_pieces(moving_x, moving_y, xx, yy)
                moving_x = xx
                moving_y = yy
                aw.clear()
                if paika_single_check(xx, yy, direction) or paika:  # will the next move be a paika? if so, switch turn
                    pieces[yy][xx] = turn
                    is_moving = False
                    switch_turn()
                    direction = ()
                    positions.clear()
                    ai_moves.clear()
                    mark_all_movables()

                    gamelist.append([])  # create gamelist entry
                    gamelist[-1].append(copy.deepcopy(pieces))
                    gamelist[-1].append(turn)
                    gamelist[-1].append(notturn)

                    listbox.insert(END, "Move #" + str(len(gamelist)))

                    render()
                    c.update()
                    if not win_check():
                        if ai_game:
                            time.sleep(.5)
                            ai()
                    return
                pieces[yy][xx] = 3
                reset_movable()
                mark_to_movables(xx, yy, direction)
            render()
        else:  # if we are asking the player which piece to remove
            if (xx, yy) not in asking:  # if the player clicked somewhere else
                return
            if xx - moving_x == 1 or xx - moving_x == -1 or yy - moving_y == 1 or yy - moving_y == -1:
                aw[moving_x, moving_y] = "approach"
            else:
                aw[moving_x, moving_y] = "withdrawal"
            remove_pieces(ask_x, ask_y, moving_x, moving_y)
            aw.clear()
            ask_player = False
            asking.clear()
            if paika_single_check(moving_x, moving_y, direction) or paika:  # will the next move be a paika? if so, switch turn
                pieces[moving_y][moving_x] = turn
                is_moving = False
                switch_turn()
                direction = ()
                positions.clear()
                ai_moves.clear()
                mark_all_movables()

                gamelist.append([])
                gamelist[-1].append(copy.deepcopy(pieces))
                gamelist[-1].append(turn)
                gamelist[-1].append(notturn)

                listbox.insert(END, "Move #" + str(len(gamelist)))

                render()
                c.update()
                if not win_check():
                    if ai_game:
                        time.sleep(.5)
                        ai()
                return
            reset_movable()
            mark_to_movables(moving_x, moving_y, direction)
    elif menu_pos == 0:
        if x - 3.5 * dw < event.x < x - 0.5 * dw:
            if y - 0.5 * dh < event.y < y + 0.5 * dh:
                menu_pos = 1
                reset_menu_selections()
                highlight_selection(event.x, event.y)
        elif x + 0.5 * dw < event.x < x + 3.5 * dw:
            if y - 0.5 * dh < event.y < y + 0.5 * dh:
                start_two_player_game()
                reset_menu_selections()
    elif menu_pos == 1:
        if x - 2 * dw < event.x < x + 2 * dw:
            if y - 2 * dh < event.y < y - 1.25 * dh:
                set_depth_one()
                start_ai_game()
                reset_menu_selections()
            if y - 1 * dh < event.y < y - 0.25 * dh:
                set_depth_two()
                start_ai_game()
                reset_menu_selections()
            if y < event.y < y + 0.75 * dh:
                set_depth_three()
                start_ai_game()
                reset_menu_selections()
            if y + 1.25 * dh < event.y < y + 2 * dh:
                custom_depth()
                start_ai_game()
                reset_menu_selections()
        if x - 4 * dw < event.x < x - 2.5 * dw:
            if y + 1.25 * dh < event.y < y + 2 * dh:
                menu_pos = 0
                reset_menu_selections()
                highlight_selection(event.x, event.y)
    render()


def motion(event):
    highlight_selection(event.x, event.y)


def highlight_selection(xx, yy):
    global menu_select1, menu_select2, menu_aiselect1, menu_aiselect2, menu_aiselect3, menu_aiselect4, menu_aiselect5
    if menu_pos == 0:
        if x - 3.5 * dw < xx < x - 0.5 * dw:
            if y - 0.5 * dh < yy < y + 0.5 * dh:
                menu_select1 = True
            else:
                menu_select1 = False
        else:
            menu_select1 = False
        if x + 0.5 * dw < xx < x + 3.5 * dw:
            if y - 0.5 * dh < yy < y + 0.5 * dh:
                menu_select2 = True
            else:
                menu_select2 = False
        else:
            menu_select2 = False
    if menu_pos == 1:
        if x - 2 * dw < xx < x + 2 * dw:
            if y - 2 * dh < yy < y - 1.25 * dh:
                menu_aiselect1 = True
            else:
                menu_aiselect1 = False
            if y - 1 * dh < yy < y - 0.25 * dh:
                menu_aiselect2 = True
            else:
                menu_aiselect2 = False
            if y < yy < y + 0.75 * dh:
                menu_aiselect3 = True
            else:
                menu_aiselect3 = False
            if y + 1.25 * dh < yy < y + 2 * dh:
                menu_aiselect4 = True
            else:
                menu_aiselect4 = False
        else:
            menu_aiselect1 = False
            menu_aiselect2 = False
            menu_aiselect3 = False
            menu_aiselect4 = False
        if x - 4 * dw < xx < x - 2.5 * dw:
            if y + 1.25 * dh < yy < y + 2 * dh:
                menu_aiselect5 = True
            else:
                menu_aiselect5 = False
        else:
            menu_aiselect5 = False
    render()


def reset_menu_selections():
    global menu_select1, menu_select2, menu_aiselect1, menu_aiselect2, menu_aiselect3, menu_aiselect4, menu_aiselect5
    menu_select1 = False
    menu_select2 = False
    menu_aiselect1 = False
    menu_aiselect2 = False
    menu_aiselect3 = False
    menu_aiselect4 = False
    menu_aiselect5 = False


# ----------------------------------------------------------------------------------------------------------------------
# INTERFACE:


root = Tk()
root.title("Fanorona")
root.minsize(width=600, height=250)

# configuring grid information
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

menubar = Menu(root)

match_menu = Menu(menubar, tearoff=0)

match_menu.add_command(label="Back to Main Menu", command=menubar_back)
match_menu.add_command(label="Start 2 Player Game", command=start_two_player_game)
match_menu.add_command(label="Start AI Game", command=menubar_ai_game)

menubar.add_cascade(menu=match_menu, label="Match")

ai_menu = Menu(menubar, tearoff=0)
depth_menu = Menu(ai_menu, tearoff=0)

depth_menu.add_command(label="Easy (1)", command=set_depth_one)
depth_menu.add_command(label="Normal (2)", command=set_depth_two)
depth_menu.add_command(label="Hard (3)", command=set_depth_three)
depth_menu.add_command(label="Custom", command=custom_depth)

ai_menu.add_cascade(menu=depth_menu, label="Difficulty")
menubar.add_cascade(menu=ai_menu, label="AI Settings")

view_menu = Menu(menubar, tearoff=0)
view_menu.add_command(label="Canvas Color", command=canvas_color_pick)
view_menu.add_command(label="Reset Canvas Color", command=canvas_color_reset)
# view_menu.add_command(label="Player 1 Color", command=p1_color_pick)
# view_menu.add_command(label="Player 2 Color", command=p2_color_pick)

menubar.add_cascade(menu=view_menu, label="View")

root.config(menu=menubar)

# column 0: listbox
listbox = Listbox(root)
selectlistbox = Button(root, text="Select", command=listboxselect)

listbox.grid(row=0, column=0, sticky=N+S)
selectlistbox.grid(row=1, column=0, sticky=W+E)

''' OLD MENU:
# column 1: menu
menu = Frame(root)
test = Button(menu, text="AI", command=ai)
undo = Button(menu, text="Undo", command=undo)
clear = Button(menu, text="Clear Everything", command=clear)
place = Button(menu, text="Start Game - 2 Player", command=start_two_player_game)
placeai = Button(menu, text="Start Game - VS CPU", command=start_ai_game)
reset = Button(menu, text="Reset Pieces", command=reset_pieces)

menu.grid(row=0, column=1, rowspan=2, padx=10)
test.pack(fill=X)
undo.pack(fill=X)
clear.pack(fill=X)
place.pack(fill=X)
placeai.pack(fill=X)
reset.pack(fill=X)
'''

# Columns 2: Canvas
c = Canvas(root, width=900, height=500)
c.grid(row=0, column=2, rowspan=2, sticky=N+S+W+E)

# binds
c.bind("<Configure>", resize)
c.bind("<Button-1>", click)
c.bind("<Motion>", motion)

root.mainloop()