# Stone 31 proof, boot 2: the help window at the
# LARGE size, with no disk fitted. The settings
# window's Large row is pressed first (its point at
# (168, 712), as in Stone 28's boots), Escape closes
# the settings window, and the word 'help' opens the
# help window on the narrow large face (forty-two
# cells across): left cell 1, top row 16 — the
# layout's row 17 held up so the sixteen-high window
# stands whole — forty wide, sixteen high. The first
# page's lines must stand in it whole, DECODED letter
# by letter at the large scale — every line at most
# thirty-six letters, the window's inner width at
# this size, so none is cut at the window's edge —
# its foot decoded too; the down arrow turns to the
# second page, decoded the same way, and Escape
# closes the window.

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


# The kept help words' first two pages, exactly as
# src/helpwords.nifla keeps them (boot 1 decodes all
# five pages at the usual size).
PAGES = (
    ("The windows",
     "Welcome greets you. It tells what",
     "Cardnull is and its verse.",
     "Feather shows a small program",
     "that visits. It is checked first.",
     "Files lists your kept notes,",
     "and a kept picture.",
     "Settings sets the time zone,",
     "the chime, and the word size.",
     "Editor is where a note is",
     "written and changed."),
    ("More windows",
     "Paint is for drawing. Pick a",
     "color, then draw on the canvas.",
     "Verse shows the verse for the",
     "day, in the World English Bible.",
     "Calculator reckons sums. Press",
     "its keys to reckon a sum.",
     "Help is this window. It tells",
     "how Cardnull works, plainly.",
     "Press More below to turn the",
     "page. Arrow keys turn it too."),
)

PX, PY = 506, 378


def click(x, y):
    global PX, PY
    mousemove(x - PX, y - PY)
    PX, PY = x, y
    mousebutton(1)
    mousebutton(0)


# The settings window's place at the usual size, and
# at the large size after the press, as in Stone 28.
UX, UY = 5, 32
LX, LY = 1, 16
# The help window's place at the large size: left
# cell 1, top row 16, forty wide, sixteen high, its
# page's lines at its left + 2, its foot at its
# top + 14 — its turning word at its left + 34.
HX, HY = 1, 16


def check_page(d, page):
    for i, line in enumerate(PAGES[page]):
        said = decode(d, HY + 2 + i, HX + 2, line, BLACK, 3)
        expect(said == line,
               f"page {page + 1}'s large line {i + 1} reads exactly (read: {said!r})")
    foot = f"Page {page + 1} of 5"
    said = decode(d, HY + 14, HX + 2, foot, BLACK, 3)
    expect(said == foot,
           f"the foot names the standing page {foot!r}, large (read: {said!r})")


d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

typewrite("settings")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, UY, UX + 1, "Settings", WHITE, 2) == "Settings", 25)
expect(d is not None, "the settings window opened at the usual size")

click(168, 712)
d = waitdump(lambda d: d is not None
             and decode(d, LY + 12, LX + 4, "Large", WHITE, 3) == "Large", 25)
expect(d is not None, "a press on the Large row stood the words large")

sendkey("esc")
d = waitdump(lambda d: d is not None
             and pixel(d, 100, LY * 24 + 12) == BLACK, 15)
expect(d is not None, "Escape closed the settings window")

# The word 'help', on the large face: the window stands
# at its large place, its first page whole in it. The
# pointer is first moved up to the face's top left, off
# the window's words — left where the Large press put
# it, it would rest on the page's own letters and spoil
# their decoding.
mousemove(-54, -326)
mousemove(-54, -326)
typewrite("help")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, HY, HX + 1, "Help", WHITE, 3) == "Help", 25)
expect(d is not None, "the word 'help' opened the help window at the large size")
if d:
    expect(pixel(d, 600, HY * 24 + 12) == BLUE,
           "the help window stands forward at the large size, its title bar blue")
    check_page(d, 0)
    said = decode(d, HY + 14, HX + 34, "More", WHITE, 3)
    expect(said == "More",
           f"the foot's turning word reads 'More', large (read: {said!r})")

# The down arrow turns to the second page, whole too.
sendkey("down")
d = waitdump(lambda d: d is not None
             and decode(d, HY + 14, HX + 2, "Page 2 of 5", BLACK, 3) == "Page 2 of 5", 15)
expect(d is not None, "the down arrow turned to the second page at the large size")
if d:
    check_page(d, 1)

sendkey("esc")
d = waitdump(lambda d: d is not None
             and pixel(d, 100, HY * 24 + 12) == BLACK, 15)
expect(d is not None, "Escape closed the help window at the large size")

done()
