# Stone 27 proof, boot 2: what a restart finds. The
# SAME keeping disk boot 1 let two notes go on is fitted
# again — a fresh boot, a fresh machine. The files
# window and the editor window must both list the one
# remaining note and neither of the let-go ones: the
# removal truly went through the disk's CNN3 store, in
# the page's own order, the remaining note whole.

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


GX, GY = 5, 32
A = "remember the garden"
B = "call billy about the roof"
C = "pray for quinton"

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn again, on the same disk")

typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 3, GX + 4, B, WHITE) == B, 25)
expect(d is not None, "after a restart the files window lists the remaining note")
if d:
    said = decode(d, GY + 12, GX + 2, B, WHITE)
    expect(said == B,
           f"the remaining note stands whole at the foot (read: {said!r})")
    said = decode(d, GY + 4, GX + 4, C, GRAY)
    expect(said == " " * len(C),
           "the note let go in the editor is gone from the list")
    said = decode(d, GY + 4, GX + 4, A, GRAY)
    expect(said == " " * len(A),
           "the note let go in the files window is gone from the list")

typewrite("editor")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 4, GX + 4, B, GRAY) == B, 25)
expect(d is not None, "after a restart the editor window lists the remaining note")
if d:
    said = decode(d, GY + 5, GX + 4, C, GRAY)
    expect(said == " " * len(C),
           "the editor's list holds the one remaining note only")

done()
