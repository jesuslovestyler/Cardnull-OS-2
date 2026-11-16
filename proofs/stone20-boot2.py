# Stone 20 proof, boot 2: the SAME keeping disk boot 1
# left behind — its card now carries the clicked choices
# (the world's standard offset, and the chime off), laid
# by the window's clicks and checked byte for byte by
# the shell between the boots. Nothing is typed but the
# word 'settings': the bar clock must already stand on
# the world's standard time (00, where boot 1 began on
# Eastern's 19), and the window must show both choices
# as boot 1 left them — the choices persisted from the
# settings card, not from anything this boot did.

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
if d:
    said = decode(d, 0, 56, "00:", WHITE)
    expect(said == "00:",
           f"the bar clock stands on the world's standard time from the disk's card (read: {said!r})")

typewrite("settings")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 4, GX + 4, "World's standard time", WHITE)
             == "World's standard time", 25)
expect(d is not None, "the settings window shows the clicked time zone, persisted")
if d:
    said = decode(d, GY + 3, GX + 4, "Eastern time", GRAY)
    expect(said == "Eastern time",
           f"Eastern stands unpicked, as boot 1 left it (read: {said!r})")
    said = decode(d, GY + 8, GX + 4, "Chime off", WHITE)
    expect(said == "Chime off",
           f"the chime stands off, persisted from the card (read: {said!r})")
    said = decode(d, GY + 7, GX + 4, "Chime on", GRAY)
    expect(said == "Chime on",
           f"the chime-on row stands unpicked (read: {said!r})")
    said = decode(d, GY + 10, GX + 2, "Your choices are kept on the disk.", GRAY)
    expect(said == "Your choices are kept on the disk.",
           f"the window still says the choices are kept (read: {said!r})")

done()
