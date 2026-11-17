# Stone 28 proof, boot 1: large print, chosen in the
# settings window on a fitted keeping disk whose card
# is of the OLD shape — C, N, the offset byte 59 for
# Eastern, the chime byte 0, and NO size byte chosen
# (its fifth byte stands 0, as every card laid before
# this stone carries it). The bench clock stands at
# 2026-11-15T00:00:00 on the world's standard time, so
# Eastern shows 19:00 on the bar.
#
# The desktop must rise at the usual size; the settings
# window must show its new third choice — "Words:" with
# "Usual size" standing picked and "Large" unpicked —
# and a press on the Large row must repaint the whole
# desktop at the large size at once: every word decoded
# letter by letter against the system's own letter
# shapes AT THE NEW SCALE (three times size, in
# twenty-four-pixel cells — the decode itself is the
# measure of the bigger words), the bar standing
# twenty-four pixels tall where it stood sixteen. The
# welcome window is then DRAGGED at the large size and
# decoded at its new place, a press on the chime-off
# row in the settings window at the large size stands
# the chime off (painter and pointer agreeing at the
# new size), and the typing line and an answer are
# decoded at the large size too.

import re

BLUE = (0, 0, 170)
WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
DARK = (85, 85, 85)
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
    # Decodes at scale 'sc': a letter cell is sc * 8
    # pixels square — 16 at the usual size (sc 2), 24
    # at large print (sc 3).
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


# The pointer's point, tracked as the scenarios move it:
# it starts at (506, 378) on every boot.
PX, PY = 506, 378


def click(x, y):
    global PX, PY
    mousemove(x - PX, y - PY)
    PX, PY = x, y
    mousebutton(1)
    mousebutton(0)


# The settings window's places: at the usual size,
# left cell 5, top row 30 (fifty-four wide; top row
# 32 until Stone 33, whose bar at the screen's foot
# rose the taller windows' first places); at the
# large size, left cell 1, top row 14 (forty large
# cells wide on the forty-two-cell grid).
UX, UY = 5, 30
LX, LY = 1, 14

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")
if d:
    said = decode(d, 47, 56, "19:", WHITE, 2)
    expect(said == "19:", f"the bar clock starts on Eastern time at the usual size (read: {said!r})")
    said = decode(d, 47, 2, "Cardnull", WHITE, 2)
    expect(said == "Cardnull", f"the bar's title stands at the usual size (read: {said!r})")
    expect(pixel(d, 300, 767) == BLUE and pixel(d, 300, 735) == BLACK,
           "the bar stands at the screen's foot at the usual size, two rows tall")

typewrite("settings")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, UY + 11, UX + 4, "Usual size", WHITE, 2)
             == "Usual size", 25)
expect(d is not None, "the settings window shows 'Usual size' standing picked — the old card's standing")
if d:
    said = decode(d, UY, UX + 1, "Settings", WHITE, 2)
    expect(said == "Settings", f"the window's title reads in plain words (read: {said!r})")
    said = decode(d, UY + 10, UX + 2, "Words:", GRAY, 2)
    expect(said == "Words:", f"the words' size is labelled in plain words (read: {said!r})")
    said = decode(d, UY + 12, UX + 4, "Large", GRAY, 2)
    expect(said == "Large", f"'Large' stands unpicked at the usual size (read: {said!r})")
    said = decode(d, UY + 14, UX + 2, "Your choices are kept on the disk.", GRAY, 2)
    expect(said == "Your choices are kept on the disk.",
           f"the window says the choices are kept on the disk (read: {said!r})")

# A press on the Large row (row 42 at the usual size;
# its point at (168, 680)): the whole desktop must
# stand at the large size at once.
click(168, 680)
d = waitdump(lambda d: d is not None
             and decode(d, LY + 12, LX + 4, "Large", WHITE, 3)
             == "Large", 25)
