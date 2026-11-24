# Boot 1 of Stone 44's proof: the shipped disc booted
# at the BIOS door with a second display adapter
# fitted (-device secondary-vga,id=vga2), the bench's
# clock pinned to a known morning (Tuesday, November
# 24, 2026). The main desktop must stand untouched,
# and the second head — read through the monitor's
# own screendump for that device (tools/pixels.py's
# dump2) — must stand at the granted screen's own
# shape, 1024 by 768, wearing the companion page:
# the desktop's deep glass ground, the system's name
# large, "The second screen", the day and the date in
# plain words, the clock's face, and the Psalm 127
# lines — every line DECODED against the system's own
# letter shapes. And when the minute turns, the page
# must be painted again: the clock's face on the
# second screen shows a new minute while nothing on
# the first screen was asked to move.

import re
import time

BLUE = (0, 0, 170)
WHITE = (255, 255, 255)
GLASS = (31, 94, 110)
PALE = (200, 216, 220)

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


def dec2(d, y, sc, text):
    # One line of the companion page: centered, its
    # letters 'sc' times the font's own size, in the
    # page's pale ink on its glass ground.
    n = len(text)
    x0 = (1024 - n * 8 * sc) // 2
    out = []
    for i in range(n):
        rows = []
        for r in range(8):
            v = 0
            for c in range(8):
                if pixel(d, x0 + (i * 8 + c) * sc + sc // 2,
                         y + r * sc + sc // 2) == PALE:
                    v |= 1 << (7 - c)
            rows.append(v)
        bm = tuple(rows)
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
expect(d is not None, "the main desktop stands with a second adapter fitted")
if d:
    said = decode(d, 2, 4, "Files", WHITE)
    expect(said == "Files",
           f"the Files icon's name reads on the main screen (read: {said!r})")

d2 = None
for _ in range(60):
    d2 = dump2("vga2")
    if d2 is not None and d2[0] == 1024 and d2[1] == 768:
        break
    time.sleep(0.5)
expect(d2 is not None and d2[0] == 1024 and d2[1] == 768,
       "the second head stands at 1024 by 768")
if d2 and d2[0] == 1024:
    expect(count(d2, GLASS) > 700000,
           f"the second screen's ground is the desktop's glass ({count(d2, GLASS)} px)")
    for (y, sc, text) in [(150, 3, "Cardnull"),
                          (260, 2, "The second screen"),
                          (350, 2, "Tuesday, November 24, 2026"),
                          (520, 2, "Unless Yahweh builds the house,"),
                          (570, 2, "they labor in vain who build it."),
                          (620, 2, "Psalm 127:1")]:
        said = dec2(d2, y, sc, text)
        expect(said == text,
               f"the page's line at {y} reads {text!r} (read: {said!r})")
    clk = dec2(d2, 400, 2, "00:00:00")
    shape = (len(clk) == 8 and clk[2] == ":" and clk[5] == ":"
             and clk[0:2].isdigit() and clk[3:5].isdigit()
             and clk[6:8].isdigit())
    expect(shape, f"the clock's face stands on the page (read: {clk!r})")
    if shape:
        firstminute = clk[3:5]
        turned = None
        for _ in range(22):
            time.sleep(5)
            d2 = dump2("vga2")
            if d2 is None or d2[0] != 1024:
                continue
            clk2 = dec2(d2, 400, 2, "00:00:00")
            if (len(clk2) == 8 and clk2[2] == ":" and clk2[5] == ":"
                    and clk2[3:5].isdigit() and clk2[3:5] != firstminute):
                turned = clk2
                break
        expect(turned is not None,
               f"the page is painted again when the minute turns ({clk!r} -> {turned!r})")

done()
