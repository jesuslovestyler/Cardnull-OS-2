# Stone 50 proof, boot 3: the disk alone, again.
# Boot 2's disk is booted once more, alone, and the
# files window is asked for its list: the note typed
# on the disk's own boot in boot 2 must stand there
# still — keeping written after the installing
# survives the installed disk's reboot, through the
# disk's own store paths, exactly as keeping always
# has.

import re

BLUE = (0, 0, 170)
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


GX, GY = 5, 29

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 120)
expect(d is not None, "the desktop rose from the hard disk alone again")

typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, "Notes kept on the disk:", GRAY)
             == "Notes kept on the disk:", 25)
expect(d is not None, "the files window opened on the disk's keeping")
if d:
    said = decode(d, GY + 3, GX + 4, "remember the garden", WHITE)
    expect(said == "remember the garden",
           f"the first note still stands (read: {said!r})")
    said = decode(d, GY + 4, GX + 4, "roof note", GRAY)
    expect(said == "roof note",
           f"the second note still stands (read: {said!r})")
    said = decode(d, GY + 5, GX + 4, "written on the disk itself", GRAY)
    expect(said == "written on the disk itself",
           f"the note written on the disk's own boot survived its reboot (read: {said!r})")
    said = decode(d, GY + 13, GX + 4, "kept picture", GRAY)
    expect(said == "kept picture",
           f"the kept picture still stands (read: {said!r})")

done()
