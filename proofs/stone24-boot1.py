# Stone 24 proof, boot 1: the paint feather, exercised
# on the REAL path. The shipped disc is booted at the
# BIOS door (the face of light), the word 'paint' is
# typed, and the paint feather must come through the
# door — checked first, as its plain-words answer line
# and its own painted window say — and then DRAW:
#
#   - the window shows the feather's own painting: its
#     invitation decoded letter by letter, its swatches
#     in their colors, its chosen color named ("Color:
#     Red" at the opening), its canvas standing empty
#     on its light-gray ground;
#   - a press of the pointer on one canvas cell paints
#     that cell in the chosen color (Red), read back as
#     pixels;
#   - a drag with the button held paints along its
#     path — the cells it crossed stand Red too;
#   - a press on the Blue swatch chooses Blue: the
#     feather's own words in the window say "Color:
#     Blue", the star stands on the Blue swatch and has
#     left the Red, and the next canvas press paints
#     Blue;
#   - a press on the feather's Clear word empties the
#     canvas again: every painted cell back to the
#     canvas ground, the swatches still standing.
#
# The presses are the bench's PS/2 mouse (the monitor's
# mouse_move and mouse_button, as the pointer proofs
# drive it): they travel the system's own pointer road,
# are carried across the feather door's desk as visits,
# and every mark checked here was laid by the feather
# itself in answer. The arrow is parked at the
# desktop's corner before each reading, so no reading
# ever reads the arrow.
#
# Stone 38 adaptation: the door's plain-words line no
# longer stands on the desktop's ground (the old
# answers strip at row 24) — the console lives in the
# terminal window now, and the paint window stands on
# the terminal's own first place, over it. The line is
# therefore read at the end, in the terminal once
# Escape has closed the paint window and the terminal
# stands revealed — Stone 30's road for its own door
# line. There it wraps at the window's measure: its
# first line ends at "then", and "draw." stands on
# the row below it.
#
# The window's place on this face (1024x768, sixty-four
# cells across): fifty-four wide, centered — left at
# cell 5, top at the layout's row for the text face's
# row 17 (cell row 32). The feather's cells stand 1:1
# in it: the cell (row, col) of the feather's region
# stands at window cell (row + 24, col - 8).

import re

BLUE = (0, 0, 170)
RED = (170, 0, 0)
GREEN = (0, 170, 0)
DBLUE = (0, 0, 170)
PURPLE = (170, 0, 170)
ORANGE = (170, 85, 0)
BLACK = (0, 0, 0)
GRAY = (170, 170, 170)
WHITE = (255, 255, 255)

# The system's letter shapes, from its own font file
# (the featherpaint proof's decoding, carried here).
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


# The arrow's point, tracked as the bench moves it: it
# starts at the screen's middle, its point two pixels
# in from its corner (504 + 2, 376 + 2).
CUR = [506, 378]


def move_to(x, y):
    mousemove(x - CUR[0], y - CUR[1])
    CUR[0], CUR[1] = x, y


def click(x, y):
    move_to(x, y)
    mousebutton(1)
    time.sleep(0.4)
    mousebutton(0)
    time.sleep(0.4)


def park():
    move_to(60, 60)


def cell_center(row, col):
    """The screen pixel at the center of the feather
    cell (row, col), as the window carries it 1:1."""
    return ((col - 8) * 16 + 8, (row + 24) * 16 + 8)


def cell_pixel(d, row, col):
    x, y = cell_center(row, col)
    return pixel(d, x, y)


d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

# The word 'paint' asks for the paint feather.
typewrite("paint")
enter()

# The opening visit stands: the Red swatch is painted
# (its first cell — the swatch's middle cell carries
# the chosen star, whose white is not the swatch's red).
RX, RY = cell_center(11, 16)
d = waitdump(lambda d: d is not None and pixel(d, RX, RY) == RED, 25)
expect(d is not None, "the paint window stands with the feather's swatches painted")
if d:
    park()
    time.sleep(0.6)
    d = dump()
    said = decode(d, 34, 8, "Pick a color, then draw below.", WHITE)
    expect(said == "Pick a color, then draw below.",
           f"the feather's invitation reads whole in its window (read: {said!r})")
    said = decode(d, 36, 8, "Color: Red", WHITE)
    expect(said == "Color: Red",
           f"the feather names its first chosen color (read: {said!r})")
    expect(cell_pixel(d, 11, 16) == RED, "the Red swatch stands red")
    expect(cell_pixel(d, 11, 24) == GREEN, "the Green swatch stands green")
    expect(cell_pixel(d, 11, 32) == DBLUE, "the Blue swatch stands blue")
    expect(cell_pixel(d, 11, 40) == PURPLE, "the Purple swatch stands purple")
    expect(cell_pixel(d, 11, 48) == ORANGE, "the Orange swatch stands orange")
    expect(cell_pixel(d, 11, 56) == BLACK, "the Black swatch stands black")
    expect(cell_pixel(d, 16, 30) == GRAY,
           "the canvas stands empty on its light-gray ground")
    expect(cell_pixel(d, 18, 40) == GRAY,
           "the canvas stands empty at its far corner too")

