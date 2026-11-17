# Stone 30 proof, boot 1: the calculator feather,
# exercised on the REAL path. The shipped disc is
# booted at the BIOS door (the face of light), the
# word 'calculator' is typed, and the calculator
# feather must come through the door — checked first,
# as its plain-words answer line says — and then
# RECKON:
#
#   - the window shows the feather's own painting: its
#     invitation decoded letter by letter, its keys in
#     their colors with their plain words decoded, and
#     the sum's line standing at "0";
#   - presses on its painted keys work real sums, the
#     line decoded off the feather's cells after each
#     stage: 7 add 5 is 12; a Clear; 9 take away 4 is
#     5; 5 take away 9 is -4 (a sum below nothing,
#     carried honestly); 6 times 7 is 42; 10 share out
#     3 is 3, 1 left over (the remainder named); 5
#     share out 0 answered "Cannot share out by 0." —
#     plainly, and the machine still standing;
#   - Escape closes the window, the bar's menu — its
#     nine choices decoded, Calculator the seventh —
#     opens it again by a press on the Calculator
#     choice, and a press on its close mark closes it.
#
# Every press is a fresh visit through the door: the
# host carries the press across the desk (gift 1000
# plus the row times 100 plus the column), the feather
# reckons, and its standing lives in its cells between
# visits. The sums only come out right if the feather
# truly reckons across visits. The presses are the
# bench's PS/2 mouse (the monitor's mouse_move and
# mouse_button, as the pointer proofs drive it). The
# arrow is parked at the desktop's corner before each
# reading, so no reading ever reads the arrow.
#
# The window's place on this face (1024x768, sixty-four
# cells across): fifty-four wide, centered — left at
# cell 5, top at the layout's row for the text face's
# row 17 (cell row 32). The feather's cells stand 1:1
# in it: the cell (row, col) of the feather's region
# stands at window cell (row + 24, col - 8). The sum's
# line stands on the feather's row 11 — screen row 35
# — its words from screen column 9, black on the
# line's light gray.

import re

BLUE = (0, 0, 170)
RED = (170, 0, 0)
GREEN = (0, 170, 0)
PURPLE = (170, 0, 170)
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


def sumline(d):
    """The sum's line as it stands: decoded across its
    whole span — forty-eight cells from its first
    letter — with an empty cell read as the space it
    is (the line's own words stand apart by spaces:
    "7 add 5 is 12"), and the trailing emptiness
    trimmed away."""
    out = []
    for i in range(48):
        bm = cell_bitmap(d, (9 + i) * 16, 35 * 16, BLACK)
        if all(v == 0 for v in bm):
            out.append(" ")
            continue
        best, bestd = None, 999
        for code, g in GLYPHS.items():
            dist = sum(bin(a ^ b).count("1") for a, b in zip(bm, g))
            if dist < bestd:
                bestd, best = dist, code
        out.append(chr(best) if bestd <= 2 else "?")
    return "".join(out).rstrip()


def press(row, col, want):
    """Press the feather's key at cell (row, col) and
    wait for the sum's line to read `want`."""
    click(*cell_center(row, col))
    park()
    d = waitdump(lambda d: d is not None and sumline(d) == want, 15)
    expect(d is not None,
           f"after the press at ({row}, {col}) the sum's line reads {want!r}")


# The keys' cells in the feather's own reckoning.
K7, K8, K9 = (13, 18), (13, 24), (13, 30)
K4, K5, K6 = (14, 18), (14, 24), (14, 30)
K1, K2, K3 = (15, 18), (15, 24), (15, 30)
K0 = (16, 18)
ADD, TAKE, TIMES, SHARE = (13, 40), (14, 40), (15, 40), (16, 40)
EQUALS, CLEAR = (16, 27), (17, 24)

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

# The word 'calculator' asks for the calculator feather.
typewrite("calculator")
enter()

