# Stone 25 proof, boot 2: restart, and the kept note
# surviving it. A fitted keeping disk stands ready (its
# settings card laid by prove-stone25.sh, its notes page
# empty). A note is kept by the word 'note'; the word
# 'rest' opens the rest panel — its plain words DECODED
# letter by letter against the system's own letter
# shapes — and a press on Restart's row rests the
# machine the other way: this scenario then watches the
# desktop FALL (the drawn face goes — the screen leaves
# the picture shape or its blue bar goes) and RISE A
# SECOND TIME in the same QEMU run (the drawn desktop
# standing again, the welcome window's title decoded
# again). After the second rise the word 'files' opens
# the files window, and the note kept before the restart
# must stand in its list, read back from the disk by the
# second rising, exactly as it was typed.

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


def desktop_up(d):
    return (d is not None and d[0] == 1024
            and pixel(d, 300, 760) == BLUE
            and decode(d, 5, 7, "Welcome", WHITE) == "Welcome")


# Places on this face, as in boot 1: the files window
# at left cell 5, top row 32; the rest panel centered —
# left cell 24, top row 22, its words at its left + 1.
FX, FY = 5, 31
RL, RT = 24, 22
NOTE = "still here after rest"

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn (the first rise)")

# A note is kept before the restart.
typewrite("note " + NOTE)
enter()
# (The keeping is proven where it can be read whole:
# in the files window after the restart, below — and
# the answer line's own words are Stone 15's standing
# proof. A short settle is all that is needed here.)
time.sleep(2)

# The typed word 'rest' opens the rest panel.
typewrite("rest")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, RT + 2, RL + 1, "Restart", WHITE) == "Restart", 25)
expect(d is not None, "the word 'rest' opened the rest panel")
if d:
    for i, word in enumerate(("Rest", "Shut down", "Restart", "Stay")):
        said = decode(d, RT + i, RL + 1, word, WHITE)
        expect(said == word,
               f"the rest panel's row {i + 1} reads {word!r} (read: {said!r})")

# A press on Restart's row: the point stands at
# (506, 378); a move of (-56, +14) lays it at
# (450, 392), on the panel's third row.
mousemove(-56, 14)
mousebutton(1)
mousebutton(0)

# The desktop must FALL: the drawn face goes (the
# screen leaves its picture shape, or the bar's blue
# leaves its place) as the machine resets and the
# firmware's own screen stands in its place.
fell = False
end = time.time() + 30
while time.time() < end and not fell:
    try:
        d = dump()
    except Exception:
        d = None
    if d is None or d[0] != 1024 or pixel(d, 300, 760) != BLUE:
        fell = True
    time.sleep(0.3)
expect(fell, "the desktop fell: the machine truly reset")

# And RISE A SECOND TIME in the same run: the drawn
# desktop standing again, its welcome window's title
# decoded again.
d = waitdump(desktop_up, 60)
expect(d is not None,
       "the desktop rose a second time in the same run after the restart")

# After the second rise, the files window lists the
# note kept before the restart — it survived, read
# back from the disk by the second rising.
if d:
    typewrite("files")
    enter()
    d = waitdump(lambda d: d is not None
                 and decode(d, FY + 2, FX + 2, "Notes kept on the disk:", GRAY)
                 == "Notes kept on the disk:", 25)
    expect(d is not None, "the files window opened after the second rise")
    if d:
        said = decode(d, FY + 3, FX + 4, NOTE, WHITE)
        expect(said == NOTE,
               f"the note kept before the restart is still there (read: {said!r})")

done()
