# Stone 31 proof, boot 1: the help window, opened by
# its word, with no disk fitted. The word 'help' opens
# the window with its first page standing in it; every
# page's eleven lines are DECODED letter by letter
# against the system's own letter shapes and compared
# against the kept help words in src/helpwords.nifla,
# page by page — the pages turned by the down arrow
# key and by presses on the window's foot (its More
# word, and First page on the last page, which returns
# to the first page) — with the foot's own standing
# ("Page 1 of 5" and its turning word) decoded on the
# pages where it changes. The up arrow on the first
# page turns nothing. Tab then brings the welcome
# window forward, the word 'help' brings the help
# window forward again, Escape closes it; the bar's
# menu — its nine choices decoded, Help the eighth
# window choice and Rest last — opens it by a press
# on the Help choice, and a press on its close mark
# closes it.
#
# The window's place on this face (1024x768, sixty-four
# cells across): left cell 5, top row 32 — centered, at
# the layout's row 17, like the files window's —
# fifty-four wide, sixteen high, its page's lines at
# its left + 2, its foot at its top + 14: the page's
# standing at its left + 2 and its turning word at its
# right (More at its left + 48, First page at its
# left + 42).

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


# The kept help words, page by page, exactly as
# src/helpwords.nifla keeps them.
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
    ("Words you can type",
     "Type a word, then press Enter.",
     "hello says hello back.",
     "time tells the time and date.",
     "memory tells the memory size.",
     "clear clears the screen.",
     "welcome opens Welcome.",
     "feather asks the feather in.",
     "files opens Files.",
     "settings opens Settings.",
     "editor opens Editor."),
    ("More words you can type",
     "paint opens Paint.",
     "verse opens Verse.",
     "calculator opens Calculator.",
     "help opens this Help window.",
     "note, then words, keeps a note.",
     "notes shows the kept notes.",
     "setup lets a disk remember.",
     "eastern sets Eastern time.",
     "utc sets the standard time.",
     "chime sounds the welcome again."),
    ("Moving and resting",
     "usb tells if a USB keyboard",
     "is plugged in and ready.",
     "The round button opens the menu.",
     "Tab brings the next window up.",
     "Escape closes the front window.",
     "The small x closes its window.",
     "Drag a title bar to move it.",
     "rest offers Shut down, Restart,",
     "and Stay. shutdown and restart",
     "name those two choices at once."),
)

HX, HY = 5, 30

# The pointer's point, tracked as the bench moves it:
# it starts at the screen's middle (506, 378).
CUR = [506, 378]


def move_to(x, y):
    mousemove(x - CUR[0], y - CUR[1])
    CUR[0], CUR[1] = x, y


def click(x, y):
    move_to(x, y)
    mousebutton(1)
    mousebutton(0)


def check_page(d, page):
    """Every line of the standing page decodes exactly,
    and its foot names the page."""
    for i, line in enumerate(PAGES[page]):
        said = decode(d, HY + 2 + i, HX + 2, line, BLACK)
        expect(said == line,
               f"page {page + 1}'s line {i + 1} reads exactly (read: {said!r})")
    foot = f"Page {page + 1} of 5"
    said = decode(d, HY + 14, HX + 2, foot, BLACK)
    expect(said == foot,
           f"the foot names the standing page {foot!r} (read: {said!r})")


d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

# The word 'help' opens the window, its first page in it.
typewrite("help")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, HY, HX + 1, "Help", WHITE) == "Help", 25)
expect(d is not None, "the word 'help' opened the help window")
if d:
    expect(pixel(d, 200, HY * 16 + 8) == BLUE,
           "the help window stands forward, its title bar blue")
    check_page(d, 0)
    said = decode(d, HY + 14, HX + 48, "More", WHITE)
    expect(said == "More",
           f"the foot's turning word reads 'More' (read: {said!r})")

# The down arrow turns to the second page.
sendkey("down")
d = waitdump(lambda d: d is not None
             and decode(d, HY + 14, HX + 2, "Page 2 of 5", BLACK) == "Page 2 of 5", 15)
expect(d is not None, "the down arrow turned to the second page")
if d:
    check_page(d, 1)

# A press on the foot's More word turns to the third
# page. The point stands at (506, 378); the More word's
# cells stand at the foot's right — its center (856,
# 712) — walked in two moves, as the close-mark walks
# in the other proofs walk (one great move saturates
# the pointer's reckoning on the bench).
mousemove(175, 167)
mousemove(175, 167)
CUR[0], CUR[1] = 856, 712
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, HY + 14, HX + 2, "Page 3 of 5", BLACK) == "Page 3 of 5", 15)
expect(d is not None, "a press on the foot's More word turned to the third page")
if d:
    check_page(d, 2)

# The down arrow turns to the fourth page.
sendkey("down")
d = waitdump(lambda d: d is not None
             and decode(d, HY + 14, HX + 2, "Page 4 of 5", BLACK) == "Page 4 of 5", 15)
