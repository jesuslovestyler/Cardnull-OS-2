# Stone 48 proof, boot 1: the picture window opens
# from the files window, on a real kept picture. A
# fitted keeping disk stands ready (its settings card
# and one known note laid by prove-stone48.sh). The
# word 'paint' opens the paint feather and the bench's
# mouse draws a Red cell and a Blue cell, exactly as
# Stone 26's proof draws them, so a picture stands
# kept on the disk. The word 'files' lists it; the
# down arrow picks it, and the window's foot carries
# the new word "Look at it" beside "Rename", with the
# foot's line naming both doors. A press on "Look at
# it" opens the picture window forward — its title
# decoded — and the kept picture stands in it in its
# big measure: the Red cell's block and the Blue
# cell's block at the places the window's own
# reckoning gives them (each canvas cell sixteen
# pixels wide and thirty-two tall, one cell in from
# the window's left edge, under its title bar), and
# an untouched cell standing on the canvas ground. A
# press on the window's close mark closes it.

import re

BLUE = (0, 0, 170)
RED = (170, 0, 0)
DBLUE = (0, 0, 170)
GRAY = (170, 170, 170)
WHITE = (255, 255, 255)

_vals = {}
for _m in re.finditer(r"block\[(\d+)\] = (\d+)",
                      open("src/font.nifla").read()):
    _vals[int(_m.group(1))] = int(_m.group(2))
GLYPHS = {}
for _code in range(32, 127):
    GLYPHS[_code] = tuple(_vals.get((_code - 32) * 8 + _r, 0)
                          for _r in range(8))


def cell_bitmap(d, cx, cy, ink):
    rows = []
    for r in range(8):
        v = 0
        for c in range(8):
            if pixel(d, cx + 2 * c + 1, cy + 2 * r + 1) == ink:
                v |= 1 << (7 - c)
        rows.append(v)
    return tuple(rows)


def decode(d, prow, pcol, text, ink):
    out = []
    for i in range(len(text)):
        bm = cell_bitmap(d, (pcol + i) * 16, prow * 16, ink)
        if all(v == 0 for v in bm):
            out.append(" ")
            continue
        best, bestd = None, 999
        for code, g in GLYPHS.items():
            dist = sum(bin(a ^ b).count("1") for a, b in zip(bm, g))
            if dist < bestd:
                bestd, best = dist, code
        out.append(chr(best) if bestd <= 2 else "?")
    return "".join(out)


CUR = [506, 378]


def move_to(x, y):
    while CUR[0] != x or CUR[1] != y:
        dx = max(-61, min(61, x - CUR[0]))
        dy = max(-61, min(61, y - CUR[1]))
        mousemove(dx, dy)
        CUR[0] += dx
        CUR[1] += dy


def click(x, y):
    move_to(x, y)
    mousebutton(1)
    time.sleep(0.4)
    mousebutton(0)
    time.sleep(0.4)


def park():
    move_to(60, 60)


def cell_center(row, col):
    """The screen pixel at the center of the paint
    feather cell (row, col), as the paint window
    carries it 1:1 (Stone 24's reckoning)."""
    return ((col - 8) * 16 + 8, (row + 24) * 16 + 8)


def cell_pixel(d, row, col):
    x, y = cell_center(row, col)
    return pixel(d, x, y)


# The files window's place (Stone 19): left cell 5,
# top row 29 (row 31 through Stone 48; the window
# grew by Stone 49's exchange row and by Stone 50's
# Cardinal door row, its top standing one row higher
# for each); the kept picture's entry stands
# on GY + 13, and its foot on GY + 11.
GX, GY = 5, 29
NOTE = "remember the garden"

# The picture window's place: fifty cells wide,
# centered — left cell 7 — and sixteen high, its top
# laid at the layout's row 17 and clamped whole above
# the bar, to row 30. Its drawing stands one cell in
# from its left edge and under its title bar: canvas
# cell (row, col) of the feather's canvas stands at
# block column col - 16, block row row - 14, each
# block sixteen pixels wide and thirty-two tall.
PX, PY = 7, 30


def pic_block_center(row, col):
    x = PX * 16 + 16 + (col - 16) * 16 + 8
    y = PY * 16 + 16 + (row - 14) * 32 + 16
    return (x, y)


