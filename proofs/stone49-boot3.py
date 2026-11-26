# Stone 49 proof, boot 3: no stick stands in this
# computer. The disk is boot 1's, its notes standing
# as they were laid. The files window's exchange
# words stand while a note stands picked — the words
# stand whether or not a stick stands, so the keeper
# can always ask — and both presses are answered in
# the window, in plain words: "No stick stands in
# this computer." Nothing is copied, and nothing
# pretends to be.

import re

BLUE = (0, 0, 170)
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
if d:
    said = decode(d, GY + 14, GX + 2, "To the stick", WHITE)
    expect(said == "To the stick",
           f"the exchange words stand though no stick stands (read: {said!r})")

for _ in press_exchange(GX + 7):
    d = waitdump(row_has("No stick stands in this computer."), 12)
    if d is not None:
        break
expect(d is not None, "'To the stick' with no stick is answered plainly in the window")

# The pick moves to the second note by a press on
# its row (this bench's USB road carries no arrow
# keys — boot 1 tells it), forgetting the spoken
# word, so the second press speaks for itself.
click((GX + 6) * 16 + 8, (GY + 4) * 16 + 8)
park()
for _ in press_exchange(GX + 22):
    d = waitdump(row_has("No stick stands in this computer."), 12)
    if d is not None:
        break
expect(d is not None, "'From the stick' with no stick is answered plainly in the window")

done()
