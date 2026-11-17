# Pointer-trail proof, boot 1: the pointer is DRAGGED
# across the desktop, and afterwards the desktop must
# stand exactly as it stood before.
#
# The shipped disc is booted at the BIOS door (the face
# of light). A reference picture of the desktop is taken
# with the arrow at the screen's middle. The bench's
# mouse then carries the arrow through a path of stops
# across the desktop — wide moves, then a drag of small
# steps out and back — and home to the middle again,
# each stop confirmed by the arrow standing there. A
# second picture is then taken, and the two pictures
# must agree at EVERY pixel but the bottom bar's clock
# ground (the bar stands at the foot since Stone 33 and
# carries the clock, whose seconds honestly advance
# between the two pictures; nothing else on the desktop
# moves on its own). The bottom row of every stop's
# patch — the row at the stop's y + 16 — is also named
# and checked on its own, because that row is where the
# fault lived.
#
# Why this proof exists: the arrow's white edge is laid
# one pixel around its black shape, so its bottom pass
# paints at y + 16 — one row BELOW the sixteen-by-
# sixteen square the pointer's save kept and laid back.
# That row was drawn but never saved or restored, so
# every place the arrow had stood kept the five white
# edge pixels of its last row: a dotted trail across
# the desktop, witnessed by Tyler dragging the pointer
# in UTM (November 15, 2026). The standing Stone 13
# proof moved the arrow and checked the square it left
# — sixteen rows of it — and passed, because the trail
# stands in the seventeenth row it never looked at.
# This proof compares the whole desktop, so no row can
# hide again.

BLUE = (0, 0, 170)
WHITE = (255, 255, 255)

HOME = (504, 376)


def arrow_white(d, x0, y0):
    """The arrow's white edge, counted in its whole
    patch: sixteen wide and seventeen tall."""
    if d is None:
        return 0
    n = 0
    for y in range(y0, y0 + 17):
        for x in range(x0, x0 + 16):
            if pixel(d, x, y) == WHITE:
                n += 1
    return n


def frame_diff(a, b):
    """Every pixel where two pictures disagree, leaving
    out the bottom bar's clock ground (Stone 33: the
    bar stands at the foot now — its right end, the
    clock's cells on its lower row, is the one honest
    difference time makes)."""
    out = []
    w, h, pa = a
    _, _, pb = b
    for y in range(0, h):
        if y >= 752:
            xs = range(0, 380)
        else:
            xs = range(0, w)
        base = y * w * 3
        for x in xs:
            o = base + x * 3
            if pa[o:o + 3] != pb[o:o + 3]:
                out.append((x, y))
    return out


d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")
if d:
    expect(arrow_white(d, HOME[0], HOME[1]) > 20,
           "the arrow stands at the screen's middle")

time.sleep(1)
ref = dump()
expect(ref is not None, "the reference desktop is taken, the arrow at home")

# The path: wide moves across the desktop, each stop a
# place the arrow stands and is then taken from. The
# stops stand on different grounds — the black answers
# region, the feather window, the open desktop — so the
# trail is tried against each.
STOPS = [(704, 476), (454, 536), (304, 536),
         (424, 276), (704, 316)]
MOVES = [(200, 100), (-250, 60), (-150, 0),
         (120, -260), (280, 40)]
if ref:
    for (dx, dy), (sx, sy) in zip(MOVES, STOPS):
        mousemove(dx, dy)
        d = waitdump(lambda d, sx=sx, sy=sy:
                     d is not None and arrow_white(d, sx, sy) > 20, 15)
        expect(d is not None,
               f"the arrow followed the mouse to ({sx}, {sy})")

    # The drag: small steps out from the last wide stop,
    # small steps back to it — the motion Tyler's hand
    # made, many stands in a line.
    for i in range(6):
        mousemove(30, 20)
    d = waitdump(lambda d: d is not None
                 and arrow_white(d, 884, 436) > 20, 15)
    expect(d is not None, "the drag carried the arrow out to (884, 436)")
    for i in range(6):
        mousemove(-30, -20)
    d = waitdump(lambda d: d is not None
                 and arrow_white(d, 704, 316) > 20, 15)
    expect(d is not None, "the drag brought the arrow back to (704, 316)")

    # And home to the middle, where the reference stands.
    mousemove(-200, 60)
    d = waitdump(lambda d: d is not None
                 and arrow_white(d, HOME[0], HOME[1]) > 20, 15)
    expect(d is not None, "the arrow stands at home for the reckoning")

    time.sleep(1)
    after = dump()
    expect(after is not None, "the desktop is read again after the dragging")
    if after:
        diff = frame_diff(ref, after)
        expect(len(diff) == 0,
               "after the drag the desktop is pixel for pixel what it "
               f"was before it ({len(diff)} differing pixels, "
               f"first of them {diff[:8]})")
        # The fault's own row, named: at every wide stop,
        # the row one below the arrow's old square must
        # hold the desktop the reference holds there.
        trail = []
        for (sx, sy) in STOPS:
            for x in range(sx, sx + 16):
                if pixel(ref, x, sy + 16) != pixel(after, x, sy + 16):
                    trail.append((x, sy + 16))
        expect(len(trail) == 0,
               "no stop keeps the arrow's bottom edge row: the trail "
               f"row stands clean at every stop ({len(trail)} "
               f"remnant pixels, first of them {trail[:8]})")

done()
