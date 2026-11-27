# Stone 50 proof, boot 5: no hard disk stands in
# this computer. The disc boots the system and the
# shipped stick stands on the bus, but no hard disk
# is fitted at all. The files window opens — the
# making's row stands whether or not anything is
# kept, for the making concerns the whole machine —
# and the making is asked for and answered in plain
# words: "No hard disk stands in this computer."

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


CUR = [506, 378]


def move_to(x, y):
    while CUR[0] != x or CUR[1] != y:
        dx = max(-61, min(61, x - CUR[0]))
        dy = max(-61, min(61, y - CUR[1]))
        mousemove(dx, dy)
        CUR[0] += dx
        CUR[1] += dy


def click(x, y):
    move_to(x, y)
    mousebutton(1)
    time.sleep(0.4)
    mousebutton(0)
    time.sleep(0.4)


def park():
    move_to(60, 60)


GX, GY = 5, 29

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 150)
expect(d is not None, "the desktop is drawn")

typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 15, GX + 2, "Make this computer a Cardinal", WHITE)
             == "Make this computer a Cardinal", 25)
expect(d is not None, "the files window stands with the making's words, though nothing is kept")

time.sleep(2)
for _try in range(3):
    click((GX + 7) * 16 + 8, (GY + 15) * 16 + 8)
    park()
    d = waitdump(lambda d: d is not None and decode(
        d, GY + 2, GX + 2, "Make this computer a Cardinal?",
        GRAY) == "Make this computer a Cardinal?", 10)
    if d is not None:
        break
expect(d is not None, "the asking opened with no disk in the machine")

time.sleep(2)
for _try in range(3):
    click((GX + 10) * 16 + 8, (GY + 7) * 16 + 8)
    park()
    d = waitdump(lambda d: d is not None and decode(
        d, GY + 15, GX + 2, "No hard disk stands in this computer.",
        WHITE) == "No hard disk stands in this computer.", 15)
    if d is not None:
        break
expect(d is not None, "the making was answered plainly: 'No hard disk stands in this computer.'")

done()