expect(d is not None, "clicking 'Large' repainted the window at the large size, 'Large' standing picked")
if d:
    said = decode(d, 31, 2, "Cardnull", WHITE, 3)
    expect(said == "Cardnull", f"the bar's title stands large (read: {said!r})")
    said = decode(d, 31, 34, "19:", WHITE, 3)
    expect(said == "19:", f"the bar clock stands large at its narrow-grid place (read: {said!r})")
    expect(pixel(d, 300, 767) == BLUE and pixel(d, 1016, 719) == BLACK,
           "the bar stands at the screen's foot at the large size, two rows tall")
    said = decode(d, LY, LX + 1, "Settings", WHITE, 3)
    expect(said == "Settings", f"the window's title stands large (read: {said!r})")
    said = decode(d, LY + 2, LX + 2, "Time zone:", GRAY, 3)
    expect(said == "Time zone:", f"the time zone label stands large (read: {said!r})")
    said = decode(d, LY + 3, LX + 4, "Eastern time", WHITE, 3)
    expect(said == "Eastern time", f"the time choice stands large, still picked (read: {said!r})")
    said = decode(d, LY + 10, LX + 2, "Words:", GRAY, 3)
    expect(said == "Words:", f"the words' label stands large (read: {said!r})")
    said = decode(d, LY + 11, LX + 4, "Usual size", GRAY, 3)
    expect(said == "Usual size", f"'Usual size' stands unpicked now (read: {said!r})")
    said = decode(d, LY + 14, LX + 2, "Your choices are kept on the disk.", GRAY, 3)
    expect(said == "Your choices are kept on the disk.",
           f"the keeping word stands large (read: {said!r})")
    expect(pixel(d, 25, 492) == DARK and pixel(d, 985, 492) == (10, 18, 22)
           and pixel(d, 995, 492) == BLACK,
           "the settings window's frame spans forty large cells (x 24 to 983), "
           "its Stone 33 shadow standing just past its right edge")

# Escape closes the settings window; the welcome
# window is then dragged at the large size: its point
# is laid on its title bar at (492, 84) — the welcome
# stands at left cell 4, top row 3 at this size — the
# button goes down, and four small steps carry the
# point by (+48, +96) in all.
sendkey("esc")
d = waitdump(lambda d: d is not None and pixel(d, 100, 396) == BLACK, 15)
expect(d is not None, "Escape closed the settings window at the large size")
mousemove(492 - PX, 84 - PY)
PX, PY = 492, 84
mousebutton(1)
for _ in range(4):
    mousemove(12, 24)
    PX, PY = PX + 12, PY + 24
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, 7, 7, "Welcome", WHITE, 3) == "Welcome", 25)
expect(d is not None, "the welcome window was dragged at the large size and reads at its new place")
if d:
    said = decode(d, 8, 8, "Welcome to Cardnull", BLACK, 3)
    expect(said == "Welcome to Cardnull",
           f"the dragged window's body stands large at the new place (read: {said!r})")
    expect(pixel(d, 108, 84) == BLACK,
           "the ground the welcome window stood on is plain desktop again")

# The settings window again, at the large size: a
# press on the chime-off row (row 22 at this size; its
# point at (252, 540)) must land where the words stand.
typewrite("settings")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, LY + 7, LX + 4, "Chime on", WHITE, 3)
             == "Chime on", 25)
expect(d is not None, "the settings window reopened at the large size, the chime standing on")
click(252, 540)
d = waitdump(lambda d: d is not None
             and decode(d, LY + 8, LX + 4, "Chime off", WHITE, 3)
             == "Chime off", 25)
expect(d is not None, "clicking the chime-off row at the large size stood the chime off")
if d:
    said = decode(d, LY + 7, LX + 4, "Chime on", GRAY, 3)
    expect(said == "Chime on", f"the chime-on row stands unpicked now (read: {said!r})")

# The typing line and an answer, at the large size:
# Escape closes the window, 'hello' is typed (its echo
# decoded on the typing line, row 29 at this size) and
# answered (the answer decoded in the answers region,
# whose first row is row 16 at this size).
sendkey("esc")
typewrite("hello")
d = waitdump(lambda d: d is not None
             and decode(d, 29, 2, "hello", GRAY, 3) == "hello", 15)
expect(d is not None, "the typing line echoes at the large size")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, 16, 2, "Hello. It is good to see you.", GRAY, 3)
             == "Hello. It is good to see you.", 25)
expect(d is not None, "the answer stands at the large size")

done()
