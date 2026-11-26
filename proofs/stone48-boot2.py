# Stone 48 proof, boot 2: the picture window with no
# picture kept, its place in the bar's menu, and its
# chip. No disk is fitted, so no picture can stand
# kept. The word 'picture' opens the window all the
# same, and its body says in plain words — DECODED
# against the system's own letter shapes — that no
# picture stands kept yet, and how one comes to stand
# there. Escape closes it. The bar's menu — risen one
# row higher for its fourteen choices, all DECODED:
# the thirteen windows' names with Picture the
# thirteenth choice, standing after Shield in the
# append-before-Rest place the newest window's choice
# has always taken, and Rest last — opens it again by
# a press on the Picture choice. With the files
# window forward the picture window's title bar
# stands in its behind gray, and a press on its chip
# on the bar raises it, its bar blue again.

import re

BLUE = (0, 0, 170)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FRAME = (85, 85, 85)
LIGHT = (170, 170, 170)

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


# The picture window's place (1024x768, sixty-four
# cells across): fifty wide and sixteen high,
# centered — its left at cell 7, its top clamped to
# row 30 so it stands whole above the bar. Its title
# stands at its top row, one cell in; its lines two
# cells in.
PX, PY = 7, 30

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

typewrite("picture")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, PY, PX + 1, "Picture", WHITE) == "Picture", 25)
expect(d is not None, "the word 'picture' opened the picture window")
if d:
    for row, line in ((PY + 2, "No picture stands kept yet."),
                      (PY + 4, "Paint one in the paint window and keep it,"),
                      (PY + 5, "and it will stand here, big, to look at.")):
        said = decode(d, row, PX + 2, line, BLACK)
        expect(said == line,
               f"the empty window's line reads exactly (read: {said!r})")

sendkey("esc")
d = waitdump(lambda d: d is not None
             and decode(d, PY, PX + 1, "Picture", WHITE) != "Picture", 15)
expect(d is not None, "Escape closed the picture window")

# The menu: a press on the start button opens it, its
# fourteen choices decoded — the thirteen windows'
# names in their standing order, Picture thirteenth
# and Rest last. The menu rises from the bar at the
# screen's foot: fourteen rows from row 32.
click(16, 752)
d = waitdump(lambda d: d is not None
             and decode(d, 44, 1, "Picture", WHITE) == "Picture", 25)
expect(d is not None, "a press on the start button opened the menu, with Picture standing in it")
if d:
    for i, word in enumerate(("Welcome", "Feather", "Files", "Editor",
                              "Paint", "Calculator", "Verse", "Help",
                              "Settings", "Terminal", "Bible", "Shield",
                              "Picture", "Rest")):
        said = decode(d, 32 + i, 1, word, WHITE)
        expect(said == word,
               f"the menu's choice {i + 1} reads {word!r} (read: {said!r})")

# A press on the Picture choice opens the window
# again, exactly as the typed word does. The choice's
# row stands at (40, 712).
click(40, 712)
d = waitdump(lambda d: d is not None
             and decode(d, PY, PX + 1, "Picture", WHITE) == "Picture", 25)
expect(d is not None, "a press on the menu's Picture choice opened the window")
if d:
    said = decode(d, PY + 2, PX + 2, "No picture stands kept yet.", BLACK)
    expect(said == "No picture stands kept yet.",
           f"the menu-opened window tells its plain words too (read: {said!r})")

# The chip: the files window comes forward (its word
# typed), and the picture window stands behind. Its
# title bar itself cannot be read for the gray here:
# since Stone 49 grew the files window by its
# exchange row, the files window's first place (top
# row 30, the picture window's own bar row) covers
# the picture window's bar whole while it stands
# forward. The desktop's other telling of the same
# standing is the window's chip on the bar — white
# on light gray while its window stands behind, as
# the bar's chips tell for every window (Stone 39's
# reckoning) — counted over the Picture chip's plate
# (the bar's upper row, from column 17).
typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and count_in(d, LIGHT, 17 * 16, 46 * 16, 27 * 16, 47 * 16)
             > count_in(d, BLUE, 17 * 16, 46 * 16, 27 * 16, 47 * 16), 25)
expect(d is not None, "with the files window forward, the picture window stands behind — its chip stands gray")
# The open windows' chips pack in the icons' order on
# the bar's upper row: Files at column 2, Terminal at
# column 8, Picture at column 17. A press on the
# Picture chip raises its window: the bar blue again.
click((17 + 2) * 16 + 8, 46 * 16 + 8)
d = waitdump(lambda d: d is not None
             and pixel(d, (PX + 20) * 16, PY * 16 + 8) == BLUE, 25)
expect(d is not None, "a press on the picture window's chip raised its window")

sendkey("esc")
d = waitdump(lambda d: d is not None
             and decode(d, PY, PX + 1, "Picture", WHITE) != "Picture", 15)
expect(d is not None, "Escape closed the picture window again")

done()
