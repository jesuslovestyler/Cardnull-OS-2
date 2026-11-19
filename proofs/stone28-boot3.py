# Stone 28 proof, boot 3: a FRESH keeping disk whose
# card is of the old shape — C, N, the offset byte 59
# for Eastern, the chime byte 0, and the size byte 0,
# as every card laid before this stone carries it. The
# desktop must rise at the USUAL size: an old card
# behaves exactly as it always has. The settings
# window must show 'Usual size' standing picked and
# 'Large' unpicked, and the chime standing on, as the
# old card has always left it.

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


UX, UY = 5, 30

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")
if d:
    said = decode(d, 47, 56, "19:", WHITE, 2)
    expect(said == "19:", f"an old-shape card rises at the usual size, on Eastern time (read: {said!r})")
    # Stone 38 adaptation: the pixel just above the bar
    # (300, 735) was the old ground's black before the
    # desktop-at-boot world; now the terminal window
    # stands there, and the pixel is its bottom frame
    # edge (dark gray) — still not bar blue, so the bar
    # is exactly two rows tall, as named.
    expect(pixel(d, 300, 767) == BLUE and pixel(d, 300, 735) == (85, 85, 85),
           "the bar stands at the screen's foot, two rows tall: the usual size, as before this stone")

typewrite("settings")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, UY + 11, UX + 4, "Usual size", WHITE, 2)
             == "Usual size", 25)
expect(d is not None, "the settings window shows 'Usual size' standing picked from the old card")
if d:
    said = decode(d, UY + 12, UX + 4, "Large", GRAY, 2)
    expect(said == "Large", f"'Large' stands unpicked (read: {said!r})")
    said = decode(d, UY + 7, UX + 4, "Chime on", WHITE, 2)
    expect(said == "Chime on", f"the chime stands on, as the old card left it (read: {said!r})")

done()
