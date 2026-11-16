# Stone 27 proof, boot 3: a sitting's notes let go.
# NO disk is fitted: two notes are kept by the word
# 'note' for the sitting only, and the files window —
# which now lists a sitting's notes under their honest
# heading — picks the second, asks, and lets it go by
# keyboard (Enter, up, Enter). The editor's list, from
# the same page, then holds the first note only: a
# session-only note is removable with the same
# confirmation, through the same page.

import re

BLUE = (0, 0, 170)
WHITE = (255, 255, 255)
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
FIRST = "first words"
SECOND = "second words"
ASK = "Let this note go for good?"

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

typewrite("note first words")
enter()
typewrite("note second words")
enter()

typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2,
                        "Notes kept only for this sitting:", GRAY)
             == "Notes kept only for this sitting:", 25)
expect(d is not None, "with no disk, the files window lists the sitting's notes honestly")
if d:
    said = decode(d, GY + 3, GX + 4, FIRST, WHITE)
    expect(said == FIRST, f"the first sitting note stands picked (read: {said!r})")
    said = decode(d, GY + 4, GX + 4, SECOND, GRAY)
    expect(said == SECOND, f"the second sitting note is listed (read: {said!r})")

sendkey("down")
d = waitdump(lambda d: d is not None
             and decode(d, GY + 12, GX + 2, SECOND, WHITE) == SECOND, 15)
expect(d is not None, "the down arrow picked the second sitting note")

enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, ASK, GRAY) == ASK, 15)
expect(d is not None, "the asking opened for the sitting note, the same asking")
sendkey("up")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 3, GX + 4, FIRST, WHITE) == FIRST, 15)
expect(d is not None, "the yes let the second sitting note go")
if d:
    said = decode(d, GY + 4, GX + 4, SECOND, GRAY)
    expect(said == " " * len(SECOND),
           "the files list holds the first sitting note only")

typewrite("editor")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 4, GX + 4, FIRST, GRAY) == FIRST, 15)
expect(d is not None, "the editor's list holds the first sitting note, from the same page")
if d:
    said = decode(d, GY + 5, GX + 4, SECOND, GRAY)
    expect(said == " " * len(SECOND),
           "the note let go in the files window is gone from the editor too")

done()