d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

# The word 'paint' asks for the paint feather, and
# the drawing is Stone 26's own: a Red cell at
# (16, 30), the Blue swatch, a Blue cell at (15, 20).
typewrite("paint")
enter()
RX, RY = cell_center(11, 16)
d = waitdump(lambda d: d is not None and pixel(d, RX, RY) == RED, 25)
expect(d is not None, "the paint window stands with the feather's swatches painted")
click(*cell_center(16, 30))
park()
d = waitdump(lambda d: d is not None
             and cell_pixel(d, 16, 30) == RED, 15)
expect(d is not None, "a press on the canvas paints its cell Red")
click(*cell_center(11, 34))
park()
time.sleep(0.6)
click(*cell_center(15, 20))
park()
d = waitdump(lambda d: d is not None
             and cell_pixel(d, 15, 20) == DBLUE, 15)
expect(d is not None, "a press on the canvas now paints Blue")

# The files window lists the kept picture beside the
# known note; the down arrow picks the picture, and
# the foot names the new door.
typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, "Notes kept on the disk:", GRAY)
             == "Notes kept on the disk:", 25)
expect(d is not None, "the word 'files' opened the files window on the disk's keeping")
if d:
    said = decode(d, GY + 13, GX + 4, "A picture you painted", GRAY)
    expect(said == "A picture you painted",
           f"the kept picture stands listed beside the notes (read: {said!r})")
sendkey("down")
d = waitdump(lambda d: d is not None
             and decode(d, GY + 11, GX + 2, "The picture you picked:", GRAY)
             == "The picture you picked:", 15)
expect(d is not None, "the down arrow picked the kept picture")
if d:
    said = decode(d, GY + 13, GX + 4, "A picture you painted", WHITE)
    expect(said == "A picture you painted",
           f"the picked picture's entry stands white on blue (read: {said!r})")
    said = decode(d, GY + 11, GX + 26, "Look at it", WHITE)
    expect(said == "Look at it",
           f"'Look at it' stands at the window's foot (read: {said!r})")
    said = decode(d, GY + 11, GX + 36, "Rename", WHITE)
    expect(said == "Rename",
           f"'Rename' still stands at the foot, right of it (read: {said!r})")
    said = decode(d, GY + 12, GX + 2,
                  "Enter opens it in Paint. Look at it sees it big.", WHITE)
    expect(said == "Enter opens it in Paint. Look at it sees it big.",
           f"the foot's line names both doors (read: {said!r})")

# A press on "Look at it" opens the picture window,
# forward, with the kept picture standing big in it.
# The press is given the stone-47 bench discipline:
# the machine is let settle first, and the press is
# tried up to three times — a press packet dropped
# while a repaint is still running is the bench's
# known frailty, not the window's.
time.sleep(2)
d = None
for _try in range(3):
    click(36 * 16, (GY + 11) * 16 + 8)
    park()
    d = waitdump(lambda d: d is not None
                 and decode(d, PY, PX + 1, "Picture", WHITE) == "Picture", 12)
    if d is not None:
        break
expect(d is not None, "a press on 'Look at it' opened the picture window")
if d:
    x, y = pic_block_center(16, 30)
    expect(pixel(d, x, y) == RED,
           "the Red cell stands in the picture window, in its big block")
    expect(pixel(d, x - 7, y - 15) == RED,
           "the Red cell's block stands whole, to its corner")
    x, y = pic_block_center(15, 20)
    expect(pixel(d, x, y) == DBLUE,
           "the Blue cell stands in the picture window, in its big block")
    x, y = pic_block_center(18, 40)
    expect(pixel(d, x, y) == GRAY,
           "an untouched cell stands on the canvas ground in the picture window")

# A press on its close mark closes it: the mark's
# cell is the window's fifty-second-from-last — left
# 7, fifty wide, so the mark's cell is 55.
click((PX + 50 - 2) * 16 + 8, PY * 16 + 8)
park()
d = waitdump(lambda d: d is not None
             and decode(d, PY, PX + 1, "Picture", WHITE) != "Picture", 15)
expect(d is not None, "a press on the picture window's close mark closed it")

done()
