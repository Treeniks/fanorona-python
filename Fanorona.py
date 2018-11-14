from tkinter import *
from tkinter import messagebox
import copy
import random


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
gamelist = []
ai_moves = []


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
    thickness = int(correct_width / 225) + 1

    x = round(width / 2)
    y = round(height / 2)

    c.delete(ALL)
    draw_lines(x, y, correct_width, correct_height, thickness)
    draw_arrows(x, y, correct_width, correct_height, thickness)
    draw_positions(x, y, correct_width, correct_height)
    draw_aimove(x, y, correct_width, correct_height, thickness)
    draw_pieces(x, y, correct_width, correct_height, thickness)
    draw_movable(x, y, correct_width, correct_height, thickness)
    draw_asking(x, y, correct_width, correct_height, thickness)


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
                              fill="black", width=thickness)
            elif pieces[i][j] == 2:
                c.create_oval(x + dw * (j - 4) - w * (25 / 900),
                              y + dh * (i - 2) - h * (25 / 500),
                              x + dw * (j - 4) + w * (25 / 900),
                              y + dh * (i - 2) + h * (25 / 500),
                              fill="white", width=thickness)
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
                                  fill="black", outline="#004CFF", activefill="#292929", width=thickness)

                elif pieces[i][j] == 2:
                    c.create_oval(x + dw * (j - 4) - w * (25 / 900),
                                  y + dh * (i - 2) - h * (25 / 500),
                                  x + dw * (j - 4) + w * (25 / 900),
                                  y + dh * (i - 2) + h * (25 / 500),
                                  fill="white", outline="blue", activefill="#EBEBEB", width=thickness)
                else:
                    if turn == 1:
                        c.create_oval(x + dw * (j - 4) - w * (10 / 900),
                                      y + dh * (i - 2) - h * (10 / 500),
                                      x + dw * (j - 4) + w * (10 / 900),
                                      y + dh * (i - 2) + h * (10 / 500),
                                      fill="black", outline="#004CFF", activefill="#292929", width=thickness - 2)
                    else:
                        c.create_oval(x + dw * (j - 4) - w * (10 / 900),
                                      y + dh * (i - 2) - h * (10 / 500),
                                      x + dw * (j - 4) + w * (10 / 900),
                                      y + dh * (i - 2) + h * (10 / 500),
                                      fill="white", outline="blue", activefill="#EBEBEB", width=thickness - 2)


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


def check_single_movable(x, y, pieceslist=pieces):
    tempdirection = create_tempdirection(x, y)
    for i in tempdirection:
        if possible_approach(x, y, i, pieceslist) or possible_withdrawal(x, y, i, pieceslist):
            return True
    return False


def check_single_paika(x, y, pieceslist=pieces):
    tempdirection = create_tempdirection(x, y)
    for i in tempdirection:
        if possible_paika(x, y, i, pieceslist):
            return True
    return False


def possible_approach(x, y, i, pieceslist=pieces):
    if in_bounce_approach(x, y, i) and pieceslist[y + i[1]][x + i[0]] == 0 and pieceslist[y + i[1] + i[1]][x + i[0] + i[0]] == notturn:
        return True


def possible_withdrawal(x, y, i, pieceslist=pieces):
    if in_bounce_withdrawal(x, y, i) and pieceslist[y + i[1]][x + i[0]] == 0 and pieceslist[y - i[1]][x - i[0]] == notturn:
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


def paika_single_check(x, y, directiontuple, pieceslist=pieces, positionslist=positions):
    tempdirection = create_tempdirection(x, y)
    for i in tempdirection:
        if (possible_approach(x, y, i, pieceslist) and (x + i[0], y + i[1]) not in positionslist and not directiontuple == i) or (
                possible_withdrawal(x, y, i, pieceslist) and (x + i[0], y + i[1]) not in positionslist and not directiontuple == i):
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


def remove_pieces(x1, y1, x2, y2, pieceslist=pieces, awdict=aw):
    global ask_player, asking
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
                    while -1 < x2 + j + k2 < 9 and -1 < y2 + i + k1 < 5 and pieceslist[y2 + i + k1][x2 + j + k2] == notturn:
                        pieceslist[y2 + i + k1][x2 + j + k2] = 0
                        k1 += i
                        k2 += j
                elif awdict[x2, y2] == "withdrawal":
                    while -1 < x1 - j - k2 < 9 and -1 < y1 - i - k1 < 5 and pieceslist[y1 - i - k1][x1 - j - k2] == notturn:
                        pieceslist[y1 - i - k1][x1 - j - k2] = 0
                        k1 += i
                        k2 += j


