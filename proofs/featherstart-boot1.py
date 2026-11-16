# Feather-start proof, boot 1: the word "feather" as
# the STARTUP face spells it, READ BACK as writing,
# with NO input at all.
#
# The shipped disc is booted at the BIOS door (the
# face of light) and NO key is sent and NO mouse is
# moved: the scenario only waits and looks, as
# prove-nowitness does. At the desktop's rising both
# windows stand open (the welcome forward, the
# feather's behind it), so the feather window's title
# bar is part of the first thing a person sees. Every
# place the word "feather" stands in that startup
# view is DECODED — each letter cell's pattern matched
# against the system's own letter shapes (parsed here
# from src/font.nifla, the same shapes pixface draws
# with):
#
#   * the feather window's title, "Feather", at its
#     title row;
#   * the feather window's body before any visit,
#     "No feather has visited yet.";
#   * the word "feather" in the invitation line under
#     the welcome panel ("hello time memory eastern
#     utc feather welcome usb setup clear").
#
# Why this proof exists: the feather-paint proof
# (prove-featherpaint.sh) types the word 'feather'
# first and then decodes the VISIT's panel — a path
# that repaints the window after a visit. The startup
# painting is the same painter reached with empty
# hands, and Tyler, booting the delivered disc of
# November 16, 2026 in UTM, read its title as "feath"
# — the word losing its last two letters where he
# first met it, while the visit itself read whole.
# Counting colors is not reading, and typing first is
# not starting; this proof reads the startup view
# itself, letter by letter, with no hands on the
# machine.

import re

BLUE = (0, 0, 170)
GREEN = (0, 170, 0)
WHITE = (255, 255, 255)
GRAY = (170, 170, 170)

# The system's letter shapes, from its own font file:
# the shape for the letter of code c stands at
# (c - 32) * 8, eight row-bytes, the leftmost pixel the
# row's high bit.
_vals = {}
for _m in re.finditer(r"block\[(\d+)\] = (\d+)",
                      open("src/font.nifla").read()):
    _vals[int(_m.group(1))] = int(_m.group(2))
GLYPHS = {}
for _code in range(32, 127):
    GLYPHS[_code] = tuple(_vals.get((_code - 32) * 8 + _r, 0)
                          for _r in range(8))


def cell_bitmap(d, cx, cy, ink):
    """One letter cell's 8x8 pattern: the ink pixels at
    the centers of the cell's doubled font pixels."""
    rows = []
    for r in range(8):
        v = 0
        for c in range(8):
            if pixel(d, cx + 2 * c + 1, cy + 2 * r + 1) == ink:
                v |= 1 << (7 - c)
        rows.append(v)
    return tuple(rows)


def decode(d, prow, pcol, text, ink):
    """The writing painted at (prow, pcol), read cell by
    cell against the letter shapes — as many cells as
    the expected text holds."""
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


# The feather window's place on this face (1024x768,
# sixty-four cells across): fifty-four wide, centered —
# its left at cell 5, its top at the layout's row for
# the text face's row 14 (cell row 26). Its title
# stands at its top row, one cell in; its body two
# rows below the title, two cells in. The invitation's
# second line stands at the layout's row for the text
# face's row 12 (cell row 23), two cells in, and the
# word "feather" stands thirty letters into it.
GX, GY = 5, 26

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "with no input at all, the desktop is drawn")
if d:
    title = decode(d, GY, GX + 1, "Feather", WHITE)
    expect(title == "Feather",
           f"at startup the feather window's title reads whole (read: {title!r})")
    said = decode(d, GY + 2, GX + 2, "No feather has visited yet.", GRAY)
    expect(said == "No feather has visited yet.",
           f"at startup the feather window's body reads whole (read: {said!r})")
    word = decode(d, 23, 2 + 30, "feather", GRAY)
    expect(word == "feather",
           f"at startup the invitation's word reads whole (read: {word!r})")

done()
