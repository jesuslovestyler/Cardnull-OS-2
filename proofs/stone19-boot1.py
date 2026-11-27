# Stone 19 proof, boot 1: the files window, with a fitted
# keeping disk prepared with three known notes (the CNN3
# store laid directly, as prove-stone15.sh lays it: the
# settings card on sector 8, the notes header on sector
# 64, one sector to a note from sector 65).
#
# The word 'files' opens the window; its rendered list is
# DECODED letter by letter against the system's own
# letter shapes (parsed from src/font.nifla, the way
# prove-featherpaint.sh reads) and compared against the
# known notes; the down arrow moves the pick and the
# picked note's whole words must stand at the window's
# foot; a press of the pointer on the third entry's row
# picks it instead; Tab cycles through all three windows;
# and Escape closes the files window back to the desktop.

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


# The files window's place on this face (1024x768,
# sixty-four cells across): fifty-four wide, centered —
# left at cell 5, top at cell row 29 — one row higher
# since Stone 50 grew the list by the Cardinal door's
# row (row 30 through Stone 49; the taller windows'
# first places rose at Stone 33, whose bar at the
# screen's foot took the foot's two rows). Title at
# row 29, heading at 31, the list at rows 32 onward
# (entries' words at column 9), the picked note's
# label at row 40 and its words at row 41 (column 7).
GX, GY = 5, 29
NOTES = ["remember the garden",
         "call billy about the roof",
         "pray for quinton"]

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, "Notes kept on the disk:", GRAY)
             == "Notes kept on the disk:", 25)
expect(d is not None, "the word 'files' opened the files window on the disk's notes")
if d:
    said = decode(d, GY, GX + 1, "Files", WHITE)
    expect(said == "Files", f"the window's title reads in plain words (read: {said!r})")
    said = decode(d, GY + 3, GX + 4, NOTES[0], WHITE)
    expect(said == NOTES[0],
           f"the first entry stands picked, white on blue (read: {said!r})")
    said = decode(d, GY + 4, GX + 4, NOTES[1], GRAY)
    expect(said == NOTES[1], f"the second entry is listed (read: {said!r})")
    said = decode(d, GY + 5, GX + 4, NOTES[2], GRAY)
    expect(said == NOTES[2], f"the third entry is listed (read: {said!r})")
    said = decode(d, GY + 11, GX + 2, "The note you picked:", GRAY)
    expect(said == "The note you picked:",
           f"the picked note is labelled in plain words (read: {said!r})")
    said = decode(d, GY + 12, GX + 2, NOTES[0], WHITE)
    expect(said == NOTES[0],
           f"the picked note's whole words stand at the window's foot (read: {said!r})")

# The down arrow moves the pick to the second note.
sendkey("down")
d = waitdump(lambda d: d is not None
             and decode(d, GY + 12, GX + 2, NOTES[1], WHITE) == NOTES[1], 15)
expect(d is not None, "the down arrow picked the second note: its words stand at the foot")
if d:
    said = decode(d, GY + 4, GX + 4, NOTES[1], WHITE)
    expect(said == NOTES[1],
           f"the second entry now stands picked, white on blue (read: {said!r})")

# A press of the pointer on the third entry's row picks
# it: the arrow's point stands at (506, 378); a move of
# (-306, +174) lays it at (200, 552), on the third
# entry's row (cell row 34 — one higher since Stone
# 50 grew the files window by the Cardinal door's
# row; cell row 35 through Stone 49, which grew it
# by its exchange row).
mousemove(-306, 174)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, GY + 12, GX + 2, NOTES[2], WHITE) == NOTES[2], 15)
expect(d is not None, "a press on the third entry picked it: its words stand at the foot")
# The arrow stands on that entry's row, over one of its
# letters; park it up on the welcome window before
# reading the entry itself back.
mousemove(500, -400)
d = waitdump(lambda d: d is not None
             and decode(d, GY + 5, GX + 4, NOTES[2], WHITE) == NOTES[2], 15)
expect(d is not None, "the third entry now stands picked, white on blue")

# Tab cycles through the open windows (Stone 38:
# four stand open now — the terminal window stands
# open from the rising, and the cycle reaches it
# between the files window and the welcome): files
# to terminal, terminal to welcome, welcome to
# feather, feather back to files.
sendkey("tab")
d = waitdump(lambda d: d is not None and pixel(d, 400, 32 * 16 + 10) == BLUE
             and pixel(d, 400, GY * 16 + 10) == DARK, 15)
expect(d is not None, "Tab brought the terminal window forward, the files window behind")
sendkey("tab")
d = waitdump(lambda d: d is not None and pixel(d, 400, 90) == BLUE
             and pixel(d, 400, GY * 16 + 10) == DARK, 15)
expect(d is not None, "Tab brought the welcome window forward, the files window behind")
sendkey("tab")
d = waitdump(lambda d: d is not None and pixel(d, 400, 426) == BLUE, 15)
expect(d is not None, "Tab again brought the feather window forward")
sendkey("tab")
d = waitdump(lambda d: d is not None and pixel(d, 400, GY * 16 + 10) == BLUE, 15)
expect(d is not None, "Tab again brought the files window forward")

# Escape closes the files window back to the desktop;
# the welcome window stands forward in its place.
sendkey("esc")
d = waitdump(lambda d: d is not None and pixel(d, 400, GY * 16 + 10) == BLACK
             and pixel(d, 600, 600) == BLACK, 15)
expect(d is not None, "Escape closed the files window back to the desktop")
if d:
    expect(pixel(d, 400, 90) == BLUE,
           "the welcome window stands forward in its place")

done()
