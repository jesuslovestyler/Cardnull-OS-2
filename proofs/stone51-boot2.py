# Stone 51 proof, boot 2: the bar menu, grown to
# fifteen rows — Picture at the twelfth choice,
# Tunes at the thirteenth, and Rest last still, one
# row lower than Stone 48 left it. A press on the
# Tunes choice opens the tunes window, exactly as
# the word does. A press on Amazing Grace's row —
# the tune standing picked — sings it: the scenario
# waits out its whole reckoned length (about six
# and a half seconds of the speaker's road) and
# finds the window standing whole after the
# singing, its pick unmoved.

import re
import time

BLUE = (0, 0, 170)
GRAY = (170, 170, 170)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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
    try:
        return _decode(d, prow, pcol, text, ink)
    except IndexError:
        return ""


def _decode(d, prow, pcol, text, ink):
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


GX, GY = 14, 32
MT = 31  # the menu's top: the grid's 48 rows less its fifteen and the bar's two

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 150)
expect(d is not None, "the desktop is drawn")
if d is None:
    # A wedged boot (the bench's SeaBIOS trouble)
    # means nothing else in this scenario can speak.
    done()

# The start button opens the menu: fifteen rows,
# Tunes at the thirteenth choice, Rest last.
time.sleep(3)
click(16, 752)
park()
d = waitdump(lambda d: d is not None and d[0] == 1024
             and decode(d, MT + 13, 1, "Tunes", WHITE) == "Tunes", 15)
expect(d is not None, "the menu stands with Tunes at its thirteenth choice")
expect(decode(d, MT + 12, 1, "Picture", WHITE) == "Picture",
       "Picture stands at the twelfth choice still")
expect(decode(d, MT + 14, 1, "Rest", WHITE) == "Rest",
       "Rest stands last, one row lower")

# The Tunes choice opens the window.
click(4 * 16 + 8, (MT + 13) * 16 + 8)
park()
d = waitdump(lambda d: d is not None and d[0] == 1024
             and decode(d, GY, GX + 1, "Tunes", WHITE) == "Tunes", 15)
expect(d is not None, "the menu's Tunes choice opened the tunes window")

# Amazing Grace stands picked; a press on its row
# sings it. Wait out the singing, then find the
# window whole.
click((GX + 6) * 16 + 8, (GY + 3) * 16 + 8)
park()
time.sleep(9)
d = waitdump(lambda d: d is not None and d[0] == 1024
             and decode(d, GY, GX + 1, "Tunes", WHITE) == "Tunes"
             and decode(d, GY + 3, GX + 2, "Amazing Grace", WHITE)
             == "Amazing Grace", 15)
expect(d is not None, "the window stands whole after the singing, its pick unmoved")

done()
