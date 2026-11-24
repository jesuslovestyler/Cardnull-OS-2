# Boot 2 of Stone 44's proof: the shipped disc booted
# at the BIOS door with NO second adapter fitted. The
# desktop must stand exactly as it always has, and
# there must be no second head to read: the raising
# finds nothing, claims nothing, and nothing anywhere
# changes.

import re

BLUE = (0, 0, 170)
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


d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 3000, 60)
expect(d is not None, "the desktop stands as before with no second adapter")
if d:
    said = decode(d, 2, 4, "Files", WHITE)
    expect(said == "Files",
           f"the Files icon's name reads (read: {said!r})")
    said = decode(d, 28, 7, "No feather has visited yet.", (170, 170, 170))
    expect(said == "No feather has visited yet.",
           f"the feather window stands as before (read: {said!r})")

d2 = dump2("vga2")
expect(d2 is None, "no second head stands to be read")

done()
