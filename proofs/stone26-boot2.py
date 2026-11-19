# Stone 26 proof, boot 2: the picture survived. The
# SAME keeping disk boot 1 drew on is fitted again —
# a fresh boot, a fresh machine — and nothing has
# drawn yet in this sitting. The word 'files' lists
# the known note and the kept picture beside it; the
# down arrow picks the picture (its foot says how it
# opens), and Enter opens it in the paint window: the
# feather's opening visit stands, the host lays the
# kept picture back into its cells, and the canvas
# stands with its colors as drawn in the sitting
# before — the Red cell Red, the Blue cell Blue, an
# untouched cell still on the canvas ground, the
# chosen color still Blue with its star standing.

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


def cell_center(row, col):
    return ((col - 8) * 16 + 8, (row + 24) * 16 + 8)


def cell_pixel(d, row, col):
    x, y = cell_center(row, col)
    return pixel(d, x, y)


GX, GY = 5, 31
NOTE = "remember the garden"

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn again, on the same disk")

# The files window lists the note and the picture that
# the sitting before kept — before anything has drawn
# in this sitting at all.
typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 13, GX + 4, "A picture you painted", GRAY)
             == "A picture you painted", 25)
expect(d is not None, "the files window lists the kept picture after a restart")
if d:
    said = decode(d, GY + 3, GX + 4, NOTE, WHITE)
    expect(said == NOTE,
           f"the known note still stands listed beside it (read: {said!r})")

# The down arrow picks the picture: its entry stands
# picked, and the window's foot names it and says how
# it opens.
sendkey("down")
d = waitdump(lambda d: d is not None
             and decode(d, GY + 11, GX + 2, "The picture you picked:", GRAY)
             == "The picture you picked:", 15)
expect(d is not None, "the down arrow picked the picture: its label stands at the foot")
if d:
    said = decode(d, GY + 13, GX + 4, "A picture you painted", WHITE)
    expect(said == "A picture you painted",
           f"the picture's entry now stands picked, white on blue (read: {said!r})")
    said = decode(d, GY + 12, GX + 2, "Press Enter or click it to open it in Paint.", WHITE)
    expect(said == "Press Enter or click it to open it in Paint.",
           f"the foot says in plain words how the picture opens (read: {said!r})")

# Enter opens the picked picture in the paint window.
enter()
d = waitdump(lambda d: d is not None
             and cell_pixel(d, 16, 30) == RED, 25)
expect(d is not None, "Enter opened the kept picture in the paint window: its Red cell stands")
# (Stone 38: the invitation is read on its own wait
# now, as in boot 1 — the heavier repaints can catch
# the window mid-draw on the frame the canvas cell
# first shows in.)
d = waitdump(lambda d: d is not None
             and decode(d, 34, 8, "Pick a color, then draw below.", WHITE)
             == "Pick a color, then draw below.", 15)
if d:
    said = decode(d, 34, 8, "Pick a color, then draw below.", WHITE)
    expect(said == "Pick a color, then draw below.",
           f"the feather's invitation reads whole in the opened picture (read: {said!r})")
    said = decode(d, 36, 8, "Color: Blue", WHITE)
    expect(said == "Color: Blue",
           f"the kept picture's chosen color stands: Blue (read: {said!r})")
    expect(cell_pixel(d, 15, 20) == DBLUE,
           "the kept picture's Blue cell stands Blue")
    expect(cell_pixel(d, 18, 40) == GRAY,
           "an untouched cell stands on the canvas ground, as it was left")
    sx, sy = cell_center(11, 34)
    star = 0
    for y in range(sy - 8, sy + 8):
        for x in range(sx - 8, sx + 8):
            if pixel(d, x, y) == WHITE:
                star += 1
    expect(star > 0, "the chosen star stands on the Blue swatch, as it was left")

done()
