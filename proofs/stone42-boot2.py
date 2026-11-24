# Boot 2 of Stone 42's proof: the Shield's reckoning
# of a refusal, on a disc whose welcome feather has
# been tampered with (one byte of its program turned
# after its card was written, the making in
# prove-stone42.sh — the same tampering the disc
# proof's third boot uses). The word 'feather' asks
# for the visit: the feather window comes forward,
# but no visit stands in it — its body still says no
# feather has visited yet — for the door has reckoned
# the feather's bytes against its card, found them
# not matching, and turned the feather away in plain
# words (the refusal's own words are the disc proof's
# to read). The word 'shield' then opens the Shield
# window, and its reckoning tells what the door did:
# none let in, one turned away. Escape closes it.

import re

BLUE = (0, 0, 170)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (170, 170, 170)

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


SX, SY = 5, 28

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

typewrite("feather")
enter()
# The feather window stands at left cell 5, top row
# 26; before any visit its body says so, two rows
# below its title, two cells in — and after the
# refused asking it says so still.
d = waitdump(lambda d: d is not None
             and decode(d, 26, 6, "Feather", WHITE) == "Feather"
             and decode(d, 28, 7, "No feather has visited yet.", GRAY)
             == "No feather has visited yet.", 25)
expect(d is not None, "the refused feather never visited: the window still says so")

typewrite("shield")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, SY, SX + 1, "Shield", WHITE) == "Shield"
             and decode(d, SY + 12, SX + 2, "Feathers turned away: 1", BLACK)
             == "Feathers turned away: 1", 25)
expect(d is not None, "the Shield window's reckoning shows the feather turned away")
if d:
    said = decode(d, SY + 11, SX + 2,
                  "Feathers let in since this rising: 0", BLACK)
    expect(said == "Feathers let in since this rising: 0",
           f"and none let in (read: {said!r})")

sendkey("esc")
d = waitdump(lambda d: d is not None
             and decode(d, SY, SX + 1, "Shield", WHITE) != "Shield", 15)
expect(d is not None, "Escape closed the Shield window")

done()
