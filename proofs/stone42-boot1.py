# Boot 1 of Stone 42's proof: the Shield showing
# itself, on the shipped disc. At the rising the
# tenth icon stands at the desktop's left edge — its
# name's first letter in the clear beside its
# picture, the rest of the name under the terminal
# window that stands open at the rising, as a window
# stands over the icons it covers (Stone 41's proof
# reads the Bible icon the same honest way) — and its
# gold cross stands on the picture. The word 'shield'
# opens the Shield window: its title, and every one
# of its plain lines decoded — what the Shield does
# at the feather door, the door's reckoning since
# this rising (none let in, none turned away), and
# its two standing truths, that it has no switch and
# sends nothing anywhere. Escape closes it. A press
# on its icon opens it again, and a press on its
# close mark — at (920, 456), the mark's own cell:
# the window stands at left cell 5, fifty-four wide,
# so the mark's cell is 5 + 54 - 2 = 57, pixels 912
# to 928, center 920; its top row is 28, the window
# clamped whole above the bar — closes it. The bar's
# menu — its thirteen choices decoded (Stone 46: the
# menu grew by the Paint and Terminal choices, rose
# two rows higher, and its choices stand in the
# icons' order; Shield stands twelfth and Rest
# last, on the very row Shield stood on before, the
# menu having risen as far as the choice moved
# down) — opens it by a press on the Shield choice. Its chip stands on the bar:
# with the files window forward the Shield's title
# bar stands in its behind gray, and a press on the
# Shield's chip raises it, its bar blue again. And
# after a feather's visit stands, the window's
# reckoning has moved: one let in, none turned away.

import re

BLUE = (0, 0, 170)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FRAME = (85, 85, 85)
GREEN = (0, 170, 0)
PALETTE_GOLD = (255, 255, 85)

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
    if d[0] < (pcol + len(text)) * 16 or d[1] < (prow + 1) * 16:
        return ""
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


def count_in(d, rgb, x0, y0, x1, y1):
    n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pixel(d, x, y) == rgb:
                n += 1
    return n


# The pointer's tracked place and its stepping, as
# Stone 41's proof keeps them: the bench's mouse_move
# is relative, in packets of at most sixty-one, and
# the pointer starts at the desktop's heart.
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
    mousebutton(0)


# The Shield window's place on this face (1024x768,
# sixty-four cells across): fifty-four wide and
# eighteen high, centered — its left at cell 5, its
# top clamped to row 28 so it stands whole above the
# bar. Its title stands at its top row, one cell in;
# its lines two cells in, from two rows below.
SX, SY = 5, 28

LINES = (
    (SY + 2, "The Shield stands on guard."),
    (SY + 4, "Every feather is checked at the door before"),
    (SY + 5, "it may visit: its card is read, its bytes are"),
    (SY + 6, "reckoned, and only one whose reckoning matches"),
    (SY + 7, "its card is let in. One that does not reckon"),
    (SY + 8, "true is turned away in plain words, and"),
    (SY + 9, "never runs."),
    (SY + 14, "The Shield has no switch. It cannot be turned"),
    (SY + 15, "off, and it sends nothing anywhere: nothing"),
    (SY + 16, "about you leaves this machine."),
)

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")
if d:
    said = decode(d, 38, 4, "S", WHITE)
    expect(said == "S",
           f"the Shield icon stands on the desktop, its name's first letter in the clear (read: {said!r})")
    expect(count_in(d, PALETTE_GOLD, 16, 37 * 16, 48, 39 * 16) > 5,
           "the icon's gold cross stands on the desktop")

typewrite("shield")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, SY, SX + 1, "Shield", WHITE) == "Shield", 25)
expect(d is not None, "the word 'shield' opened the Shield window")
if d:
    for row, line in LINES:
        said = decode(d, row, SX + 2, line, BLACK)
        expect(said == line,
               f"the Shield window's line reads exactly (read: {said!r})")
    said = decode(d, SY + 11, SX + 2,
                  "Feathers let in since this rising: 0", BLACK)
    expect(said == "Feathers let in since this rising: 0",
           f"the reckoning stands at none let in (read: {said!r})")
    said = decode(d, SY + 12, SX + 2, "Feathers turned away: 0", BLACK)
    expect(said == "Feathers turned away: 0",
           f"the reckoning stands at none turned away (read: {said!r})")

