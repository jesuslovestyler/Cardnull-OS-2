# Mend proof (found by Stone 49), boot 1: the press.
# A fitted keeping disk stands ready (its Eastern
# card and two notes, laid by prove-mend49.sh) and
# NO stick stands on the bus. A picture is painted
# and kept the bench's way (Stone 26's drawing: a
# Red cell and a Blue cell) — those presses travel
# the carried-press road with the paint window
# standing forward, and they must paint, as they
# always have. The files window then picks the kept
# picture by its row — which opens the picture in
# the paint window behind, Stone 26's way — and the
# word 'files' raises the files window forward
# again, the picture standing picked in it. The
# paint window now stands open, and a visit has
# stood in it, and another window stands forward:
# the very standing in which the unmended road
# carried the files window's presses into the
# canvas. A press on "To the stick" follows — the
# exchange press of Stone 49's first boot, at the
# same point of the screen, inside the paint
# window's shown region. The files window must
# answer it itself, in plain words ("No stick
# stands in this computer."), and the disk's
# picture keeping must stand exactly as the
# painting left it: prove-mend49.sh reads the
# disk's picture sectors after this boot and after
# its control (mend49-boot2.py — every step the
# same, the exchange press never made) and compares
# them byte for byte.

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


# The files window's place (Stone 19; its top one
# row higher since Stone 49 grew it by the exchange
# row): left cell 5, top row 30. The picture's
# entry stands on GY + 13 and the exchange's row on
# GY + 14 — "To the stick" at GX + 2, and the
# exchange's spoken word at GX + 2 on the same row.
GX, GY = 5, 30


def press_exchange(col):
    """A press on an exchange word at the files
    window's last row, at the given column — given
    the stone-47 bench discipline: the machine is
    let settle first, and the press is tried up to
    three times, the caller reading the window's
    answer after."""
    time.sleep(2)
    for _try in range(3):
        click(col * 16 + 8, (GY + 14) * 16 + 8)
        park()
        yield


def row_has(text):
    return lambda d: d is not None and \
        decode(d, GY + 14, GX + 2, text, WHITE) == text


# The machine is first let rise unwatched: on this
# bench, under load, the harness's own watching
# (a screendump and a full-frame count every poll)
# can starve the very rise it waits for — rises
# that take seconds unwatched have timed out at
# 300s watched from the first second. The settle
# changes no check: the desktop must still stand
# drawn before anything else is believed.
time.sleep(20)
d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 300)
expect(d is not None, "the desktop is drawn")

# A picture is painted and kept, Stone 26's
# drawing: a Red cell at (16, 30), the Blue swatch,
# a Blue cell at (15, 20). These presses travel
# the carried-press road with the paint window
# standing forward — the road's true work, which
# the mend must not hinder.
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

# The files window picks the kept picture, by a
# press on the picture's row — which also opens
# the picture in the paint window, Stone 26's
# way — and the word 'files' raises the files
# window again, the picture standing picked in
# it. The paint window stands open and visited,
# behind.
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

# The mend's press: on "To the stick", inside the
# paint window's shown region, with the files
# window forward and the paint window open behind.
# The files window must answer it alone, in plain
# words; the disk's picture sectors, read by
# prove-mend49.sh against the control boot's,
# must stand unmoved.
for _ in press_exchange(GX + 7):
    d = waitdump(row_has("No stick stands in this computer."), 12)
    if d is not None:
        break
expect(d is not None, "the exchange press was answered by the files window alone, in plain words")

done()
