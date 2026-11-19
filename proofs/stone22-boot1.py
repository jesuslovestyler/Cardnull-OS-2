# Stone 22 proof, boot 1: window dragging, with a fitted
# keeping disk prepared with two known notes (the CNN3
# store laid directly, as prove-stone19.sh lays it: the
# settings card on sector 8, the notes header on sector
# 64, one sector to a note from sector 65).
#
# The word 'files' opens the files window at the place
# its measures have always reckoned (left cell 5, top
# row 32 on this face), and its rendered list is DECODED
# letter by letter against the system's own letter
# shapes (parsed from src/font.nifla, the way
# prove-featherpaint.sh reads). The pointer is then laid
# on the window's title bar, the button pressed, and the
# pointer carried — button held, in small steps, the
# motion of a hand dragging — up and to the right by
# five cells across and ten rows up. The button is let
# go, and the window must now render at the new place
# (left cell 10, top row 22): its title and its list are
# decoded THERE, letter by letter. The ground the window
# stood on must stand plain black desktop again — every
# pixel of the old place that the new place does not
# cover is compared, the way prove-pointertrail.sh
# compares the whole desktop. A press on the second
# note's row IN THE DRAGGED WINDOW must pick that note
# (the shared geometry reckoning: the press is reckoned
# from the same place the painter painted), and a press
# on the dragged window's close mark must close it.

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


def old_place_remnants(d):
    """Pixels of the window's first place that are not
    plain black desktop, leaving out the ground that is
    another window's own: the part its new place covers,
    and the part the feather window covers (it stands
    open behind, at left cell 5, top row 26, fifty-four
    by nine — its foot overlaps the files window's first
    place, and that ground must show the feather window
    repainted, not black) — and, since Stone 33, the
    feather window's shadow's reach past its foot and
    right edge (five pixels, at y 560 to 564 here),
    which is the feather's own ground too. The arrow
    stands at the new place, inside the new rect, so it
    never falls in the part compared here. (Stone 38:
    the terminal window's own ground is left out the
    same way — it stands open behind at left cell 5,
    top row 32, fifty-four by fourteen, over the files
    window's first place, and that ground must show
    the terminal repainted, not black — with its
    shadow's reach past its foot and right edge.)"""
    w, h, px = d
    bad = []
    for y in range(GY * 16, (GY + 15) * 16):
        for x in range(GX * 16, (GX + 54) * 16):
            if NX * 16 <= x < (NX + 54) * 16 + 5 and NY * 16 <= y < (NY + 15) * 16 + 5:
                continue
            if GX * 16 <= x < (GX + 54) * 16 + 5 and 26 * 16 <= y < 35 * 16 + 5:
                continue
            if GX * 16 <= x < (GX + 54) * 16 + 5 and 32 * 16 <= y < 46 * 16 + 5:
                continue
            o = (y * w + x) * 3
            if px[o] != 0 or px[o + 1] != 0 or px[o + 2] != 0:
                bad.append((x, y))
                if len(bad) > 8:
                    return bad
    return bad


# The files window's places on this face (1024x768,
# sixty-four cells across): fifty-four wide, fifteen
# high (fourteen until Stone 26 grew it by the kept
# picture's row). It opens centered at the desktop's foot — left
# cell 5, top row 31 (top row 32 until Stone 33, whose
# bar at the screen's foot rose the taller windows'
# first places) — and the drag carries it to left
# cell 10 (the rightmost place it wholly fits: 10 + 54
# is the face's 64) and top row 21. Its list stands at
# its top + 3 (the first note) and + 4 (the second),
# their words at its left + 4; the picked note's words
# stand again at its top + 12, at its left + 2.
GX, GY = 5, 31
NX, NY = 10, 21
FIRST = "remember the garden"
SECOND = "pray for mother"

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY, GX + 1, "Files", WHITE) == "Files", 25)
expect(d is not None, "the word 'files' opened the files window at its first place")
if d:
    said = decode(d, GY + 3, GX + 4, FIRST, WHITE)
    expect(said == FIRST,
           f"the first note stands picked at the first place (read: {said!r})")
    said = decode(d, GY + 4, GX + 4, SECOND, GRAY)
    expect(said == SECOND,
           f"the second note stands listed at the first place (read: {said!r})")

# The pointer's point starts at (506, 378). A move of
# (-106, +126) lays its point at (400, 504): on the
# window's title bar (row 31, spanning the window's
# width), well away from the close mark at its right
# end. The button goes down there — the drag begins.
mousemove(-106, 126)
mousebutton(1)
# The drag itself: four small steps, the button held
# throughout, carrying the point by (+80, -160) in all
# — five cells across, ten rows up.
for _ in range(4):
    mousemove(20, -40)
mousebutton(0)

d = waitdump(lambda d: d is not None
             and decode(d, NY, NX + 1, "Files", WHITE) == "Files", 25)
expect(d is not None, "after the drag the window's title reads at the new place")
if d:
    said = decode(d, NY + 2, NX + 2, "Notes kept on the disk:", GRAY)
    expect(said == "Notes kept on the disk:",
           f"the window's heading stands at the new place (read: {said!r})")
    said = decode(d, NY + 3, NX + 4, FIRST, WHITE)
    expect(said == FIRST,
           f"the first note stands picked at the new place (read: {said!r})")
    said = decode(d, NY + 4, NX + 4, SECOND, GRAY)
    expect(said == SECOND,
           f"the second note stands listed at the new place (read: {said!r})")
    bad = old_place_remnants(d)
    expect(len(bad) == 0,
           "the ground the window stood on is plain desktop again, "
           f"no remnants ({len(bad)} non-black pixels, first of them {bad[:8]})")

# A press on the second note's row in the DRAGGED
# window: the pointer's point stands at (480, 344); a
# move of (-180, +64) lays it at (300, 408), on the
# second note's row at the new place (row 25).
mousemove(-180, 64)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, NY + 4, NX + 4, SECOND, WHITE) == SECOND, 15)
expect(d is not None, "a press on the second note's row in the dragged window picked it")
if d:
    said = decode(d, NY + 3, NX + 4, FIRST, GRAY)
    expect(said == FIRST,
           f"the first note now stands unpicked at the new place (read: {said!r})")
    said = decode(d, NY + 12, NX + 2, SECOND, WHITE)
    expect(said == SECOND,
           f"the picked note's whole words stand at the dragged window's foot (read: {said!r})")

# The close mark at the DRAGGED place closes the
# window: its cell is the window's left + 52 at its top
# row — the point (1000, 344), a move of (+700, -64)
# from where the pointer stands.
mousemove(700, -64)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None and pixel(d, 400, NY * 16 + 40) == BLACK
             and pixel(d, 300, NY * 16 + 100) == BLACK, 15)
expect(d is not None, "the close mark at the dragged place closed the window")

done()
