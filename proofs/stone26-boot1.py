# Stone 26 proof, boot 1: paint keeps its pictures. A
# fitted keeping disk stands ready (its settings card
# and one known note laid by prove-stone26.sh). The
# word 'paint' opens the paint feather as it always
# has (Stone 24); the bench's PS/2 mouse draws on the
# real pointer road — a Red cell, the Blue swatch, a
# Blue cell — and every press visit that stands is
# written through to the disk's picture store by the
# host (the feather itself never touches the disk).
# The word 'files' then lists the kept picture beside
# the known note, in plain words, and a press on the
# picture's row opens it again in the paint window.
# prove-stone26.sh reads the disk's own bytes after
# this boot, and boot 2 proves the picture survived.

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
    mousemove(x - CUR[0], y - CUR[1])
    CUR[0], CUR[1] = x, y


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


# The files window's place (Stone 19): left cell 5, top
# row 32; the kept picture's entry stands on its last
# row, GY + 13, its words at column GX + 4.
GX, GY = 5, 30
NOTE = "remember the garden"

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

# The word 'paint' asks for the paint feather.
typewrite("paint")
enter()
RX, RY = cell_center(11, 16)
d = waitdump(lambda d: d is not None and pixel(d, RX, RY) == RED, 25)
expect(d is not None, "the paint window stands with the feather's swatches painted")
if d:
    park()
    time.sleep(0.6)
    d = dump()
    said = decode(d, 36, 8, "Color: Red", WHITE)
    expect(said == "Color: Red",
           f"the feather names its first chosen color (read: {said!r})")
    expect(cell_pixel(d, 16, 30) == GRAY,
           "the canvas stands empty before any drawing")

# Draw: a Red cell at (16, 30).
click(*cell_center(16, 30))
park()
d = waitdump(lambda d: d is not None
             and cell_pixel(d, 16, 30) == RED, 15)
expect(d is not None, "a press on the canvas paints its cell Red")

# The Blue swatch, then a Blue cell at (15, 20).
click(*cell_center(11, 34))
park()
time.sleep(0.6)
d = dump()
if d:
    said = decode(d, 36, 8, "Color: Blue", WHITE)
    expect(said == "Color: Blue",
           f"the feather names its new chosen color (read: {said!r})")
click(*cell_center(15, 20))
park()
d = waitdump(lambda d: d is not None
             and cell_pixel(d, 15, 20) == DBLUE, 15)
expect(d is not None, "a press on the canvas now paints Blue")

# The files window lists the kept picture beside the
# known note, in plain words.
typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, "Notes kept on the disk:", GRAY)
             == "Notes kept on the disk:", 25)
expect(d is not None, "the word 'files' opened the files window on the disk's keeping")
if d:
    said = decode(d, GY + 3, GX + 4, NOTE, WHITE)
    expect(said == NOTE,
           f"the known note stands listed, picked (read: {said!r})")
    said = decode(d, GY + 13, GX + 4, "A picture you painted", GRAY)
    expect(said == "A picture you painted",
           f"the kept picture stands listed beside the notes (read: {said!r})")

# A press on the picture's row opens it again in the
# paint window: the point is laid at (200, 728), on the
# entry's row (cell row 45).
click(200, (GY + 13) * 16 + 8)
park()
d = waitdump(lambda d: d is not None
             and cell_pixel(d, 16, 30) == RED, 15)
expect(d is not None, "a press on the picture's row opened the paint window again")
# (Stone 38: the status line is read on its own wait
# now — the desktop's repaints grew heavier with the
# terminal window standing in them, and the frame
# that first shows the picture's canvas can catch
# the window's painting mid-draw, its status not yet
# laid; the standing pattern is to wait for the
# words themselves.)
d = waitdump(lambda d: d is not None
             and decode(d, 36, 8, "Color: Blue", WHITE) == "Color: Blue", 15)
if d:
    said = decode(d, 36, 8, "Color: Blue", WHITE)
    expect(said == "Color: Blue",
           f"the opened picture keeps its chosen color (read: {said!r})")
    expect(cell_pixel(d, 15, 20) == DBLUE,
           "the opened picture keeps its Blue cell")

done()
