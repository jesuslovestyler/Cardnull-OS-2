# Stone 29 proof, boot 2: the verse window at the
# LARGE size, with no disk fitted. The settings
# window's Large row is pressed first (its point at
# (168, 712), as in Stone 28's boots), Escape closes
# the settings window, and the word 'verse' opens the
# verse window on the narrow large face (forty-two
# cells across): left cell 1, top row 20 — the
# layout's row 17 held up off the face's floor — forty
# wide, twelve high. The day's verse (the bench clock
# stands pinned as in boot 1: 1 John 5:13) must stand
# in it whole, wrapped at the narrower width (thirty-
# six letters), DECODED letter by letter at the large
# scale and joined back into its exact World English
# Bible wording, its reference under it, and Escape
# closes it again.

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


def wrap(text, width):
    """The window painter's own wrapping reckoning, as
    in boot 1."""
    lines = []
    start = 0
    n = len(text)
    while start < n:
        end = start + width
        if end >= n:
            end = n
        else:
            j = end
            while j > start and text[j] != " ":
                j -= 1
            if j > start:
                end = j
        lines.append(text[start:end])
        start = end
        if start < n and text[start] == " ":
            start += 1
    return lines


VERSE = ("These things I have written to you who believe in the "
         "name of the Son of God, that you may know that you have "
         "eternal life, and that you may continue to believe in "
         "the name of the Son of God.")
REF = "1 John 5:13"

PX, PY = 506, 378


def click(x, y):
    global PX, PY
    mousemove(x - PX, y - PY)
    PX, PY = x, y
    mousebutton(1)
    mousebutton(0)


# The settings window's place at the usual size, and
# at the large size after the press, as in Stone 28.
UX, UY = 5, 30
LX, LY = 1, 14
# The verse window's place at the large size: left
# cell 1, top row 18, forty wide, twelve high, its
# verse at its left + 2 wrapped at thirty-six letters,
# its reference at its top + 10.
VX, VY = 1, 18
LINES = wrap(VERSE, 36)

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

typewrite("settings")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, UY, UX + 1, "Settings", WHITE, 2) == "Settings", 25)
expect(d is not None, "the settings window opened at the usual size")

click(168, 680)
d = waitdump(lambda d: d is not None
             and decode(d, LY + 12, LX + 4, "Large", WHITE, 3) == "Large", 25)
expect(d is not None, "a press on the Large row stood the words large")

sendkey("esc")
# (Stone 38: the closing is read at x=700 now — the
# old sample at x=100 stands on the Calculator
# icon's name, which stands on that ground since
# the desktop gained its icons.)
d = waitdump(lambda d: d is not None
             and pixel(d, 700, LY * 24 + 12) == BLACK, 15)
expect(d is not None, "Escape closed the settings window")

# The word 'verse', on the large face: the window
# stands at its large place, the verse whole in it.
# The pointer is first moved up to the face's top
# left, off the window's words — left where the Large
# press put it, it would rest on the reference's own
# letters and spoil their decoding.
mousemove(-54, -310)
mousemove(-54, -310)
typewrite("verse")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, VY, VX + 1, "Verse", WHITE, 3) == "Verse", 25)
expect(d is not None, "the word 'verse' opened the verse window at the large size")
if d:
    expect(pixel(d, 600, VY * 24 + 12) == BLUE,
           "the verse window stands forward at the large size, its title bar blue")
    joined = []
    for i, line in enumerate(LINES):
        said = decode(d, VY + 2 + i, VX + 2, line, BLACK, 3)
        expect(said == line,
               f"the verse's large line {i + 1} reads exactly (read: {said!r})")
        joined.append(said)
    expect(" ".join(joined) == VERSE,
           "the large wrapped lines join back into the verse's exact WEB wording")
    said = decode(d, VY + 10, VX + 2, REF, BLACK, 3)
    expect(said == REF,
           f"the verse's reference stands plainly under it, large (read: {said!r})")

sendkey("esc")
d = waitdump(lambda d: d is not None
             and pixel(d, 100, VY * 24 + 12) == BLACK, 15)
expect(d is not None, "Escape closed the verse window at the large size")

done()
