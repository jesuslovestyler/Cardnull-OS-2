# Stone 49 proof, boot 2: the exchange from the
# stick. The disk is boot 1's (two notes — the second
# standing under the name "roof note" with the words
# "call billy about the roof" — and the picture boot
# 1 painted and kept). The stick now stands prepared
# with a keeping of its own (prove-stone49.sh): one
# note standing under the same name "roof note" with
# other words, "the roof is fixed now", and a kept
# picture of its own, named "stick picture", its
# canvas ground throughout with one red cell at the
# block's row 5, column 10.
#
# "From the stick" on the first note is refused in
# the window — "The stick holds no note of that
# name." On the second note it is answered "Brought
# in from the stick.", and the note's words at the
# window's foot are the stick's words now. On the
# picture it is answered the same, and the picture
# window then shows the stick's picture in its big
# measure: the red cell standing at its own place,
# and the ground standing where the disk's red cell
# stood. The disk's and stick's bytes are read by
# prove-stone49.sh after the boot.

import re

BLUE = (0, 0, 170)
RED = (170, 0, 0)
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


# The files window's place, as in boot 1.
GX, GY = 5, 30

# The picture window's place (Stone 48): left cell
# 7, top row 30, fifty wide, sixteen high. Canvas
# cell (row, col) of the feather's canvas stands in
# it at block column col - 16, block row row - 14,
# each block sixteen pixels wide and thirty-two
# tall. The stick's red cell stands at the block's
# row 5, column 10 — the canvas's row 15, column 24.
PX, PY = 7, 30


def pic_block_center(row, col):
    x = PX * 16 + 16 + (col - 16) * 16 + 8
    y = PY * 16 + 16 + (row - 14) * 32 + 16
    return (x, y)


def press_exchange(col):
    time.sleep(2)
    for _try in range(3):
        click(col * 16 + 8, (GY + 14) * 16 + 8)
        park()
        yield


def row_has(text):
    return lambda d: d is not None and \
        decode(d, GY + 14, GX + 2, text, WHITE) == text


d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 150)
expect(d is not None, "the desktop is drawn")

typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, "Notes kept on the disk:", GRAY)
             == "Notes kept on the disk:", 25)
expect(d is not None, "the word 'files' opened the files window on the disk's keeping")

# The first note stands picked; the stick holds no
# note of its name — the press is refused plainly.
for _ in press_exchange(GX + 22):
    d = waitdump(row_has("The stick holds no note of that name."), 12)
    if d is not None:
        break
expect(d is not None, "'From the stick' on the first note is refused in plain words")

# The second note: its words stand at the foot
# before, and the stick's words after the bringing
# in. (The pick is moved by a press on its row, as
# boot 1 tells: this bench's USB road carries no
# arrow keys.)
click((GX + 6) * 16 + 8, (GY + 4) * 16 + 8)
park()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 12, GX + 2, "call billy about the roof", WHITE)
             == "call billy about the roof", 15)
expect(d is not None, "the second note stands picked, its own words at the foot")
for _ in press_exchange(GX + 22):
    d = waitdump(row_has("Brought in from the stick."), 12)
    if d is not None:
        break
expect(d is not None, "'From the stick' brought the stick's twin of the note in")
if d:
    said = decode(d, GY + 12, GX + 2, "the roof is fixed now", WHITE)
    expect(said == "the roof is fixed now",
           f"the note's words at the foot are the stick's words now (read: {said!r})")

# The picture: brought in likewise, and the picture
# window shows the stick's picture — its red cell at
# its own place, the ground where the disk's red
# cell stood (the canvas's row 16, column 30).
click((GX + 6) * 16 + 8, (GY + 13) * 16 + 8)
park()
typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 11, GX + 2, "The picture you picked:", GRAY)
             == "The picture you picked:", 15)
expect(d is not None, "a press on the picture's row picked the kept picture")
for _ in press_exchange(GX + 22):
    d = waitdump(row_has("Brought in from the stick."), 12)
    if d is not None:
        break
expect(d is not None, "'From the stick' brought the stick's picture in")
time.sleep(2)
for _try in range(3):
    click(36 * 16, (GY + 11) * 16 + 8)
    park()
    d = waitdump(lambda d: d is not None
                 and decode(d, PY, PX + 1, "Picture", WHITE) == "Picture", 12)
    if d is not None:
        break
expect(d is not None, "a press on 'Look at it' opened the picture window")
if d:
    x, y = pic_block_center(15, 24)
    expect(pixel(d, x, y) == RED,
           "the stick's red cell stands in the picture window, at its own place")
    x, y = pic_block_center(16, 30)
    expect(pixel(d, x, y) == GRAY,
           "the ground stands where the disk's red cell stood — the picture is the stick's")

done()
