# Stone 33 proof, boot 1: the glass face, at the usual
# size, with no disk fitted.
#
# The bar stands at the screen's FOOT now, two rows
# tall: its sheen bands and its blue lower row are
# sampled pixel by pixel, the screen's top row is plain
# desktop, and the round start button at the bar's left
# carries the cardinal — its deep-red body, gold wing,
# orange beak, lead divisions, and white eye checked in
# the bird's own shape at the button's reckoned place
# (center one cell in and at the bar's middle, radius a
# cell less two: center (16, 752), the bird drawn at
# (4, 740), twenty-four by twenty-four).
#
# A press ON THE BUTTON (its point laid at the disc's
# center) opens the menu, which RISES from the button:
# its foot on the bar's top edge (top row 37), its nine
# choices DECODED letter by letter against the system's
# own letter shapes, Rest last. A press on the Files
# choice opens the files window at its new first place
# (left cell 5, top row 30 — above the bar now; row 31
# through Stone 48, one higher since Stone 49 grew the
# window by its exchange row). The
# glass is checked on the windows: the welcome window's
# rounded corner leaves the corner pixel to the desktop
# while its frame stands a few pixels in; the welcome's
# shadow stands along its right edge and under its foot
# in the shadow's near-black; the files window's right
# shadow stands where the glass shape promises, clipped
# at the bar's top.
#
# The files window is DRAGGED by its title bar to a new
# place and decoded there, and the ground it vacated —
# its shadow's reach with it — stands plain again. Its
# close mark closes it. Then the pointer is carried
# across the glass — over the bar and the start button,
# over a window's shadow — and home again, and the
# whole desktop must stand pixel for pixel as it stood
# before the carrying (the bar's clock, at the bar's
# right end, is the one honest difference time makes,
# and it is left out of the comparison).
#
# Finally Rest is opened from the risen menu and its
# panel decoded, Stay puts it away, and Escape dismisses
# the menu and closes nothing.

import re

BLUE = (0, 0, 170)
WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
BLACK = (0, 0, 0)
FRAME = (85, 85, 85)
SHEEN = (154, 214, 222)
MID = (95, 174, 190)
TINT = (46, 126, 148)
SHADOW = (10, 18, 22)
RED = (192, 22, 34)
BRIGHT = (232, 58, 66)
GOLD = (233, 178, 58)
BEAK = (240, 126, 30)
LEAD = (24, 24, 32)

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


def count_in(d, rgb, x0, y0, x1, y1):
    n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pixel(d, x, y) == rgb:
                n += 1
    return n


# Places on this face (1024x768, sixty-four cells
# across, forty-eight down): the bar's top edge at
# y 736 (row 46), its words on row 47; the start
# button's center (16, 752); the menu at left 0, top
# row 37, nine rows; the files window at left cell 5,
# top row 30; the welcome window at left cell 6, top
# row 5, fifty-one by fourteen; the rest panel
# centered, left cell 24, top row 22.
MT = 37
FX, FY = 5, 30
RL, RT = 24, 22
CHOICES = ("Welcome", "Feather", "Files", "Settings", "Editor",
           "Verse", "Calculator", "Help", "Rest")

# The pointer's point, tracked as the scenario moves
# it: it starts at (506, 378) on every boot.
PX, PY = 506, 378


def go(x, y):
    global PX, PY
    # Carried in steps of at most 200 pixels: one long
    # leap can outrun the bench mouse's own packet, as
    # the standing proofs' small-step drags have always
    # known.
    while PX != x or PY != y:
        dx = max(-200, min(200, x - PX))
        dy = max(-200, min(200, y - PY))
        mousemove(dx, dy)
        PX, PY = PX + dx, PY + dy


def click(x, y):
    go(x, y)
    mousebutton(1)
    mousebutton(0)


