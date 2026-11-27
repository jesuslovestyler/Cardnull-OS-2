# Stone 51 proof, boot 1: the word 'tunes' opens
# the tunes window forward — its title, its line of
# plain words, the three tunes' names with Amazing
# Grace standing picked (white on blue), its word
# about the waiting, and its chip on the bar. A
# press on Jesus Loves Me's row moves the pick to
# it; the scenario then waits out the tune's whole
# reckoned singing length (its notes sum to about
# twelve seconds of the speaker's road) before it
# trusts the desktop again. The window then drags
# three cells right by its title bar — the take-hold
# reckoning now running over fourteen windows — and
# its close mark puts it away, chip and all.

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


# The tunes window's place: centered (left 14) at
# the layout's row 17 (top 29), thirty-six wide.
GX, GY = 14, 32

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 150)
expect(d is not None, "the desktop is drawn")
if d is None:
    # A wedged boot (the bench's SeaBIOS trouble)
    # means nothing else in this scenario can speak.
    done()

# The rising needs a breath before the keys land —
# on a slow bench boot the first keystrokes can fall
# before the console is listening. Type, wait, and
# if the window has not stood up, type once more
# (the word only ever brings the window forward).
time.sleep(5)
d = None
for _try in range(2):
    typewrite("tunes")
    enter()
    d = waitdump(lambda d: d is not None and d[0] == 1024
                 and decode(d, GY, GX + 1, "Tunes", WHITE) == "Tunes", 20)
    if d is not None:
        break
expect(d is not None, "the word 'tunes' opened the tunes window, forward")
expect(decode(d, GY + 2, GX + 2, "Press a tune, and it will sing.", BLACK)
       == "Press a tune, and it will sing.",
       "its line of plain words stands in it")
expect(decode(d, GY + 3, GX + 2, "Amazing Grace", WHITE) == "Amazing Grace",
       "Amazing Grace stands picked, white on blue")
expect(decode(d, GY + 4, GX + 2, "Jesus Loves Me", BLACK) == "Jesus Loves Me",
       "Jesus Loves Me stands named under it")
expect(decode(d, GY + 5, GX + 2, "Joy to the World", BLACK) == "Joy to the World",
       "Joy to the World stands named under it")
expect(decode(d, GY + 7, GX + 2, "The desktop waits while it sings,", BLACK)
       == "The desktop waits while it sings,",
       "its word about the waiting stands in it")
expect(any(decode(d, r, c, "Tunes", WHITE) == "Tunes"
           for r in (46, 47) for c in range(0, 30)),
       "the window's chip stands on the bar, forward")

# A press on Jesus Loves Me's row: the pick moves,
# and the tune sings — the scenario waits out its
# whole reckoned length before going on.
click((GX + 6) * 16 + 8, (GY + 4) * 16 + 8)
park()
d = waitdump(lambda d: d is not None and d[0] == 1024
             and decode(d, GY + 4, GX + 2, "Jesus Loves Me", WHITE)
             == "Jesus Loves Me", 15)
expect(d is not None, "the press picked Jesus Loves Me, white on blue")
expect(decode(d, GY + 3, GX + 2, "Amazing Grace", BLACK) == "Amazing Grace",
       "Amazing Grace stands unpicked again")
time.sleep(14)

# The drag: take the title bar and carry the window
# three cells right; the title stands at the new
# place. The bench's mouse can lose a packet under
# load and a drag fall short (Stone 47's lesson), so
# the drag is taken in whole-cell steps with a
# settle after each, and retried up to three
# takings, judging the place the drag reached.
def tunes_left(d):
    for c in range(4, 30):
        if decode(d, GY, c + 1, "Tunes", WHITE) == "Tunes":
            return c
    return 0


d = dump()
left = tunes_left(d) if d is not None else GX
for _try in range(3):
    if left == GX + 3:
        break
    move_to((left + 6) * 16 + 8, GY * 16 + 8)
    mousebutton(1)
    time.sleep(0.6)
    for _step in range(3):
        mousemove(16, 0)
        CUR[0] += 16
        time.sleep(0.8)
    mousebutton(0)
    time.sleep(0.8)
    d = dump()
    if d is not None:
        left = tunes_left(d)
park()
expect(left == GX + 3, "the drag carried the window three cells right")

# The close mark puts it away, chip and all.
click((GX + 3 + 34) * 16 + 8, GY * 16 + 8)
park()
d = waitdump(lambda d: d is not None and d[0] == 1024
             and decode(d, GY, GX + 4, "Tunes", WHITE) != "Tunes"
             and not any(decode(d, r, c, "Tunes", WHITE) == "Tunes"
                         for r in (46, 47) for c in range(0, 30)), 15)
expect(d is not None, "the close mark put the window away, chip and all")

done()
