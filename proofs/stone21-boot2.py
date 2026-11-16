# Stone 21 proof, boot 2: the editor window with no
# disk fitted at all. The window says plainly, in both
# its ways, that a note is kept only for this sitting —
# the same honesty the answers have always kept — and a
# note written and kept in the window stands in its list
# for the sitting, and in the reckoning of the word
# 'notes' besides: one store, however it is reached.

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


GX, GY = 5, 32
NOTE = "kept for now"

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

typewrite("editor")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 12, GX + 2,
                        "Notes are kept only for this sitting.", GRAY)
             == "Notes are kept only for this sitting.", 25)
expect(d is not None, "with no disk, the picking way says the notes last only for this sitting")
if d:
    said = decode(d, GY + 5, GX + 2, "No notes are kept yet.", GRAY)
    expect(said == "No notes are kept yet.",
           f"no note is invented for the empty page (read: {said!r})")

enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 8, GX + 2,
                        "Your note will be kept only for this sitting.", GRAY)
             == "Your note will be kept only for this sitting.", 15)
expect(d is not None, "the writing way says the note will be kept only for this sitting")
if d:
    said = decode(d, GY + 9, GX + 2, "There is no disk fitted.", GRAY)
    expect(said == "There is no disk fitted.",
           f"the writing way says there is no disk fitted (read: {said!r})")

typewrite(NOTE)
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 4, GX + 4, NOTE, WHITE) == NOTE, 15)
expect(d is not None, "the note written in the window stands in its list for the sitting")

# The word 'notes' reckons the same store: its answer
# names the sitting, and the note the window kept stands
# in it. The answers begin at the face's row 24; the
# heading is found by its own letters, wherever the
# boot's lines have left it, and the note must stand on
# the row beneath it.
typewrite("notes")
enter()


def heading_row(d):
    if d is None:
        return None
    for r in range(24, 29):
        if decode(d, r, 2, "Your notes, kept until the machine is turned off:",
                  GRAY) == "Your notes, kept until the machine is turned off:":
            return r
    return None


d = waitdump(lambda d: heading_row(d) is not None, 15)
expect(d is not None, "the word 'notes' answers that the notes are kept until the machine is turned off")
if d:
    r = heading_row(d)
    said = decode(d, r + 1, 2, NOTE, GRAY)
    expect(said == NOTE,
           f"the note the window kept stands in the word's reckoning (read: {said!r})")

done()