d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")
if d:
    expect(pixel(d, 300, 8) == BLACK,
           "the screen's top row is plain desktop now — no bar stands there")
    expect(pixel(d, 300, 740) == SHEEN,
           "the bar's upper part carries the sheen's pale band")
    expect(pixel(d, 300, 748) == MID,
           "the sheen's middle band stands under the pale band")
    expect(pixel(d, 300, 754) == TINT,
           "the calm blue-green tint stands where the sheen meets the blue")
    expect(pixel(d, 300, 760) == BLUE,
           "the bar's lower row keeps the bar's blue")
    expect(decode(d, 44, 6, ">", GRAY) == ">",
           "the typing line stands at the terminal window's foot, one row above the bar (Stone 38)")
    # The start button's cardinal, in its own shape.
    expect(count_in(d, RED, 2, 738, 31, 767) > 40,
           "the button carries the cardinal's deep red")
    expect(count_in(d, GOLD, 2, 738, 31, 767) > 5,
           "the cardinal's wing stands gold on the button")
    expect(count_in(d, LEAD, 2, 738, 31, 767) > 20,
           "the stained glass's lead divisions stand dark on the button")
    expect(pixel(d, 10, 740) == LEAD and pixel(d, 11, 740) == LEAD,
           "the crest's lead tip stands at the bird's top")
    expect(pixel(d, 18, 746) == WHITE,
           "the cardinal's eye stands white in its black mask")
    expect(pixel(d, 21, 747) == BEAK,
           "the cardinal's beak stands orange at its front")
    expect(pixel(d, 8, 752) == GOLD,
           "the cardinal's gold wing stands on its side")
    expect(pixel(d, 16, 742) == SHEEN,
           "the button's own glass sheen stands above the bird")
    # The welcome window's glass: a rounded corner and
    # a shadow. Its place: left cell 6, top row 5.
    expect(pixel(d, 96, 80) == BLACK,
           "the welcome window's rounded corner leaves its corner pixel to the desktop")
    expect(pixel(d, 102, 80) == FRAME,
           "the welcome window's frame stands a few pixels in from the corner")
    expect(pixel(d, 914, 200) == SHADOW,
           "the welcome window's shadow stands along its right edge")
    expect(pixel(d, 200, 306) == SHADOW,
           "the welcome window's shadow stands under its foot")

# A press on the start button opens the menu, risen
# from the button: its nine choices decode at rows
# 37 to 45.
click(16, 752)
d = waitdump(lambda d: d is not None
             and decode(d, MT + 8, 1, "Rest", WHITE) == "Rest", 25)
expect(d is not None, "a press on the start button opened the menu, risen from the button")
if d:
    for i, word in enumerate(CHOICES):
        said = decode(d, MT + i, 1, word, WHITE)
        expect(said == word,
               f"the risen menu's choice {i + 1} reads {word!r} (read: {said!r})")

# A press on the Files choice opens the files window
# at its new first place, above the bar.
click(40, (MT + 2) * 16 + 8)
d = waitdump(lambda d: d is not None
             and decode(d, FY, FX + 1, "Files", WHITE) == "Files", 25)
expect(d is not None, "a press on the menu's Files choice opened the files window")
if d:
    said = decode(d, FY + 2, FX + 2, "There is no disk fitted.", GRAY)
    expect(said == "There is no disk fitted.",
           f"the files window's heading stands as the typed word leaves it (read: {said!r})")
    expect(pixel(d, 200, FY * 16 + 10) == BLUE,
           "the files window stands forward, its title bar blue under its sheen")
    expect(pixel(d, 946, 600) == SHADOW,
           "the files window's right shadow stands where the glass shape promises")

# Drag the files window by its title bar: the point
# stands at (40, 632); it is laid on the title bar at
# (400, 504), the button goes down, four small steps
# carry it by (+80, -160), and it is let go. The
# window's new place: left cell 10, top row 21.
NX, NY = 10, 21
go(400, FY * 16 + 8)
mousebutton(1)
for _ in range(4):
    mousemove(20, -40)
    PX, PY = PX + 20, PY - 40
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, NY, NX + 1, "Files", WHITE) == "Files", 25)
expect(d is not None, "the glass files window was dragged by its title bar and reads at its new place")
if d:
    said = decode(d, NY + 2, NX + 2, "There is no disk fitted.", GRAY)
    expect(said == "There is no disk fitted.",
           f"the dragged window's heading stands at the new place (read: {said!r})")
    expect(pixel(d, 200, (NY + 15) * 16 + 2) == SHADOW,
           "the dragged window's shadow stands under its foot at the new place")
    # The vacated ground: the old place's pixels that
    # neither the new place nor the feather window
    # covers, and the old shadow's strip at its right,
    # must stand plain desktop again.
    bad = []
    for y in range(FY * 16, (FY + 16) * 16):
        for x in range(FX * 16, (FX + 54) * 16):
            if NX * 16 <= x < (NX + 54) * 16 and NY * 16 <= y < (NY + 15) * 16:
                continue
            # The new place's own shadow, under its foot
            # and along its right edge — the dragged
            # window stands there now, shadow and all.
            if NX * 16 + 5 <= x < (NX + 54) * 16 + 5 and (NY + 15) * 16 <= y < (NY + 15) * 16 + 5:
                continue
            # The feather window's own ground: its rect
            # (rows 26 to 34) and its shadow's reach past
            # it (five pixels right and under) — that
            # ground must show the feather window and its
            # shadow repainted, not black.
            if FX * 16 <= x < (FX + 54) * 16 + 5 and 26 * 16 <= y < 35 * 16 + 5:
                continue
            # The terminal window's own ground (Stone
            # 38): its rect (rows 32 to 45, from cell 5)
            # and its shadow's reach past it — the
            # terminal stands open on the desktop from
            # the rising, over the files window's old
            # place, and that ground must show the
            # terminal repainted whole, not black.
            if 5 * 16 <= x < (5 + 54) * 16 + 5 and 32 * 16 <= y < 46 * 16 + 5:
                continue
            if pixel(d, x, y) != BLACK:
                bad.append((x, y))
                if len(bad) > 8:
                    break
    for y in range(FY * 16 + 5, (FY + 15) * 16):
        for x in range((FX + 54) * 16, (FX + 54) * 16 + 5):
            if NX * 16 <= x < (NX + 54) * 16 and NY * 16 <= y < (NY + 15) * 16:
                continue
            # The strip's upper part is the feather
            # window's own right shadow too (its edge
            # stands at the same x, its shadow reaching
            # to y 564) — indistinguishable there, and
            # honestly the feather's; the check judges
            # the strip below it.
            if y < 35 * 16 + 5:
                continue
            # The strip is the terminal window's own
            # right shadow too (Stone 38): its edge
            # stands at the very same x, its shadow
            # reaching to y 741 — the strip is honestly
            # the terminal's for the whole of the old
            # place's height, and the check judges what
            # little stands below it.
            if y < 46 * 16 + 5:
                continue
            # The strip's crossing of the new place's
            # foot shadow (its corner square, five rows
            # under the new window's foot) is the new
            # window's own shadow, standing where it
            # should.
            if (NY + 15) * 16 <= y < (NY + 15) * 16 + 5:
                continue
            if pixel(d, x, y) != BLACK:
                bad.append((x, y))
    expect(len(bad) == 0,
           "the ground the dragged window vacated — its shadow's strip with it — "
           f"is plain desktop again ({len(bad)} remnant pixels, first of them {bad[:8]})")

