# Stone 40 proof, boot 2: what a restart finds. The
# SAME keeping disk boot 1 renamed and copied on is
# fitted again — a fresh boot, a fresh machine. The
# files window must list the second and third notes
# under their words, the copy under its given name
# with the first note's words whole at its foot, and
# the picture under its given name: the names and the
# copy truly went through the CNN3 and CNP stores, in
# the page's own order. The editor lists the copy's
# words on the page, as the page's third note.

import re

BLUE = (0, 0, 170)
WHITE = (255, 255, 255)
GRAY = (170, 170, 170)

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


GX, GY = 5, 30
A = "remember the garden"
B = "call billy about the roof"
C = "pray for quinton"
N1 = "garden notes"
N2 = "garden copy"
PN = "garden picture"

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn again, on the same disk")

typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 3, GX + 4, B, WHITE) == B, 25)
expect(d is not None, "after a restart the files window lists the remaining notes")
if d:
    said = decode(d, GY + 4, GX + 4, C, GRAY)
    expect(said == C, f"the third note stands second (read: {said!r})")
    said = decode(d, GY + 5, GX + 4, N2, GRAY)
    expect(said == N2,
           f"the copy stands third, under the name it was given (read: {said!r})")
    said = decode(d, GY + 6, GX + 4, N1, GRAY)
    expect(said == " " * len(N1),
           "no fourth entry stands in the list — the let-go note and its name are gone")
    said = decode(d, GY + 13, GX + 4, PN, GRAY)
    expect(said == PN,
           f"the picture stands under the name it was given (read: {said!r})")

click(200, (GY + 5) * 16 + 8)
park()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 5, GX + 4, N2, WHITE) == N2, 15)
expect(d is not None, "a press on the copy's row picked the copy after the restart")
if d:
    said = decode(d, GY + 12, GX + 2, A, WHITE)
    expect(said == A,
           f"the copy's words stand whole at the foot after the restart (read: {said!r})")

# The editor's first place stands at row 32 still
# (Stone 33 rose only the taller windows), so its rows
# are read at EY, two more than the files window's GY
# since Stone 49 grew the files window by its exchange row (the editor
# itself stands where it stood, at row 32).
EY = GY + 2
typewrite("editor")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, EY + 4, GX + 4, B, GRAY) == B, 25)
expect(d is not None, "after a restart the editor window lists the page")
if d:
    said = decode(d, EY + 5, GX + 4, C, GRAY)
    expect(said == C, f"the editor lists the third note (read: {said!r})")
    said = decode(d, EY + 6, GX + 4, A, GRAY)
    expect(said == A,
           f"the editor lists the copy by its words — the first note's words, kept whole (read: {said!r})")

done()
