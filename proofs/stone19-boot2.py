# Stone 19 proof, boot 2: the files window with NO disk
# fitted. It must say so in plain words — there is no
# disk fitted, and nothing is saved — and show no entry
# and no picked note: nothing is invented for an empty
# store. The words are DECODED letter by letter against
# the system's own letter shapes, as in boot 1.

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

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, "There is no disk fitted.", GRAY)
             == "There is no disk fitted.", 25)
expect(d is not None, "with no disk fitted, the window says so in plain words")
if d:
    said = decode(d, GY + 3, GX + 2, "Nothing is saved.", GRAY)
    expect(said == "Nothing is saved.",
           f"and it says nothing is saved (read: {said!r})")
    said = decode(d, GY + 11, GX + 2, "The note you picked:", GRAY)
    expect(said == " " * len("The note you picked:"),
           "no picked note is shown — no entry was invented")

done()