expect(d is not None, "the down arrow turned to the fourth page")
if d:
    check_page(d, 3)

# A press on More turns to the fifth page, whose foot
# offers the way back: First page. The point stands on
# the More word already.
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, HY + 14, HX + 2, "Page 5 of 5", BLACK) == "Page 5 of 5", 15)
expect(d is not None, "a press on More turned to the fifth page")
if d:
    check_page(d, 4)
    # The arrow stands where the More press left it —
    # on the foot's own right end, over the turning
    # word's letters — so it is parked at the desktop's
    # corner before the word is read, as the other
    # proofs park it before a reading.
    mousemove(-398, -326)
    mousemove(-398, -326)
    CUR[0], CUR[1] = 60, 60
    d = dump()
    said = decode(d, HY + 14, HX + 42, "First page", WHITE)
    expect(said == "First page",
           f"the last page's foot offers 'First page' (read: {said!r})")

# A press on First page returns to the first page: the
# point walks from its park to that word's center
# (760, 712), in two moves as before.
mousemove(350, 326)
mousemove(350, 326)
CUR[0], CUR[1] = 760, 712
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, HY + 14, HX + 2, "Page 1 of 5", BLACK) == "Page 1 of 5", 15)
expect(d is not None, "a press on First page returned to the first page")
if d:
    said = decode(d, HY + 2, HX + 2, PAGES[0][0], BLACK)
    expect(said == PAGES[0][0],
           f"the first page stands again (read: {said!r})")

# The up arrow on the first page turns nothing.
sendkey("up")
time.sleep(0.6)
d = dump()
if d:
    said = decode(d, HY + 14, HX + 2, "Page 1 of 5", BLACK)
    expect(said == "Page 1 of 5",
           f"the up arrow on the first page turned nothing (read: {said!r})")

# Tab brings the next open window forward (Stone
# 38: the cycle holds ten windows now — the terminal
# stands open from the rising, after the help window
# in the cycle's order — so the first Tab brings the
# terminal forward, and the second brings the
# welcome window forward, the help window's bar
# going quiet behind it. (The welcome window's bar
# is read at x=700 — clear of its title's own white
# letters, which stand at its left.)
sendkey("tab")
d = waitdump(lambda d: d is not None
             and decode(d, 32, 6, "Terminal", WHITE) == "Terminal"
             and pixel(d, 300, 32 * 16 + 8) == BLUE, 15)
expect(d is not None, "Tab brought the terminal window forward, the help window behind")
sendkey("tab")
d = waitdump(lambda d: d is not None
             and pixel(d, 700, 5 * 16 + 8) == BLUE
             and pixel(d, 200, HY * 16 + 8) == DARK, 15)
expect(d is not None, "Tab brought the welcome window forward, the help window behind")

# The word again, and the window stands forward again.
typewrite("help")
enter()
d = waitdump(lambda d: d is not None
             and pixel(d, 200, HY * 16 + 8) == BLUE
             and decode(d, HY + 14, HX + 2, "Page 1 of 5", BLACK) == "Page 1 of 5", 25)
expect(d is not None, "the word 'help' brought the window forward again, its first page standing")

# Escape closes it back to the desktop.
sendkey("esc")
d = waitdump(lambda d: d is not None
             and pixel(d, 200, HY * 16 + 8) == BLACK, 15)
expect(d is not None, "Escape closed the help window")

# The menu: a press on the start button opens it,
# risen from the bar at the screen's foot, its nine
# choices decoded — the eight windows' names, Help the
# eighth, and Rest last. The point stands at (760, 712);
# two moves lay it at (16, 752), the button's center.
mousemove(-372, 20)
mousemove(-372, 20)
CUR[0], CUR[1] = 16, 752
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, 44, 1, "Help", WHITE) == "Help", 25)
expect(d is not None, "a press on the start button opened the menu, with Help standing in it")
if d:
    for i, word in enumerate(("Welcome", "Feather", "Files", "Settings",
                              "Editor", "Verse", "Calculator", "Help", "Rest")):
        said = decode(d, 37 + i, 1, word, WHITE)
        expect(said == word,
               f"the menu's choice {i + 1} reads {word!r} (read: {said!r})")

# A press on the Help choice opens the window again,
# exactly as the typed word does. The point stands at
# (16, 752); a move of (+24, -40) lays it at (40, 712),
# on the menu's eighth row.
mousemove(24, -40)
CUR[0], CUR[1] = 40, 712
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, HY, HX + 1, "Help", WHITE) == "Help"
             and decode(d, HY + 2, HX + 2, PAGES[0][0], BLACK) == PAGES[0][0], 25)
expect(d is not None, "a press on the menu's Help choice opened the help window")

# A press on its close mark closes it. The point stands
# at (40, 712); two moves lay it at (920, 488), on the
# close mark's cell.
mousemove(440, -112)
mousemove(440, -112)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and pixel(d, 200, HY * 16 + 8) == BLACK, 15)
expect(d is not None, "a press on the help window's close mark closed it")

done()