def win_check():
    if check_black_win():
        msg = messagebox.askyesno("Black Won!", "Black Won!\nDo you want a rematch?")
        if msg:
            set_pieces()
    elif check_white_win():
        msg = messagebox.askyesno("White Won!", "White Won!\nDo you want a rematch?")
        if msg:
            set_pieces()


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


def find_all_movables(pieceslist, movablelist):
    global paika
    movablelist.clear()
    for i in range(5):
        for j in range(9):
            if pieceslist[i][j] == turn and check_single_movable(j, i, pieceslist):
                movablelist.append((j, i))
    if not movablelist:
        paika = True
        for i in range(5):
            for j in range(9):
                if pieceslist[i][j] == turn and check_single_paika(j, i, pieceslist):
                    movablelist.append((j, i))
    else:
        paika = False


def create_to_movables(x, y, pieceslist, moveslist, n, lvl, positionslist=[], directiontuple=()):
    global ai_pieces, ai_moveslist, tree
    local_pieces = copy.deepcopy(pieceslist)
    local_positions = copy.deepcopy(positionslist)
    local_direction = copy.deepcopy(directiontuple)
    local_moves = copy.deepcopy(moveslist)

    tempdirection = create_tempdirection(x, y)
    for i in tempdirection:

        x2 = x + i[0]
        y2 = y + i[1]

        if possible_approach(x, y, i, pieceslist) and (x2, y2) not in local_positions and not local_direction == i:
            local_pieces[y][x] = 0
            local_pieces[y2][x2] = turn

            local_positions.append((x, y))
            local_direction = i
            local_moves.append((x2, y2))

            remove_pieces(x, y, x2, y2, local_pieces, {(x2, y2): "approach"})

            if not paika_single_check(x2, y2, local_direction, local_pieces, local_positions):
                create_to_movables(x2, y2, local_pieces, local_moves, n, lvl, local_positions, local_direction)
            else:  # END OF SEQUENCE
                ai_pieces.append(local_pieces)
                tree.append([len(ai_pieces) - 1, n, lvl, valuation(local_pieces)])
                ai_moveslist.append(local_moves)
            local_pieces = copy.deepcopy(pieceslist)
            local_positions = copy.deepcopy(positionslist)
            local_direction = copy.deepcopy(directiontuple)
            local_moves = copy.deepcopy(moveslist)

        if possible_withdrawal(x, y, i, pieceslist) and (x2, y2) not in local_positions and not local_direction == i:
            local_pieces[y][x] = 0
            local_pieces[y2][x2] = turn

            local_positions.append((x, y))
            local_direction = i
            local_moves.append((x2, y2))

            remove_pieces(x, y, x2, y2, local_pieces, {(x2, y2): "withdrawal"})

            if not paika_single_check(x2, y2, local_direction, local_pieces, local_positions):
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
            local_pieces[y2][x2] = turn
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
    ai_pieces = []
    ai_pieces.append(copy.deepcopy(pieces))
    ai_moveslist = []
    ai_movable = []
    tree = []
    depth = 3
    temp = 0

    for lvl in range(depth):
        temp2 = temp
        temp = len(ai_pieces)
        for j in range(temp2, temp):
            ai_movable.clear()
            find_all_movables(ai_pieces[j], ai_movable)

            if not paika:
                for i in ai_movable:
                    create_to_movables(i[0], i[1], ai_pieces[j], [i], j, lvl)
            else:
                for i in ai_movable:
                    create_to_paika(i[0], i[1], ai_pieces[j], j, lvl)
        switch_turn()
    switch_turn()

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

    for i in range(len(tree)):
        k = tree[-i - 1]
        if score[1] == k[1]:
            if turn == 1:
                if k[3] > score[3]:
                    score = copy.deepcopy(k)
                elif k[3] == score[3]:
                    rndm = random.randrange(2)
                    if rndm == 0:
                        score = copy.deepcopy(k)
            else:
                if k[3] < score[3]:
                    score = copy.deepcopy(k)
                elif k[3] == score[3]:
                    rndm = random.randrange(2)
                    if rndm == 0:
                        score = copy.deepcopy(k)
        else:
            if not score[2] == k[2]:
                switch_turn()
            tree[score[1] - 1][3] = score[3]
            score = k

    print(tree)

    for i in range(5):
        for j in range(9):
            pieces[i][j] = ai_pieces[score[0]][i][j]

    for i in ai_moveslist[score[0] - 1]:
        ai_moves.append(i)

    switch_turn()

    gamelist.append([])
    gamelist[-1].append([])
    gamelist[-1][0] = copy.deepcopy(pieces)
    gamelist[-1].append(turn)
    gamelist[-1].append(notturn)

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
                pieces[i][j] = gamelist[-2][0][i][j]
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
    global turn, notturn, is_moving, pieces, positions, aw, direction, ask_player, asking, gamelist
    for i in range(2):
        for j in range(9):
            pieces[i][j] = 1
    for i in range(3, 5):
        for j in range(9):
            pieces[i][j] = 2
    pieces[2] = [1, 2, 1, 2, 0, 1, 2, 1, 2]

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


