# Stone 29 proof, boot 1: the verse window, opened by
# its word, with no disk fitted. The bench clock stands
# pinned at 2026-11-15T00:00:00 on the world's standard
# time (prove-stone29.sh), and the disc's choice is
# Eastern, so the date the desktop shows is November
# 14, 2026 — a count of 20,771 days since New Year's
# Day 1970, and 20,771 taken around the kept set of
# twelve verses stands at the twelfth: 1 John 5:13,
# whose words must stand in the window whole, wrapped
# at the window's width (fifty letters), DECODED letter
# by letter against the system's own letter shapes and
# joined back into the verse's exact World English
# Bible wording, with its reference under it.
#
# Tab then brings the welcome window forward (the verse
# window's bar goes quiet), the word 'verse' brings the
# verse window forward again, Escape closes it, the
# bar's menu — its seven choices decoded, Verse the
# sixth window choice and Rest last — opens it again
# by a press on the Verse choice, and a press on its
# close mark closes it.

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


def wrap(text, width):
    """The window painter's own wrapping reckoning: a
    line holds at most 'width' letters, broken at a
    space, exactly as pixprintline wraps."""
    lines = []
    start = 0
    n = len(text)
    while start < n:
        end = start + width
        if end >= n:
            end = n
        else:
            j = end
            while j > start and text[j] != " ":
                j -= 1
            if j > start:
                end = j
        lines.append(text[start:end])
        start = end
        if start < n and text[start] == " ":
            start += 1
    return lines


VERSE = ("These things I have written to you who believe in the "
         "name of the Son of God, that you may know that you have "
         "eternal life, and that you may continue to believe in "
         "the name of the Son of God.")
REF = "1 John 5:13"

# The verse window's place on this face (1024x768,
# sixty-four cells across): left cell 5, top row 32 —
# centered, at the layout's row 17, like the files
# window's — fifty-four wide, twelve high, its verse
# at its left + 2, wrapped at fifty letters, its
# reference at its top + 10.
VX, VY = 5, 32
LINES = wrap(VERSE, 50)

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

# The word 'verse' opens the window, with the day's
# verse standing in it.
typewrite("verse")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, VY, VX + 1, "Verse", WHITE) == "Verse", 25)
expect(d is not None, "the word 'verse' opened the verse window")
if d:
    expect(pixel(d, 200, VY * 16 + 8) == BLUE,
           "the verse window stands forward, its title bar blue")
    joined = []
    for i, line in enumerate(LINES):
        said = decode(d, VY + 2 + i, VX + 2, line, BLACK)
        expect(said == line,
               f"the verse's line {i + 1} reads exactly (read: {said!r})")
        joined.append(said)
    expect(" ".join(joined) == VERSE,
           "the wrapped lines join back into the verse's exact WEB wording")
    said = decode(d, VY + 10, VX + 2, REF, BLACK)
    expect(said == REF,
           f"the verse's reference stands plainly under it (read: {said!r})")

# Tab brings the welcome window forward, and the verse
# window's bar goes quiet behind it. (The welcome
# window's bar is read at x=700 — clear of its title's
# own white letters, which stand at its left.)
sendkey("tab")
d = waitdump(lambda d: d is not None
             and pixel(d, 700, 5 * 16 + 8) == BLUE
             and pixel(d, 200, VY * 16 + 8) == DARK, 15)
expect(d is not None, "Tab brought the welcome window forward, the verse window behind")

# The word again, and the window stands forward again.
typewrite("verse")
enter()
d = waitdump(lambda d: d is not None
             and pixel(d, 200, VY * 16 + 8) == BLUE
             and decode(d, VY + 10, VX + 2, REF, BLACK) == REF, 25)
expect(d is not None, "the word 'verse' brought the window forward again, its verse standing")

# Escape closes it back to the desktop.
sendkey("esc")
d = waitdump(lambda d: d is not None
             and pixel(d, 200, VY * 16 + 8) == BLACK, 15)
expect(d is not None, "Escape closed the verse window")

# The bar's menu: a press on the bar opens it, its
# seven choices decoded — the six windows' names and
# Rest last. The pointer's point starts at (506, 378);
# a move of (-306, -370) lays it at (200, 8), on the bar.
mousemove(-306, -370)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, 6, 1, "Verse", WHITE) == "Verse", 25)
expect(d is not None, "a press on the bar opened the menu, with Verse standing in it")
if d:
    for i, word in enumerate(("Welcome", "Feather", "Files", "Settings",
                              "Editor", "Verse", "Rest")):
        said = decode(d, 1 + i, 1, word, WHITE)
        expect(said == word,
               f"the menu's choice {i + 1} reads {word!r} (read: {said!r})")

# A press on the Verse choice opens the window again,
# exactly as the typed word does. The point stands at
# (200, 8); a move of (-160, +96) lays it at (40, 104),
# on the menu's sixth row.
mousemove(-160, 96)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, VY, VX + 1, "Verse", WHITE) == "Verse"
             and decode(d, VY + 10, VX + 2, REF, BLACK) == REF, 25)
expect(d is not None, "a press on the menu's Verse choice opened the verse window")

# A press on its close mark closes it. The point
# stands at (40, 104); two moves of (+440, +208) lay
# it at (920, 520), on the close mark's cell (one
# great move of (+880, +416) saturates the pointer's
# reckoning on the bench and falls short — measured
# on the bench while this proof was made).
mousemove(440, 208)
mousemove(440, 208)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and pixel(d, 200, VY * 16 + 8) == BLACK, 15)
expect(d is not None, "a press on the verse window's close mark closed it")

done()
