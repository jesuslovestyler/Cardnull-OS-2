# Stone 20 proof, boot 1: the settings window, with a
# fitted keeping disk (the settings card on sector 8 —
# C, N, and the offset byte 59 for Eastern; the chime
# byte stands 0, as a card laid before Stone 20 carries,
# so the chime stands on). The bench clock stands at
# 2026-11-15T00:00:00 on the world's standard time, so
# Eastern shows 19:00 and the world's standard 00:00 on
# the bar — the window's clicks are verified against the
# bar clock's own rendered letters, decoded letter by
# letter against the system's own letter shapes, as the
# feather and files proofs decode.
#
# The word 'settings' opens the window; its standing
# choices are read back from its rows; a press of the
# pointer on the world's-standard row moves the clock;
# a press on the chime-off row turns the chime off; Tab
# cycles through all four windows; Escape closes the
# settings window; and the typed word 'eastern' still
# moves the clock back, answered in plain words that
# say the disk will remember it.

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


# The settings window's place on this face (1024x768,
# sixty-four cells across): fifty-four wide, centered —
# left at cell 5, top at cell row 30 (cell row 32 until
# Stone 33, whose bar at the screen's foot rose the
# taller windows' first places). Title at row 30,
# "Time zone:" at 32, the Eastern choice at 33 and the
# world's standard at 34 (their words at column 9),
# "Welcome chime:" at 36, the chime choices at 37 and
# 38, and the keeping word at 44 (column 7) — it stood at 42
# until Stone 28 grew the window by the words' size
# choice, and the word moved down with the window. The bar
# clock stands at row 47, column 56.
GX, GY = 5, 30

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")
if d:
    said = decode(d, 47, 56, "19:", WHITE)
    expect(said == "19:", f"the bar clock starts on Eastern time (read: {said!r})")

typewrite("settings")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 3, GX + 4, "Eastern time", WHITE)
             == "Eastern time", 25)
expect(d is not None, "the word 'settings' opened the settings window, Eastern standing picked")
if d:
    said = decode(d, GY, GX + 1, "Settings", WHITE)
    expect(said == "Settings", f"the window's title reads in plain words (read: {said!r})")
    said = decode(d, GY + 2, GX + 2, "Time zone:", GRAY)
    expect(said == "Time zone:", f"the time zone is labelled in plain words (read: {said!r})")
    said = decode(d, GY + 4, GX + 4, "World's standard time", GRAY)
    expect(said == "World's standard time",
           f"the world's standard choice stands unpicked (read: {said!r})")
    said = decode(d, GY + 6, GX + 2, "Welcome chime:", GRAY)
    expect(said == "Welcome chime:", f"the chime is labelled in plain words (read: {said!r})")
    said = decode(d, GY + 7, GX + 4, "Chime on", WHITE)
    expect(said == "Chime on", f"the chime stands on, as the old card left it (read: {said!r})")
    said = decode(d, GY + 14, GX + 2, "Your choices are kept on the disk.", GRAY)
    expect(said == "Your choices are kept on the disk.",
           f"the window says the choices are kept on the disk (read: {said!r})")

# The typed word 'eastern' still works, exactly as
# before: it is answered in plain words (and the disk
# keeps it, as the answer says). The clicks below then
# move the choice again, so the disk this boot leaves
# behind carries the clicked choices for boot 2.
# (Stone 38: the answer stands in the terminal
# window now — the console's kept rows, at its inner
# left edge — not on the desktop's ground where the
# answers strip stood; the check reads the window's
# kept rows for the answer's line.)
typewrite("eastern")
enter()
d = waitdump(lambda d: d is not None
             and any(decode(d, r, 7, "The clock now shows Eastern time.", GRAY)
                     == "The clock now shows Eastern time."
                     for r in range(33, 44)), 15)
expect(d is not None, "the typed word 'eastern' is answered in plain words, as before")

# A press of the pointer on the world's-standard row
# (its point at (200, 552), cell row 34): the arrow
# starts with its point at (506, 378).
mousemove(-306, 174)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, 47, 56, "00:", WHITE) == "00:", 15)
expect(d is not None, "clicking the world's standard choice moved the bar clock to 00")
# Park the arrow off the window's words, then read the
# window's own standing back.
mousemove(500, -500)
d = waitdump(lambda d: d is not None
             and decode(d, GY + 4, GX + 4, "World's standard time", WHITE)
             == "World's standard time", 15)
expect(d is not None, "the window now shows the world's standard time standing picked")
if d:
    said = decode(d, GY + 3, GX + 4, "Eastern time", GRAY)
    expect(said == "Eastern time",
           f"Eastern stands unpicked now (read: {said!r})")

# A press on the chime-off row (its point at (200, 616),
# cell row 38): the arrow's point stands at (700, 52)
# after the parking above.
mousemove(-500, 564)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, GY + 7, GX + 4, "Chime on", GRAY) == "Chime on", 15)
expect(d is not None, "clicking the chime-off row unpicked the chime-on row")
mousemove(500, -500)
d = waitdump(lambda d: d is not None
             and decode(d, GY + 8, GX + 4, "Chime off", WHITE) == "Chime off", 15)
expect(d is not None, "the window now shows the chime standing off")

# Tab cycles through the open windows (Stone 38:
# five stand open now — the terminal window stands
# open from the rising, and the cycle reaches it
# between the settings window and the welcome):
# settings to terminal, terminal to welcome, welcome
# to feather, feather back to settings
# (the files window stands closed and is passed over).
sendkey("tab")
d = waitdump(lambda d: d is not None and pixel(d, 400, 32 * 16 + 10) == BLUE
             and pixel(d, 400, GY * 16 + 10) == DARK, 15)
expect(d is not None, "Tab brought the terminal window forward, the settings window behind")
sendkey("tab")
d = waitdump(lambda d: d is not None and pixel(d, 400, 90) == BLUE
             and pixel(d, 400, GY * 16 + 10) == DARK, 15)
expect(d is not None, "Tab brought the welcome window forward, the settings window behind")
sendkey("tab")
d = waitdump(lambda d: d is not None and pixel(d, 400, 426) == BLUE, 15)
expect(d is not None, "Tab again brought the feather window forward")
sendkey("tab")
d = waitdump(lambda d: d is not None and pixel(d, 400, GY * 16 + 10) == BLUE, 15)
expect(d is not None, "Tab again brought the settings window forward")

# Escape closes the settings window back to the desktop;
# the welcome window stands forward in its place.
sendkey("esc")
d = waitdump(lambda d: d is not None and pixel(d, 400, GY * 16 + 10) == BLACK
             and pixel(d, 600, 600) == BLACK, 15)
expect(d is not None, "Escape closed the settings window back to the desktop")
if d:
    expect(pixel(d, 400, 90) == BLUE,
           "the welcome window stands forward in its place")

done()
