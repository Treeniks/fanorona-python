from tkinter import *

def draw_lines(w, h, x, y):
    x -= w
    y -= h
    for i in range(9):
        c.create_line(x/2 + i * (w / 9) + (w / 18), y/2 + h / 10, x/2 + i * (w / 9) + (w / 18), y/2 + h - (h / 10), width=2)

    for i in range(5):
        c.create_line(x/2 + w / 18, y/2 + i * (h / 5) + (h / 10), x/2 + w - (w / 18), y/2 + i * (h / 5) + (h / 10), width=2)

def render(event):
    x = c.winfo_width()
    y = c.winfo_height()
    width, height = x, y
    if x/y > (9/5):
        width = y*(9/5)
    else:
        height = x*(5/9)

    c.delete(ALL)
    draw_lines(width, height, x, y)


width=900
height=500

root = Tk()
c = Canvas(root, width=width, height=height)
c.pack(fill=BOTH, expand=1)
c.bind('<Configure>', render)

root.mainloop()
