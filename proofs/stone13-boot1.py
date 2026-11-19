# Stone 13 proof, boot 1: the pointer on the face of
# light. The arrow stands at the screen's middle when the
# desktop rises; the monitor's own mouse_move carries it
# (its +x is right and its +y is down, as the bench
# speaks); where it left, the desktop stands whole again;
# and a press of the first button brings the feather —
# the same visit the word 'feather' brings, its green
# panel and all. No green stands anywhere before the
# press. (Stone 38: the feather's panel lives in the
# feather window now, not on the ground, so the press
# road is the desktop's own: the start button, then the
# risen menu's Feather choice, which asks for the
# feather exactly as the word does.)

import re

BLUE = (0, 0, 170)
GREEN = (0, 170, 0)
GRAY = (170, 170, 170)
WHITE = (255, 255, 255)

_vals = {}
for _m in re.finditer(r"block\[(\d+)\] = (\d+)",
                      open("src/font.nifla").read()):
    _vals[int(_m.group(1))] = int(_m.group(2))
GLYPHS = {}
for _code in range(32, 127):
    GLYPHS[_code] = tuple(_vals.get((_code - 32) * 8 + _r, 0)
                          for _r in range(8))


def decode(d, prow, pcol, text, ink):
    if d is None:
        return ""
    out = []
    for i in range(len(text)):
        cx, cy = (pcol + i) * 16, prow * 16
        bm = []
        for r in range(8):
            v = 0
            for c in range(8):
                if pixel(d, cx + 2 * c + 1, cy + 2 * r + 1) == ink:
                    v |= 1 << (7 - c)
            bm.append(v)
        bm = tuple(bm)
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


def arrow_white(d, x0, y0):
    """The arrow's white edge, counted in its square."""
    if d is None:
        return 0
    n = 0
    for y in range(y0, y0 + 16):
        for x in range(x0, x0 + 16):
            if pixel(d, x, y) == WHITE:
                n += 1
    return n


d = waitdump(lambda d: d is not None and d[0] == 1024 and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")
if d:
    expect(count(d, GREEN) == 0, "no feather panel stands before the press")
    expect(arrow_white(d, 504, 376) > 20,
           "the arrow stands at the screen's middle")

# The arrow follows the mouse: right 200, down 100.
mousemove(200, 100)
d = waitdump(lambda d: d is not None and arrow_white(d, 704, 476) > 20, 15)
expect(d is not None, "the arrow followed the mouse to its new place")
if d:
    expect(arrow_white(d, 504, 376) == 0,
           "where the arrow left, the desktop stands whole")

# Onto the start button, and press: the arrow's point
# is its square's (2, 2), standing at (706, 478) now —
# two moves of (-345, +137) lay it on the button's
# center (16, 752), and the press raises the menu.
mousemove(-345, 137)
mousemove(-345, 137)
d = waitdump(lambda d: d is not None and arrow_white(d, 14, 750) > 20, 15)
expect(d is not None, "the arrow stands on the start button")
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, 38, 1, "Feather", WHITE) == "Feather", 15)
expect(d is not None, "the press raised the menu from the start button: its Feather choice stands")

# Onto the menu's Feather choice (its second row, row
# 38; the point (40, 616)), and press: the visit the
# word 'feather' brings.
mousemove(24, -136)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None and count(d, GREEN) > 10000, 25)
expect(d is not None, "the press brought the feather: its green panel stands")

# The typing line still works, with the pointer about.
# The visit left the feather window forward over the
# terminal's first answer rows, so a press on the
# terminal's typing row raises the terminal first —
# the answer then stands in the clear at its first
# answer row (row 33, y 528..543).
mousemove(360, 96)
mousebutton(1)
mousebutton(0)
typewrite("hello")
enter()
d = waitdump(lambda d: d is not None and sum(
    1 for y in range(528, 544) for x in range(0, 1024)
    if pixel(d, x, y) == GRAY) > 50, 20)
expect(d is not None, "'hello' is answered in light, the pointer about")

done()
