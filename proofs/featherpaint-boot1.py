# Feather-paint proof, boot 1: the feather's visit, READ
# BACK as writing. The shipped disc is booted at the BIOS
# door (the face of light), the word 'feather' is typed,
# and the feather window's painted pixels are then
# DECODED — each letter cell's white-on-green pattern is
# matched against the system's own letter shapes (parsed
# here from src/font.nifla, the same shapes pixface
# draws with) — and the three lines must come back
# exactly as the feather wrote them:
#
#   "A feather is visiting"
#   "Hello. I am a small program, here as a feather."
#   "I was checked first, and I am whole."
#
# The panel between the window's edges must also stand
# solid: every pixel in the panel's rectangle green or
# white, with no unpainted row anywhere (no banding).
# And the system's own word for the visit is decoded
# the same way, in its gray on black: since Stone 47
# it stands in the terminal's keeping, as the first
# kept line — the visit no longer stamps it straight
# onto the desktop's ground below the window — so Tab
# brings the terminal forward and the line is read
# there, and the ground where the stamp stood is read
# too, and must stand plain.
#
# Why this proof exists: the visit's first painting laid
# each of the feather's cells at the place the layout
# reckonings (laycol/layrow) give its text-face row and
# column, squeezing eighty columns onto sixty-four and
# stretching twenty-five rows over forty-eight — one
# letter in five was overwritten by its neighbor and
# the panel's rows stood a row apart, banded. Tyler
# witnessed it on his own machine (November 15, 2026)
# reading "A fetheris vsitig" for "A feather is
# visiting", while every standing proof passed: they
# counted green and white pixels in bands, and garbled
# letters have the same colors as whole ones. This
# proof reads the letters themselves.

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
# the text face's row 14 (cell row 26). The panel's
# cells stand at rows 28 to 32, columns 6 to 57; its
# writing begins two cells in, at column 8.
GX, GY = 5, 26

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")
if d:
    said = decode(d, GY + 2, GX + 2, "No feather has visited yet.", GRAY)
    expect(said == "No feather has visited yet.",
           f"before any visit the window says so in whole letters (read: {said!r})")

typewrite("feather")
enter()
d = waitdump(lambda d: d is not None and count(d, GREEN) > 10000, 25)
expect(d is not None, "the feather's visit is shown: its green panel as light")
if d:
    time.sleep(1)
    d = dump()
    line1 = decode(d, GY + 3, GX + 3, "A feather is visiting", WHITE)
    expect(line1 == "A feather is visiting",
           f"the feather's first line reads whole (read: {line1!r})")
    line2 = decode(d, GY + 4, GX + 3,
                   "Hello. I am a small program, here as a feather.", WHITE)
    expect(line2 == "Hello. I am a small program, here as a feather.",
           f"the feather's second line reads whole (read: {line2!r})")
    line3 = decode(d, GY + 5, GX + 3,
                   "I was checked first, and I am whole.", WHITE)
    expect(line3 == "I was checked first, and I am whole.",
           f"the feather's third line reads whole (read: {line3!r})")
    stray = 0
    for y in range((GY + 2) * 16, (GY + 7) * 16):
        for x in range((GX + 1) * 16, (GX + 53) * 16):
            if pixel(d, x, y) not in (GREEN, WHITE):
                stray += 1
    expect(stray == 0,
           f"the panel stands solid green, no unpainted band ({stray} stray pixels)")
    # Stone 47: the visit's word stands in the
    # terminal's keeping, as its first kept line.
    # Tab brings the terminal forward from under the
    # feather window, and the line is read there.
    said = None
    for _ in range(6):
        sendkey("tab")
        time.sleep(0.6)
        d = dump()
        if d is not None and decode(d, 32, 6, "Terminal", WHITE) == "Terminal":
            said = decode(d, 33, 7,
                          "The feather visited, and has gone home again.",
                          GRAY)
            break
    expect(said == "The feather visited, and has gone home again.",
           f"the system's own word for the visit reads whole in the "
           f"terminal's keeping (read: {said!r})")
    # And the ground where the stamp stood — the
    # layout's row 21, pixel row 40, left of the
    # terminal window — stands plain: no gray letters.
    stray = 0
    for y in range(40 * 16, 40 * 16 + 16):
        for x in range(2 * 16, 5 * 16):
            if pixel(d, x, y) == GRAY:
                stray += 1
    expect(stray == 0,
           f"the ground where the visit's stamp stood is plain "
           f"({stray} gray pixels)")

done()