sendkey("esc")
d = waitdump(lambda d: d is not None
             and decode(d, SY, SX + 1, "Shield", WHITE) != "Shield", 15)
expect(d is not None, "Escape closed the Shield window")

# A press on the icon opens it again: the icon's box
# stands at rows 37 to 39, from the first column.
click(32, 37 * 16 + 24)
d = waitdump(lambda d: d is not None
             and decode(d, SY, SX + 1, "Shield", WHITE) == "Shield", 25)
expect(d is not None, "a press on the Shield icon opened the window")

# A press on the close mark closes it.
click(920, SY * 16 + 8)
d = waitdump(lambda d: d is not None
             and decode(d, SY, SX + 1, "Shield", WHITE) != "Shield", 15)
expect(d is not None, "a press on the Shield window's close mark closed it")

# The menu: a press on the start button opens it, its
# thirteen choices decoded — the twelve windows'
# names in the icons' order (Stone 46), with Shield
# the twelfth choice, and Rest last. The menu rises
# from the bar at the screen's foot: thirteen rows
# from row 33.
click(16, 752)
d = waitdump(lambda d: d is not None
             and decode(d, 44, 1, "Shield", WHITE) == "Shield", 25)
expect(d is not None, "a press on the start button opened the menu, with Shield standing in it")
if d:
    for i, word in enumerate(("Welcome", "Feather", "Files", "Editor",
                              "Paint", "Calculator", "Verse", "Help",
                              "Settings", "Terminal", "Bible", "Shield",
                              "Rest")):
        said = decode(d, 33 + i, 1, word, WHITE)
        expect(said == word,
               f"the menu's choice {i + 1} reads {word!r} (read: {said!r})")

# A press on the Shield choice opens the window
# again, exactly as the typed word does. The choice's
# row stands at (40, 712).
click(40, 712)
d = waitdump(lambda d: d is not None
             and decode(d, SY, SX + 1, "Shield", WHITE) == "Shield", 25)
expect(d is not None, "a press on the menu's Shield choice opened the window")

# The chip: the files window comes forward (its word
# typed), and the Shield's title bar stands in its
# behind gray — a pixel of the bar away from its
# letters, at the window's twentieth column.
typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and pixel(d, (SX + 20) * 16, SY * 16 + 8) == FRAME, 25)
expect(d is not None, "with the files window forward, the Shield's bar stands gray")
# The open windows' chips pack in the icons' order on
# the bar's upper row: Files at column 2, Terminal at
# column 8, Shield at column 17. A press on the
# Shield's chip raises its window: the bar blue again.
click((17 + 2) * 16 + 8, 46 * 16 + 8)
d = waitdump(lambda d: d is not None
             and pixel(d, (SX + 20) * 16, SY * 16 + 8) == BLUE, 25)
expect(d is not None, "a press on the Shield's chip raised its window")

sendkey("esc")
d = waitdump(lambda d: d is not None
             and decode(d, SY, SX + 1, "Shield", WHITE) != "Shield", 15)
expect(d is not None, "Escape closed the Shield window again")

# The reckoning moves: a feather's visit stands, and
# the window opened again tells it — one let in,
# none turned away.
typewrite("feather")
enter()
d = waitdump(lambda d: d is not None and count(d, GREEN) > 10000, 25)
expect(d is not None, "the feather visited")
typewrite("shield")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, SY + 11, SX + 2,
                        "Feathers let in since this rising: 1", BLACK)
             == "Feathers let in since this rising: 1", 25)
expect(d is not None, "the Shield window's reckoning shows the visit let in")
if d:
    said = decode(d, SY + 12, SX + 2, "Feathers turned away: 0", BLACK)
    expect(said == "Feathers turned away: 0",
           f"and still none turned away (read: {said!r})")

done()
