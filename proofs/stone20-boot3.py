# Stone 20 proof, boot 3: NO disk fitted at all. The
# settings window must say plainly that the choices
# last only for this sitting — and they must still work
# for the sitting: a press on the world's-standard row
# moves the bar clock, and the window shows the new
# standing, with nothing anywhere pretending the disk
# will remember it.

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


GX, GY = 5, 30

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

typewrite("settings")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 14, GX + 2, "Your choices last only for this sitting.", GRAY)
             == "Your choices last only for this sitting.", 25)
expect(d is not None, "with no disk fitted, the window says the choices last only for this sitting")
if d:
    said = decode(d, GY + 15, GX + 2, "There is no disk fitted.", GRAY)
    expect(said == "There is no disk fitted.",
           f"and it says there is no disk fitted (read: {said!r})")
    said = decode(d, GY + 3, GX + 4, "Eastern time", WHITE)
    expect(said == "Eastern time",
           f"the disc's own Eastern choice stands picked (read: {said!r})")

# The choice still works for the sitting: a press on
# the world's-standard row (point (200, 552)) moves the
# bar clock, and the window shows the new standing.
mousemove(-306, 174)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, 47, 56, "00:", WHITE) == "00:", 15)
expect(d is not None, "clicking still moved the clock for this sitting, with no disk at all")
mousemove(500, -500)
d = waitdump(lambda d: d is not None
             and decode(d, GY + 4, GX + 4, "World's standard time", WHITE)
             == "World's standard time", 15)
expect(d is not None, "the window shows the sitting's new standing, honestly labelled")

done()