# The opening visit stands: a working key's ground is
# painted (a ground cell clear of any letter — a key's
# lettered cell centers carry the letter's own white).
KX, KY = cell_center(13, 35)
d = waitdump(lambda d: d is not None and pixel(d, KX, KY) == PURPLE, 25)
expect(d is not None, "the calculator window stands with the feather's keys painted")
if d:
    park()
    time.sleep(0.6)
    d = dump()
    said = decode(d, 24, 2, "The calculator feather visited. Press its keys to reckon.", GRAY)
    expect(said == "The calculator feather visited. Press its keys to reckon.",
           f"the door's plain-words line says the calculator feather visited (read: {said!r})")
    said = decode(d, 34, 8, "Press the keys to reckon a sum.", WHITE)
    expect(said == "Press the keys to reckon a sum.",
           f"the feather's invitation reads whole in its window (read: {said!r})")
    expect(sumline(d) == "0",
           f"the sum's line stands at 0 at the opening (read: {sumline(d)!r})")
    expect(cell_pixel(d, 13, 16) == BLUE, "a figure key stands blue")
    expect(cell_pixel(d, 13, 44) == PURPLE, "a working key stands purple")
    expect(cell_pixel(d, 16, 23) == GREEN, "the Equals key stands green")
    expect(cell_pixel(d, 17, 18) == RED, "the Clear key stands red")
    said = decode(d, 37, 10, "7", WHITE)
    expect(said == "7", f"the 7 key names its figure (read: {said!r})")
    said = decode(d, 37, 31, "Add", WHITE)
    expect(said == "Add", f"the Add key names its working (read: {said!r})")
    said = decode(d, 38, 28, "Take away", WHITE)
    expect(said == "Take away", f"the Take away key names its working (read: {said!r})")
    said = decode(d, 39, 30, "Times", WHITE)
    expect(said == "Times", f"the Times key names its working (read: {said!r})")
    said = decode(d, 40, 28, "Share out", WHITE)
    expect(said == "Share out", f"the Share out key names its working (read: {said!r})")
    said = decode(d, 40, 16, "Equals", WHITE)
    expect(said == "Equals", f"the Equals key names itself (read: {said!r})")
    said = decode(d, 41, 14, "Clear", WHITE)
    expect(said == "Clear", f"the Clear key names itself (read: {said!r})")

# Add: 7 add 5 is 12 — each stage of the standing
# reckoning decoded off the line.
press(*K7, "7")
press(*ADD, "7 add")
press(*K5, "7 add 5")
press(*EQUALS, "7 add 5 is 12")

# A Clear empties the reckoning.
press(*CLEAR, "0")

# Take away: 9 take 4 is 5, and 5 take 9 is -4 — a sum
# below nothing, carried honestly.
press(*K9, "9")
press(*TAKE, "9 take")
press(*K4, "9 take 4")
press(*EQUALS, "9 take 4 is 5")
press(*CLEAR, "0")
press(*K5, "5")
press(*TAKE, "5 take")
press(*K9, "5 take 9")
press(*EQUALS, "5 take 9 is -4")

# Times: 6 times 7 is 42.
press(*CLEAR, "0")
press(*K6, "6")
press(*TIMES, "6 times")
press(*K7, "6 times 7")
press(*EQUALS, "6 times 7 is 42")

# Share out: 10 share 3 is 3, 1 left over — the whole
# answer with the remainder named.
press(*CLEAR, "0")
press(*K1, "1")
press(*K0, "10")
press(*SHARE, "10 share")
press(*K3, "10 share 3")
press(*EQUALS, "10 share 3 is 3, 1 left over")

# Sharing out by 0 is answered plainly, and the
# machine stands: 5 share 0, Equals.
press(*CLEAR, "0")
press(*K5, "5")
press(*SHARE, "5 share")
press(*K0, "5 share 0")
press(*EQUALS, "Cannot share out by 0.")
press(*CLEAR, "0")

# Escape closes the window.
sendkey("esc")
d = waitdump(lambda d: d is not None
             and pixel(d, 200, 32 * 16 + 8) == BLACK, 15)
expect(d is not None, "Escape closed the calculator window")

# The menu: a press on the start button opens it,
# risen from the bar at the screen's foot, its nine
# choices decoded — the eight windows' names and Rest
# last. The point stands parked at (60, 60).
move_to(16, 752)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, 43, 1, "Calculator", WHITE) == "Calculator", 25)
expect(d is not None, "a press on the start button opened the menu, with Calculator standing in it")
if d:
    for i, word in enumerate(("Welcome", "Feather", "Files", "Settings",
                              "Editor", "Verse", "Calculator", "Help", "Rest")):
        said = decode(d, 37 + i, 1, word, WHITE)
        expect(said == word,
               f"the menu's choice {i + 1} reads {word!r} (read: {said!r})")

# A press on the Calculator choice opens the window
# again, exactly as the typed word does. The point
# stands at (16, 752); the choice's row is the seventh
# — its cell center (40, 696).
click(40, 696)
park()
d = waitdump(lambda d: d is not None
             and cell_pixel(d, 13, 35) == PURPLE, 25)
expect(d is not None, "a press on the menu's Calculator choice opened the calculator window")
if d:
    expect(sumline(d) == "0",
           f"the sum's line stands as it was left (read: {sumline(d)!r})")

# A press on its close mark closes it: the mark's cell
# stands at the window's top row, two cells in from
# its right edge — screen cell (57, 32). The point
# stands parked at (60, 60); the way is walked in two
# moves, as Stone 29's proof walks it — one great move
# saturates the pointer's reckoning on the bench and
# falls short.
move_to(490, 290)
move_to(920, 520)
mousebutton(1)
time.sleep(0.4)
mousebutton(0)
time.sleep(0.4)
d = waitdump(lambda d: d is not None
             and pixel(d, 200, 32 * 16 + 8) == BLACK, 15)
expect(d is not None, "a press on the calculator window's close mark closed it")

done()
