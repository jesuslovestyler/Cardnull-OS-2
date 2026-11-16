# Stone 23 proof, boot 1: the bar's menu, with no disk
# fitted — the windows open the same, and the files
# window says plainly that no disk is fitted.
#
# A press of the pointer on the top bar (the Cardnull
# bar) opens the menu just under it, and the menu's
# five choices are DECODED letter by letter against the
# system's own letter shapes (parsed from
# src/font.nifla, the way prove-featherpaint.sh reads):
# Welcome, Feather, Files, Settings, Editor, one to a
# row at the menu's reckoned place (left cell 0, top
# row 1, twelve wide, five high — the place its painter
# and the pointer's pressing both read). A press on
# the Files choice opens the files window, exactly as
# the typed word does: its title and its plain heading
# are decoded at the window's own place. Escape then
# closes the files window, as it always has.
#
# The menu is opened again and dismissed by a press on
# the plain desktop elsewhere: the menu's ground must
# stand plain desktop again, no window may have opened
# (the files window's title-bar ground stays black),
# and the welcome window's title must still decode —
# the desktop whole. The typed word 'files' then opens
# the files window again, exactly as before. Finally
# the menu is opened once more and Escape puts IT away
# — and no window closes with it: the files window's
# title still decodes. The bar's clock is checked still
# standing at the bar's right end: its white figures on
# the blue bar.

import re

BLUE = (0, 0, 170)
WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
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


def menu_ground_clean(d):
    """Every pixel of the menu's own ground that no
    window covers — rows 1 to 4, cells 0 to 5 (the
    welcome window's top stands at row 5) — is plain
    black desktop again."""
    w, h, px = d
    for y in range(1 * 16, 5 * 16):
        for x in range(0, 6 * 16):
            o = (y * w + x) * 3
            if px[o] != 0 or px[o + 1] != 0 or px[o + 2] != 0:
                return False
    return True


def bar_clock_standing(d):
    """White figure pixels stand at the bar's right
    end — the date and the clock, still telling time."""
    n = 0
    for y in range(0, 16):
        for x in range(54 * 16, 64 * 16):
            if pixel(d, x, y) == WHITE:
                n += 1
    return n > 20


# The menu's place on this face (1024x768, sixty-four
# cells across): left cell 0, top row 1, its choices at
# its left + 1, one to a row. The files window opens
# where its measures have always reckoned: left cell
# 5, top row 32, its title at its left + 1, its heading
# at its top + 2, its left + 2. The welcome window's
# title stands at row 5, cell 7.
ML, MT = 0, 1
FX, FY = 5, 32
CHOICES = ("Welcome", "Feather", "Files", "Settings", "Editor")

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

# The pointer's point starts at (506, 378). A move of
# (-306, -370) lays it at (200, 8): on the top bar, in
# its first row, away from the bar's name and its
# clock. The press opens the menu.
mousemove(-306, -370)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, MT + 2, ML + 1, "Files", WHITE) == "Files", 25)
expect(d is not None, "a press on the bar opened the menu")
if d:
    for i, word in enumerate(CHOICES):
        said = decode(d, MT + i, ML + 1, word, WHITE)
        expect(said == word,
               f"the menu's choice {i + 1} reads {word!r} (read: {said!r})")

# A press on the Files choice: the pointer's point
# stands at (200, 8); a move of (-160, +48) lays it at
# (40, 56), on the menu's third row. The files window
# opens, as the typed word opens it.
mousemove(-160, 48)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, FY, FX + 1, "Files", WHITE) == "Files", 25)
expect(d is not None, "a press on the menu's Files choice opened the files window")
if d:
    said = decode(d, FY + 2, FX + 2, "There is no disk fitted.", GRAY)
    expect(said == "There is no disk fitted.",
           f"the files window's heading stands as the typed word leaves it (read: {said!r})")
    expect(pixel(d, 200, FY * 16 + 8) == BLUE,
           "the files window stands forward, its title bar blue")

# Escape closes the files window, as it always has —
# the menu is not open, so the key is the window's.
sendkey("esc")
d = waitdump(lambda d: d is not None
             and pixel(d, 200, FY * 16 + 8) == BLACK, 15)
expect(d is not None, "Escape closed the files window")

# The menu opens again, and a press on the plain
# desktop elsewhere puts it away without opening
# anything. The pointer's point stands at (40, 56); a
# move of (+160, -48) lays it back on the bar at
# (200, 8), and the press opens the menu again.
mousemove(160, -48)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, MT + 4, ML + 1, "Editor", WHITE) == "Editor", 25)
expect(d is not None, "the menu opened again from the bar")
# A move of (+700, +592) lays the point at (900, 600):
# plain desktop, on no window and no word. The press
# there dismisses the menu, and nothing else.
mousemove(700, 592)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None and menu_ground_clean(d), 15)
expect(d is not None, "a press elsewhere put the menu away, its ground plain desktop again")
if d:
    expect(pixel(d, 200, FY * 16 + 8) == BLACK,
           "the dismissing press opened no window (the files window stayed closed)")
    said = decode(d, 5, 7, "Welcome", WHITE)
    expect(said == "Welcome",
           f"the desktop stands whole, the welcome window's title intact (read: {said!r})")

# The typed word for the same window still works,
# exactly as before.
typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, FY, FX + 1, "Files", WHITE) == "Files", 25)
expect(d is not None, "the typed word 'files' opened the files window again")

# The menu opens once more, and Escape puts the MENU
# away — not the window: the files window's title must
# still decode after the key. The pointer's point
# stands at (900, 600); a move of (-700, -592) lays it
# back on the bar at (200, 8).
mousemove(-700, -592)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, MT + 3, ML + 1, "Settings", WHITE) == "Settings", 25)
expect(d is not None, "the menu opened a third time from the bar")
sendkey("esc")
d = waitdump(lambda d: d is not None
             and pixel(d, 0, 24) == BLACK
             and decode(d, FY, FX + 1, "Files", WHITE) == "Files", 15)
expect(d is not None, "Escape put the menu away and closed no window")
if d:
    expect(bar_clock_standing(d),
           "the bar's clock still stands at the bar's right end")

done()