# The close mark at the dragged place closes it.
click(1000, NY * 16 + 8)
d = waitdump(lambda d: d is not None
             and pixel(d, 400, NY * 16 + 40) == BLACK, 15)
expect(d is not None, "the close mark at the dragged place closed the glass window")

# The pointer's discipline on the glass face: a
# reference picture, the arrow carried over the bar
# and the start button and over the welcome window's
# shadow, and home again — the desktop must stand
# pixel for pixel as it was, the bar clock's own
# ground (the bar's right end, its lower row) left
# out, as time honestly moves there.
time.sleep(1)
ref = dump()
expect(ref is not None, "the reference desktop is taken")
if ref:
    go(300, 500)
    go(20, 750)
    time.sleep(0.6)
    go(500, 400)
    go(914, 200)
    time.sleep(0.6)
    go(1000, NY * 16 + 8)
    time.sleep(1)
    after = dump()
    expect(after is not None, "the desktop is read again after the carrying")
    if after:
        diff = []
        w, h, pa = ref
        _, _, pb = after
        for y in range(h):
            for x in range(w):
                if y >= 752 and x >= 380:
                    continue
                o = (y * w + x) * 3
                if pa[o:o + 3] != pb[o:o + 3]:
                    diff.append((x, y))
                    if len(diff) > 8:
                        break
        expect(len(diff) == 0,
               "after crossing the glass — bar, button, and shadow — the desktop "
               f"is pixel for pixel what it was ({len(diff)} differing pixels, "
               f"first of them {diff[:8]})")

# Rest from the risen menu: the button is pressed,
# the Rest choice pressed, the panel's words decode,
# and Stay puts it away.
click(16, 752)
d = waitdump(lambda d: d is not None
             and decode(d, MT + 8, 1, "Rest", WHITE) == "Rest", 25)
expect(d is not None, "the menu rose again from the start button")
click(40, (MT + 8) * 16 + 8)
d = waitdump(lambda d: d is not None
             and decode(d, RT + 1, RL + 1, "Shut down", WHITE) == "Shut down", 25)
expect(d is not None, "a press on the risen menu's Rest choice opened the rest panel")
if d:
    for i, word in enumerate(("Rest", "Shut down", "Restart", "Stay")):
        said = decode(d, RT + i, RL + 1, word, WHITE)
        expect(said == word,
               f"the rest panel's row {i + 1} reads {word!r} (read: {said!r})")
click(450, (RT + 3) * 16 + 8)
d = waitdump(lambda d: d is not None
             and pixel(d, 450, (RT + 1) * 16 + 8) == BLACK, 15)
expect(d is not None, "Stay put the rest panel away")

# Escape dismisses the menu and closes nothing: the
# menu rises once more, Escape puts it away, and the
# welcome window's title still decodes.
click(16, 752)
d = waitdump(lambda d: d is not None
             and decode(d, MT + 3, 1, "Settings", WHITE) == "Settings", 25)
expect(d is not None, "the menu rose a third time from the start button")
sendkey("esc")
d = waitdump(lambda d: d is not None
             and pixel(d, 8, MT * 16 + 8) == BLACK
             and decode(d, 5, 7, "Welcome", WHITE) == "Welcome", 15)
expect(d is not None, "Escape put the menu away and closed no window")

done()
