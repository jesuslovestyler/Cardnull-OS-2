# Stone 33 proof, boot 2: the glass face at LARGE
# print, from a fitted keeping disk whose settings
# card carries the size byte 2 (large) — the desktop
# rises large, as Stone 28 lays it.
#
# The grid is forty-two cells across and thirty-two
# down (twenty-four-pixel cells). The bar stands at
# its foot, two large rows tall (its top edge at
# y 720): the sheen's pale band and the blue lower row
# are sampled, and the round start button — center one
# large cell in and at the bar's middle, (24, 744),
# radius twenty-two — carries the cardinal still: its
# deep red, gold, and lead checked in the button's
# region, the bird drawn at (12, 732) at the same
# twenty-four-pixel measure it stands at the usual
# size (the button grows; the bird's drawing is the
# one drawing).
#
# A press on the button opens the menu risen from it
# (top row 21 at this size), its nine choices DECODED
# letter by letter at the large scale, and a press on
# the Files choice opens the files window at its large
# first place (left cell 1, top row 15 — above the bar
# on the narrow grid), its title decoded large.

import re

BLUE = (0, 0, 170)
WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
BLACK = (0, 0, 0)
SHEEN = (154, 214, 222)
RED = (192, 22, 34)
GOLD = (233, 178, 58)
LEAD = (24, 24, 32)
BEAK = (240, 126, 30)

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


def count_in(d, rgb, x0, y0, x1, y1):
    n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pixel(d, x, y) == rgb:
                n += 1
    return n


# Places at the large size: the menu at left 0, top
# row 21 (thirty-two rows less the bar's two and its
# own nine); the files window at left cell 1, top
# row 15, forty large cells wide.
MT = 21
FX, FY = 1, 15
CHOICES = ("Welcome", "Feather", "Files", "Settings", "Editor",
           "Verse", "Calculator", "Help", "Rest")

PX, PY = 506, 378


def click(x, y):
    global PX, PY
    mousemove(x - PX, y - PY)
    PX, PY = x, y
    mousebutton(1)
    mousebutton(0)


d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn large")
if d:
    expect(pixel(d, 300, 8) == BLACK,
           "the screen's top row is plain desktop at the large size too")
    expect(pixel(d, 300, 726) == SHEEN,
           "the large bar's upper part carries the sheen's pale band")
    expect(pixel(d, 300, 760) == BLUE,
           "the large bar's lower row keeps the bar's blue")
    expect(count_in(d, RED, 2, 722, 47, 767) > 40,
           "the large start button carries the cardinal's deep red")
    expect(count_in(d, GOLD, 2, 722, 47, 767) > 5,
           "the large button's cardinal stands gold on its wing")
    expect(count_in(d, LEAD, 2, 722, 47, 767) > 20,
           "the large button's stained glass stands leaded")
    expect(pixel(d, 18, 732) == LEAD,
           "the crest's lead tip stands at the large bird's top")
    expect(pixel(d, 33, 739) == BEAK,
           "the large cardinal's beak stands orange at its front")

# A press on the large start button: the menu rises,
# its nine choices decoded at the large scale.
click(24, 744)
d = waitdump(lambda d: d is not None
             and decode(d, MT + 8, 1, "Rest", WHITE, 3) == "Rest", 25)
expect(d is not None, "a press on the large start button opened the risen menu")
if d:
    for i, word in enumerate(CHOICES):
        said = decode(d, MT + i, 1, word, WHITE, 3)
        expect(said == word,
               f"the risen menu's choice {i + 1} reads {word!r} large (read: {said!r})")

# The Files choice opens the files window at its
# large first place, above the bar.
click(48, (MT + 2) * 24 + 12)
d = waitdump(lambda d: d is not None
             and decode(d, FY, FX + 1, "Files", WHITE, 3) == "Files", 25)
expect(d is not None, "a press on the menu's Files choice opened the files window large")
if d:
    said = decode(d, FY + 2, FX + 2, "No notes are kept on the disk yet.", GRAY, 3)
    expect(said == "No notes are kept on the disk yet.",
           f"the large files window's heading stands (read: {said!r})")

done()
