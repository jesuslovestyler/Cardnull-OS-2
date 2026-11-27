# Stone 49 proof, boot 1: the exchange to the stick.
# A fitted keeping disk stands ready (its Eastern
# card, a first note standing under its own words,
# and a second carrying the name "roof note", laid by
# prove-stone49.sh), and a blank USB stick stands on
# the bus. The word 'files' lists the notes; the
# window's last row — the window grew by that row for
# this stone, its top standing one row higher, at row
# 30 — carries "To the stick" and "From the stick"
# while the first note stands picked (DECODED). A
# press on "To the stick" copies the note and the
# window answers "Copied to the stick." on that row.
# The pick moves to the second note — the exchange
# words stand again, the spoken word forgotten — and
# it is copied likewise. (The pick is moved by a
# press on the thing's own row throughout this
# proof: the bench's stick shape carries a USB
# keyboard, and the USB road's key table — Stone
# 12's road, as it stands — carries no arrow keys,
# so the arrows cannot move the pick on this bench.
# The arrow way stands proved by the companions on
# the PS/2 bench; the row press is the window's own
# other way, and it forgets the spoken word the
# same.) A picture is then painted
# and kept the bench's way (Stone 26's drawing: a Red
# cell and a Blue cell), the files window picks it,
# and it is copied likewise. The refusals follow: the
# picture copied again is answered "A picture already
# stands on the stick.", and the first note copied
# again, "That name already stands on the stick." —
# each in plain words in the window, nothing
# overwritten. The stick's own bytes are read by
# prove-stone49.sh between the boots.

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


# The files window's place (Stone 19; its top one row
# higher since this stone grew it by the exchange
# row, and one row higher again since Stone 50 grew
# it by the Cardinal door's row): left cell 5, top
# row 29. Its foot stands on
# GY + 11, the picked note's words on GY + 12, the
# picture's entry on GY + 13, and the exchange's row
# on GY + 14 — "To the stick" at GX + 2, "From the
# stick" at GX + 16, and the exchange's spoken word
# at GX + 2 on the same row.
GX, GY = 5, 29


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


# The desktop's wait is long on purpose: with a USB
# stick on the bus, SeaBIOS walks the bus before it
# reads the disc, and on this bench that walk can
# take the better part of a minute — once, under
# load, more — before the face of light rises at
# all.
d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 150)
expect(d is not None, "the desktop is drawn")

# The files window lists the disk's two notes; the
# first stands picked, and the exchange words stand
# on the window's last row.
typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, "Notes kept on the disk:", GRAY)
             == "Notes kept on the disk:", 25)
expect(d is not None, "the word 'files' opened the files window on the disk's keeping")
if d:
    said = decode(d, GY + 14, GX + 2, "To the stick", WHITE)
    expect(said == "To the stick",
           f"'To the stick' stands on the window's last row (read: {said!r})")
    said = decode(d, GY + 14, GX + 16, "From the stick", WHITE)
    expect(said == "From the stick",
           f"'From the stick' stands beside it (read: {said!r})")

# A press on "To the stick" copies the first note;
# the window answers on the same row.
for _ in press_exchange(GX + 7):
    d = waitdump(row_has("Copied to the stick."), 12)
    if d is not None:
        break
expect(d is not None, "a press on 'To the stick' copied the first note, answered in the window")

# The pick moves to the second note, by a press on
# its row: the spoken word is forgotten and the
# exchange words stand again.
click((GX + 6) * 16 + 8, (GY + 4) * 16 + 8)
park()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 14, GX + 2, "To the stick", WHITE)
             == "To the stick", 15)
expect(d is not None, "the pick's move forgot the spoken word; the exchange words stand again")
for _ in press_exchange(GX + 7):
    d = waitdump(row_has("Copied to the stick."), 12)
    if d is not None:
        break
expect(d is not None, "the second note was copied to the stick likewise")

# A picture is painted and kept, Stone 26's drawing:
# a Red cell at (16, 30), the Blue swatch, a Blue
# cell at (15, 20).
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

# The files window picks the kept picture, and it is
# copied to the stick likewise. The pick is made by
# a press on the picture's row — which also opens
# the picture in the paint window, Stone 26's way —
# and the word 'files' raises the files window
# again, the picture standing picked in it.
typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, "Notes kept on the disk:", GRAY)
             == "Notes kept on the disk:", 25)
expect(d is not None, "the files window stands forward again for the picture's picking")
click((GX + 6) * 16 + 8, (GY + 13) * 16 + 8)
park()
typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 11, GX + 2, "The picture you picked:", GRAY)
             == "The picture you picked:", 15)
expect(d is not None, "a press on the picture's row picked the kept picture")
for _ in press_exchange(GX + 7):
    d = waitdump(row_has("Copied to the stick."), 12)
    if d is not None:
        break
expect(d is not None, "the kept picture was copied to the stick")

# The refusals: the picture copied again, and the
# first note copied again — each answered plainly,
# nothing overwritten. The picture is picked again
# by its row (through the paint window and back, as
# above), which forgets the spoken word; the first
# note by its own row.
click((GX + 6) * 16 + 8, (GY + 13) * 16 + 8)
park()
typewrite("files")
enter()
for _ in press_exchange(GX + 7):
    d = waitdump(row_has("A picture already stands on the stick."), 12)
    if d is not None:
        break
expect(d is not None, "the picture copied again is refused in plain words")
click((GX + 6) * 16 + 8, (GY + 3) * 16 + 8)
park()
for _ in press_exchange(GX + 7):
    d = waitdump(row_has("That name already stands on the stick."), 12)
    if d is not None:
        break
expect(d is not None, "the first note copied again is refused in plain words")

done()