# A press on a canvas cell paints it in the chosen
# color: cell (16, 30), Red.
click(*cell_center(16, 30))
park()
d = waitdump(lambda d: d is not None
             and cell_pixel(d, 16, 30) == RED, 15)
expect(d is not None, "a press on the canvas paints its cell in the chosen color (Red)")

# A drag paints along its path: from (16, 30) held
# down, across to (18, 40).
move_to(*cell_center(16, 30))
mousebutton(1)
time.sleep(0.4)
for step in [(392, 656), (424, 664), (456, 672), (488, 680)]:
    move_to(*step)
    time.sleep(0.4)
move_to(*cell_center(18, 40))
time.sleep(0.4)
mousebutton(0)
time.sleep(0.4)
park()
d = waitdump(lambda d: d is not None
             and cell_pixel(d, 18, 40) == RED, 15)
expect(d is not None, "the drag's end cell stands painted (Red)")
if d:
    expect(cell_pixel(d, 17, 34) == RED,
           "a cell the drag crossed stands painted too")

# A press on the Blue swatch chooses Blue.
click(*cell_center(11, 34))
park()
time.sleep(0.6)
d = dump()
if d:
    said = decode(d, 36, 8, "Color: Blue", WHITE)
    expect(said == "Color: Blue",
           f"the feather names its new chosen color (read: {said!r})")
    sx, sy = cell_center(11, 34)
    star = 0
    for y in range(sy - 8, sy + 8):
        for x in range(sx - 8, sx + 8):
            if pixel(d, x, y) == WHITE:
                star += 1
    expect(star > 0, "the chosen star stands on the Blue swatch")
    sx, sy = cell_center(11, 18)
    star = 0
    for y in range(sy - 8, sy + 8):
        for x in range(sx - 8, sx + 8):
            if pixel(d, x, y) == WHITE:
                star += 1
    expect(star == 0, "the star has left the Red swatch")

# The next canvas press paints Blue: cell (15, 20).
click(*cell_center(15, 20))
park()
d = waitdump(lambda d: d is not None
             and cell_pixel(d, 15, 20) == DBLUE, 15)
expect(d is not None, "a press on the canvas now paints Blue")

# A press on the feather's Clear word empties the
# canvas: every painted cell back to its ground.
click(*cell_center(12, 59))
park()
d = waitdump(lambda d: d is not None
             and cell_pixel(d, 16, 30) == GRAY
             and cell_pixel(d, 18, 40) == GRAY
             and cell_pixel(d, 15, 20) == GRAY, 15)
expect(d is not None, "the Clear word empties the canvas: every painted cell is ground again")
if d:
    expect(cell_pixel(d, 11, 16) == RED,
           "the swatches still stand after the clearing")
    said = decode(d, 36, 8, "Color: Blue", WHITE)
    expect(said == "Color: Blue",
           f"the chosen color stands after the clearing (read: {said!r})")

# Escape closes the paint window, and the terminal —
# which shares the paint window's first place and
# still stands there beneath it — stands revealed,
# holding the door's plain-words line in its answers.
sendkey("esc")
d = waitdump(lambda d: d is not None
             and decode(d, 32, 6, "Terminal", WHITE) == "Terminal", 15)
expect(d is not None, "Escape closed the paint window, the terminal standing in its place")
if d:
    said = ""
    for r in range(33, 43):
        if decode(d, r, 7, "The paint feather visited. Pick a color, then", GRAY) \
                == "The paint feather visited. Pick a color, then":
            said = decode(d, r + 1, 7, "draw.", GRAY)
            break
    expect(said == "draw.",
           f"the door's plain-words line says the paint feather visited (read: {said!r})")

done()
