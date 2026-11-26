# Mend proof (found by Stone 49), boot 2: the
# control. Every step of mend49-boot1.py stands
# here the same — the same prepared disk, the same
# picture painted the same way through the same
# carried presses with the paint window forward,
# the same picking of the picture in the files
# window with the paint window open behind — and
# then this boot simply ends: the exchange press
# is never made. prove-mend49.sh reads this disk's
# picture sectors and the press boot's, and the
# two must stand byte for byte the same: whatever
# the press changed would stand between them, and
# under the mended road nothing may.

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


# The files window's place, as in boot 1.
GX, GY = 5, 30


# The machine is first let rise unwatched, as in
# boot 1: on this bench, under load, the harness's
# own watching can starve the rise it waits for.
# The settle changes no check.
time.sleep(20)
d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 300)
expect(d is not None, "the desktop is drawn")

# The same painting as boot 1, through the same
# carried presses with the paint window forward.
typewrite("paint")
enter()
RX, RY = cell_center(11, 16)
d = waitdump(lambda d: d is not None and pixel(d, RX, RY) == RED, 25)
expect(d is not None, "the paint window stands with the feather's swatches painted")
click(*cell_center(16, 30))
park()
d = waitdump(lambda d: d is not None
             and cell_pixel(d, 16, 30) == RED, 15)
expect(d is not None, "a press on the canvas paints its cell Red, the paint window forward")
click(*cell_center(11, 34))
park()
time.sleep(0.6)
click(*cell_center(15, 20))
park()
d = waitdump(lambda d: d is not None
             and cell_pixel(d, 15, 20) == DBLUE, 15)
expect(d is not None, "a press on the canvas now paints Blue, the paint window forward")

# The same picking as boot 1: the picture's row,
# then the files window raised forward again, the
# paint window open and visited behind.
typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, "Notes kept on the disk:", GRAY)
             == "Notes kept on the disk:", 25)
expect(d is not None, "the word 'files' opened the files window on the disk's keeping")
click((GX + 6) * 16 + 8, (GY + 13) * 16 + 8)
park()
typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 11, GX + 2, "The picture you picked:", GRAY)
             == "The picture you picked:", 15)
expect(d is not None, "a press on the picture's row picked the kept picture")

# And here the control boot ends: no exchange
# press. The disk's picture keeping now stands as
# the painting alone left it, for the comparison
# prove-mend49.sh makes.
done()