def listboxselect():
    global turn, notturn, is_moving, pieces, positions, aw, direction, ask_player, asking, gamelist
    k = listbox.curselection()[0]
    for i in range(5):
        for j in range(9):
            pieces[i][j] = gamelist[k][0][i][j]
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
    if not ask_player:  # if not aw == both
        if pieces[y][x] == 3 and len(positions) == 1:  # deselect piece
            pieces[y][x] = turn
            mark_all_movables()
            is_moving = False
            direction = ()
            aw.clear()
            positions.clear()
            ai_moves.clear()
            render()
            return
        if not movable[y][x]:  # is it even a movable place/piece?
            return
        if not is_moving:  # first selection of a piece to move
            reset_movable()
            mark_to_movables(x, y, direction)
            moving_x = x
            moving_y = y
            is_moving = True
            pieces[y][x] = 3
            positions.append((x, y))
            ai_moves.clear()
        else:  # player selects where to move to
            pieces[moving_y][moving_x] = 0
            positions.append((x, y))
            direction = (x - moving_x, y - moving_y)
            if (x, y) in aw and aw[(x, y)] == "both":  # will we have to ask the player which piece to remove?
                pieces[y][x] = 3
                remove_pieces(moving_x, moving_y, x, y)
                ask_x = moving_x
                ask_y = moving_y
                moving_x = x
                moving_y = y
                reset_movable()
                render()
                return
            if not paika:  # only remove pieces if it's not a paika
                remove_pieces(moving_x, moving_y, x, y)
            moving_x = x
            moving_y = y
            aw.clear()
            if paika_single_check(x, y, direction) or paika:  # will the next move be a paika? if so, switch turn
                pieces[y][x] = turn
                is_moving = False
                switch_turn()
                direction = ()
                positions.clear()
                ai_moves.clear()
                mark_all_movables()

                gamelist.append([])  # create gamelist entry
                gamelist[-1].append([])
                gamelist[-1][0] = copy.deepcopy(pieces)
                gamelist[-1].append(turn)
                gamelist[-1].append(notturn)

                listbox.insert(END, "Move #" + str(len(gamelist)))

                render()
                win_check()
                return
            pieces[y][x] = 3
            reset_movable()
            mark_to_movables(x, y, direction)
        render()
    else:  # if we are asking the player which piece to remove
        if (x, y) not in asking:  # if the player clicked somewhere else
            return
        if x - moving_x == 1 or x - moving_x == -1 or y - moving_y == 1 or y - moving_y == -1:
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
            gamelist[-1].append([])
            gamelist[-1][0] = copy.deepcopy(pieces)
            gamelist[-1].append(turn)
            gamelist[-1].append(notturn)

            listbox.insert(END, "Move #" + str(len(gamelist)))

            render()
            win_check()
            return
        reset_movable()
        mark_to_movables(moving_x, moving_y, direction)
        render()


# ----------------------------------------------------------------------------------------------------------------------
# INTERFACE:


root = Tk()
root.title("Fanorona")
root.minsize(width=600, height=250)

# TODO add menubar

# configuring grid information
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

# column 0: listbox
listbox = Listbox(root)
selectlistbox = Button(root, text="select", command=listboxselect)

listbox.grid(row=0, column=0, sticky=N+S)
selectlistbox.grid(row=1, column=0, sticky=W+E)

# column 1: menu
menu = Frame(root)
test = Button(menu, text="AI", command=ai)
undo = Button(menu, text="Undo", command=undo)
clear = Button(menu, text="Clear Everything", command=clear)
place = Button(menu, text="Start Game", command=set_pieces)
reset = Button(menu, text="Reset Pieces", command=reset_pieces)

menu.grid(row=0, column=1, rowspan=2)
test.pack()
undo.pack()
clear.pack()
place.pack()
reset.pack()

# Columns 2: Canvas
c = Canvas(root, width=900, height=500)
c.grid(row=0, column=2, rowspan=2, sticky=N+S+W+E)

# binds
c.bind("<Configure>", resize)
c.bind("<Button-1>", click)

root.mainloop()