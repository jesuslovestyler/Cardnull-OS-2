# Stone 50 proof, boot 2: the installed disk alone.
# Nothing stands in the machine but boot 1's disk —
# no disc, no stick — and SeaBIOS boots the disk
# itself: its own record names the image at sector
# 2048, the doorman walks from there, and the desktop
# rises from the disk alone. The files window lists
# what stood before the installing — the two notes
# and the kept picture, carried over whole — and a
# new note is typed on this boot and kept, to be
# looked for again after the disk's reboot in boot 3.

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
expect(d is not None, "the desktop rose from the hard disk alone — no disc, no stick in the machine")

typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, "Notes kept on the disk:", GRAY)
             == "Notes kept on the disk:", 25)
expect(d is not None, "the files window opened on the disk's own keeping")
if d:
    said = decode(d, GY + 3, GX + 4, "remember the garden", WHITE)
    expect(said == "remember the garden",
           f"the first note carried over (read: {said!r})")
    said = decode(d, GY + 4, GX + 4, "roof note", GRAY)
    expect(said == "roof note",
           f"the second note carried over, under its name (read: {said!r})")
    said = decode(d, GY + 13, GX + 4, "kept picture", GRAY)
    expect(said == "kept picture",
           f"the kept picture carried over, under its name (read: {said!r})")
    said = decode(d, GY + 15, GX + 2, "Make this computer a Cardinal", WHITE)
    expect(said == "Make this computer a Cardinal",
           f"the making's words stand on a disk boot too (read: {said!r})")

# A new note, typed and kept on the disk's own boot.
typewrite("note written on the disk itself")
enter()
time.sleep(2)
typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 5, GX + 4, "written on the disk itself", GRAY)
             == "written on the disk itself", 25)
expect(d is not None, "a note typed on the disk's own boot was kept and stands in its list")

done()
