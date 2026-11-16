# Stone 28 proof, boot 2: the SAME keeping disk boot 1
# left behind — its card now carries the size byte 2
# (large) and the chime byte 2 (off), written through
# by boot 1's clicks. Nothing is chosen at the rise:
# the desktop must come up LARGE from the card, the
# bar's title and clock decoded at the large scale,
# and the settings window must show both choices as
# boot 1 left them. A press on the 'Usual size' row at
# the large size then brings the desktop back to the
# usual size at once — painter and pointer agreeing at
# the large size on the way back, too.

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


UX, UY = 5, 32
LX, LY = 1, 16

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")
if d:
    said = decode(d, 0, 1, "Cardnull", WHITE, 3)
    expect(said == "Cardnull", f"the desktop rose large from the card (read: {said!r})")
    said = decode(d, 0, 34, "19:", WHITE, 3)
    expect(said == "19:", f"the bar clock stands large from the card (read: {said!r})")
    expect(pixel(d, 300, 23) == BLUE and pixel(d, 300, 24) == BLACK,
           "the bar stands twenty-four pixels tall: large print persisted")

typewrite("settings")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, LY + 12, LX + 4, "Large", WHITE, 3)
             == "Large", 25)
expect(d is not None, "the settings window shows 'Large' standing picked, as boot 1 left it")
if d:
    said = decode(d, LY + 8, LX + 4, "Chime off", WHITE, 3)
    expect(said == "Chime off", f"the chime stands off, as boot 1 left it (read: {said!r})")
    said = decode(d, LY + 11, LX + 4, "Usual size", GRAY, 3)
    expect(said == "Usual size", f"'Usual size' stands unpicked (read: {said!r})")
    said = decode(d, LY + 14, LX + 2, "Your choices are kept on the disk.", GRAY, 3)
    expect(said == "Your choices are kept on the disk.",
           f"the window says the choices are kept on the disk (read: {said!r})")

# A press on the 'Usual size' row at the large size
# (row 27; its point at (252, 660)): the desktop must
# stand at the usual size at once.
click(252, 660)
d = waitdump(lambda d: d is not None
             and decode(d, UY + 11, UX + 4, "Usual size", WHITE, 2)
             == "Usual size", 25)
expect(d is not None, "clicking 'Usual size' at the large size restored the usual size at once")
if d:
    said = decode(d, 0, 56, "19:", WHITE, 2)
    expect(said == "19:", f"the bar clock stands at the usual size again (read: {said!r})")
    said = decode(d, UY, UX + 1, "Settings", WHITE, 2)
    expect(said == "Settings", f"the window's title stands at the usual size again (read: {said!r})")
    expect(pixel(d, 300, 15) == BLUE and pixel(d, 300, 16) == BLACK,
           "the bar stands sixteen pixels tall again")

done()
