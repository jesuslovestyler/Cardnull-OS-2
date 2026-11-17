# Stone 28 proof, boot 4: NO disk at all. The size
# choice must still work for the sitting, and the
# settings window must say so in plain words, the way
# it already does for the other choices — at the usual
# size first ("Your choices last only for this
# sitting." with "There is no disk fitted." beneath),
# and, after a press on the Large row, at the large
# size too: the same words, decoded at the large scale
# (the foot's line is longer than the narrow grid
# holds whole, so its first thirty-eight letters are
# decoded where they stand, and the line beneath it is
# decoded whole).

import re

BLUE = (0, 0, 170)
WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
BLACK = (0, 0, 0)

_vals = {}
for _m in re.finditer(r"block\[(\d+)\] = (\d+)",
                      open("src/font.nifla").read()):
    _vals[int(_m.group(1))] = int(_m.group(2))
GLYPHS = {}
for _code in range(32, 127):
    GLYPHS[_code] = tuple(_vals.get((_code - 32) * 8 + _r, 0)
                          for _r in range(8))


def cell_bitmap(d, cx, cy, ink, sc):
    rows = []
    for r in range(8):
        v = 0
        for c in range(8):
            if pixel(d, cx + sc * c + 1, cy + sc * r + 1) == ink:
                v |= 1 << (7 - c)
        rows.append(v)
    return tuple(rows)


def decode(d, prow, pcol, text, ink, sc):
    out = []
    for i in range(len(text)):
        bm = cell_bitmap(d, (pcol + i) * sc * 8, prow * sc * 8, ink, sc)
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


PX, PY = 506, 378


def click(x, y):
    global PX, PY
    mousemove(x - PX, y - PY)
    PX, PY = x, y
    mousebutton(1)
    mousebutton(0)


UX, UY = 5, 30
LX, LY = 1, 14

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

typewrite("settings")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, UY + 14, UX + 2, "Your choices last only for this sitting.", GRAY, 2)
             == "Your choices last only for this sitting.", 25)
expect(d is not None, "with no disk fitted, the window says the choices last only for this sitting")
if d:
    said = decode(d, UY + 15, UX + 2, "There is no disk fitted.", GRAY, 2)
    expect(said == "There is no disk fitted.",
           f"the window says there is no disk fitted (read: {said!r})")

# A press on the Large row (its point at (168, 712),
# as in boot 1): the choice works for the sitting, and
# the sitting-only words stand at the large size.
click(168, 680)
d = waitdump(lambda d: d is not None
             and decode(d, LY + 12, LX + 4, "Large", WHITE, 3)
             == "Large", 25)
expect(d is not None, "with no disk, clicking 'Large' still stands the words large for the sitting")
if d:
    said = decode(d, LY + 14, LX + 2, "Your choices last only for this sittin", GRAY, 3)
    expect(said == "Your choices last only for this sittin",
           f"the sitting-only words stand large (read: {said!r})")
    said = decode(d, LY + 15, LX + 2, "There is no disk fitted.", GRAY, 3)
    expect(said == "There is no disk fitted.",
           f"the no-disk words stand large (read: {said!r})")

done()
