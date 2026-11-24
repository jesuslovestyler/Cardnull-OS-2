# Stone 41 proof, boot 2: the Bible reading window's
# other two roads in, with no disk fitted. The ninth
# desktop icon stands down the left edge — a blue book
# with a gold cross, its name 'Bible' beside its
# picture; of the name, the first letter stands clear
# of the terminal window that stands open at the
# rising over the rest (a window stands over the icons
# it covers, as on any desktop — Stone 38's proof
# reads the rising the same way), and the name whole
# is read on the window's own title bar once a press
# on its box opens it on its contents page, exactly
# as the typed word does; a press on the window's
# close mark closes it. The bar's menu — risen one
# row higher than Stone 31 left it, its ten choices
# decoded, Bible the ninth choice and Rest last —
# opens it by a press on the Bible choice, and
# Escape closes it.
#
# The window's place is boot 1's: left cell 5, top
# row 30, fifty-four wide, sixteen high. The ninth
# icon's box stands at rows 33 to 35 (the icons stand
# four rows apart from row 1), its name at row 34
# beside the picture. The menu rises from the bar at
# the screen's foot: ten rows from row 36, its choices
# one to a row from row 36, Bible on row 44.

import re

BLUE = (0, 0, 170)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# The palette's gold — the color the icons are painted
# in (palette color 14: the Files folder's gold, and
# the Bible cross's). The start button's cardinal
# carries a different gold of its own, (233, 178, 58),
# which Stone 33's proofs read; the cross is this one.
PALETTE_GOLD = (255, 255, 85)


def count_in(d, rgb, x0, y0, x1, y1):
    n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pixel(d, x, y) == rgb:
                n += 1
    return n

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


BX, BY = 5, 30

# The pointer's point, tracked as the bench moves it:
# it starts at the screen's middle (506, 378).
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


d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

# The ninth icon stands on the desktop: its picture
# clear, and the first letter of its name in the
# clear — the terminal window standing open at the
# rising covers the name's other letters, as it
# covers every icon name it stands over. The name
# whole is read on the opened window's title bar
# below.
d = waitdump(lambda d: d is not None
             and decode(d, 34, 4, "B", WHITE) == "B", 25)
expect(d is not None, "the Bible icon stands on the desktop, its name's first letter in the clear")
if d:
    expect(count_in(d, PALETTE_GOLD, 16, 33 * 16, 48, 36 * 16) > 5,
           "the icon's gold cross stands on the desktop")

# A press on the icon's box opens the window on its
# contents page. The box's center stands at (40, 552).
click(40, 552)
d = waitdump(lambda d: d is not None
             and decode(d, BY, BX + 1, "Bible", WHITE) == "Bible"
             and decode(d, BY + 14, BX + 8, "Page 1 of 30", BLACK) == "Page 1 of 30", 25)
expect(d is not None, "a press on the Bible icon opened the window on its contents page")

# A press on its close mark closes it. The mark's cell
# stands at the window's top right — cell column
# left + width - 2 = 57, pixels 912 to 928, so its
# center stands at (920, 488).
click(920, 488)
d = waitdump(lambda d: d is not None
             and pixel(d, 200, BY * 16 + 8) == BLACK, 15)
expect(d is not None, "a press on the Bible window's close mark closed it")

# The menu: a press on the start button opens it, its
# ten choices decoded — the nine windows' names with
# Bible the ninth choice, and Rest last.
click(16, 752)
d = waitdump(lambda d: d is not None
             and decode(d, 44, 1, "Bible", WHITE) == "Bible", 25)
expect(d is not None, "a press on the start button opened the menu, with Bible standing in it")
if d:
    for i, word in enumerate(("Welcome", "Feather", "Files", "Settings",
                              "Editor", "Verse", "Calculator", "Help",
                              "Bible", "Rest")):
        said = decode(d, 36 + i, 1, word, WHITE)
        expect(said == word,
               f"the menu's choice {i + 1} reads {word!r} (read: {said!r})")

# A press on the Bible choice opens the window again,
# exactly as the typed word does. The choice's row
# stands at (40, 712).
click(40, 712)
d = waitdump(lambda d: d is not None
             and decode(d, BY, BX + 1, "Bible", WHITE) == "Bible"
             and decode(d, BY + 3, BX + 2, "One whole book stands here:", BLACK) == "One whole book stands here:", 25)
expect(d is not None, "a press on the menu's Bible choice opened the window on its contents page")

# Escape closes it back to the desktop.
sendkey("esc")
d = waitdump(lambda d: d is not None
             and pixel(d, 200, BY * 16 + 8) == BLACK, 15)
expect(d is not None, "Escape closed the Bible window")

done()
