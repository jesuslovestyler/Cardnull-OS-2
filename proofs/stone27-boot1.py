# Stone 27 proof, boot 1: letting a note go, on a fitted
# keeping disk prepared with three known notes (the CNN3
# store laid directly, as prove-stone19.sh lays it: the
# settings card on sector 8, the notes header on sector
# 64, one sector to a note from sector 65).
#
# In the files window the first note stands picked, with
# "Let this note go" standing at the window's foot. A
# press on those words opens the asking — "Let this note
# go for good?", the note's words, "Yes, let it go" and
# "Keep it", with "Keep it" standing picked — and every
# word of it is DECODED letter by letter against the
# system's own letter shapes. The cancel paths are
# proven first: a press on "Keep it" leaves the note
# whole, and Escape after Enter opens the asking leaves
# it whole again. Then Enter and the up arrow and Enter
# let the first note go for real. In the editor window
# the third note is picked, its "Let this note go" is
# pressed, and a press on "Yes, let it go" lets it go.
# prove-stone27.sh reads the disk's own bytes after this
# boot, and boot 2 proves what a restart finds.

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


CUR = [506, 378]


def move_to(x, y):
    mousemove(x - CUR[0], y - CUR[1])
    CUR[0], CUR[1] = x, y


def click(x, y):
    move_to(x, y)
    mousebutton(1)
    time.sleep(0.4)
    mousebutton(0)
    time.sleep(0.4)


def park():
    move_to(60, 60)


# The windows' place on this face (1024x768, sixty-four
# cells across): fifty-four wide, centered — left cell
# 5, top row 32. In the files window: heading at GY+2,
# the notes at GY+3 onward (words at GX+4), the foot's
# label at GY+11 with "Let this note go" at GX+36, the
# picked note's words at GY+12. The asking (either
# window): the question at GY+2, the note's words at
# GY+3, "Yes, let it go" at GY+5, "Keep it" at GY+6
# (their words at GX+4). In the editor's picking way:
# the new-note entry at GY+3, the notes at GY+4 onward,
# the keeping word at GY+12 with "Let this note go" at
# GX+36 on that row.
GX, GY = 5, 30
A = "remember the garden"
B = "call billy about the roof"
C = "pray for quinton"
ASK = "Let this note go for good?"
YES = "Yes, let it go"
KEEP = "Keep it"
GO = "Let this note go"

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

# --- the files window: the offer stands at its foot ---
typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, "Notes kept on the disk:", GRAY)
             == "Notes kept on the disk:", 25)
expect(d is not None, "the word 'files' opened the files window on the disk's notes")
if d:
    said = decode(d, GY + 3, GX + 4, A, WHITE)
    expect(said == A, f"the first note stands picked (read: {said!r})")
    said = decode(d, GY + 11, GX + 36, GO, WHITE)
    expect(said == GO,
           f"'Let this note go' stands at the window's foot (read: {said!r})")
    said = decode(d, GY + 12, GX + 2, A, WHITE)
    expect(said == A,
           f"the picked note's words stand at the foot (read: {said!r})")

# --- a press on the words asks first ---
click((GX + 36) * 16 + 8, (GY + 11) * 16 + 8)
park()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, ASK, GRAY) == ASK, 15)
expect(d is not None, "a press on 'Let this note go' asked first, in plain words")
if d:
    said = decode(d, GY + 3, GX + 2, A, WHITE)
    expect(said == A, f"the asking shows the note's own words (read: {said!r})")
    said = decode(d, GY + 5, GX + 4, YES, GRAY)
    expect(said == YES, f"the yes stands plainly, not picked (read: {said!r})")
    said = decode(d, GY + 6, GX + 4, KEEP, WHITE)
    expect(said == KEEP,
           f"'Keep it' stands picked — Enter alone lets nothing go (read: {said!r})")

# --- cancel by pointer: the note stands whole ---
click(200, (GY + 6) * 16 + 8)
park()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, "Notes kept on the disk:", GRAY)
             == "Notes kept on the disk:", 15)
expect(d is not None, "a press on 'Keep it' put the asking away")
if d:
    said = decode(d, GY + 3, GX + 4, A, WHITE)
    expect(said == A, f"the note stands whole after the no (read: {said!r})")
    said = decode(d, GY + 5, GX + 4, C, GRAY)
    expect(said == C, f"the third note stands whole too (read: {said!r})")

# --- cancel by Escape: the note stands whole ---
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, ASK, GRAY) == ASK, 15)
expect(d is not None, "Enter on the picked note opened the asking again")
sendkey("esc")
d = waitdump(lambda d: d is not None
             and decode(d, GY + 12, GX + 2, A, WHITE) == A, 15)
expect(d is not None, "Escape put the asking away, the note whole at the foot")
if d:
    said = decode(d, GY + 3, GX + 4, A, WHITE)
    expect(said == A, f"the note still stands picked and whole (read: {said!r})")

# --- the yes, by keyboard: the first note is let go ---
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, ASK, GRAY) == ASK, 15)
expect(d is not None, "the asking opened once more")
sendkey("up")
d = waitdump(lambda d: d is not None
             and decode(d, GY + 5, GX + 4, YES, WHITE) == YES, 15)
expect(d is not None, "the up arrow picked 'Yes, let it go'")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 3, GX + 4, B, WHITE) == B, 15)
expect(d is not None, "the yes let the first note go: the second stands first now")
if d:
    said = decode(d, GY + 4, GX + 4, C, GRAY)
    expect(said == C, f"the third note stands second, whole (read: {said!r})")
    said = decode(d, GY + 5, GX + 4, C, GRAY)
    expect(said == " " * len(C),
           "no third entry remains — the page holds two notes")
    said = decode(d, GY + 12, GX + 2, B, WHITE)
    expect(said == B, f"the foot shows the newly picked note (read: {said!r})")

# --- the editor window: the same letting go ---
# (The editor's first place stands at row 32 still —
# Stone 33 rose only the taller windows — so its rows
# are read at EY, two more than the files window's GY
# since Stone 49 grew the files window by its exchange row (the editor
# itself stands where it stood, at row 32).)
EY = GY + 2
typewrite("editor")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, EY + 2, GX + 2,
                        "Pick a note, then press Enter to write it:", GRAY)
             == "Pick a note, then press Enter to write it:", 25)
expect(d is not None, "the word 'editor' opened the editor window on the same store")
if d:
    said = decode(d, EY + 4, GX + 4, B, GRAY)
    expect(said == B, f"the editor lists the note the files window kept (read: {said!r})")
    said = decode(d, EY + 5, GX + 4, C, GRAY)
    expect(said == C, f"the editor lists the third note (read: {said!r})")
    said = decode(d, EY + 12, GX + 36, GO, WHITE)
    expect(said == " " * len(GO),
           "no letting go is offered while the new-note entry stands picked")

click(200, (EY + 5) * 16 + 8)
park()
d = waitdump(lambda d: d is not None
             and decode(d, EY + 5, GX + 4, C, WHITE) == C, 15)
expect(d is not None, "a press on the third note's row picked it in the editor")
if d:
    said = decode(d, EY + 12, GX + 36, GO, WHITE)
    expect(said == GO,
           f"'Let this note go' stands at the editor's foot (read: {said!r})")

click((GX + 36) * 16 + 8, (EY + 12) * 16 + 8)
park()
d = waitdump(lambda d: d is not None
             and decode(d, EY + 2, GX + 2, ASK, GRAY) == ASK, 15)
expect(d is not None, "a press on the editor's words asked first, the same asking")
if d:
    said = decode(d, EY + 3, GX + 2, C, WHITE)
    expect(said == C, f"the editor's asking shows the note's words (read: {said!r})")
    said = decode(d, EY + 6, GX + 4, KEEP, WHITE)
    expect(said == KEEP, f"'Keep it' stands picked in the editor too (read: {said!r})")

click(200, (EY + 5) * 16 + 8)
park()
d = waitdump(lambda d: d is not None
             and decode(d, EY + 4, GX + 4, B, WHITE) == B, 15)
expect(d is not None, "a press on 'Yes, let it go' let the third note go")
if d:
    said = decode(d, EY + 5, GX + 4, C, GRAY)
    expect(said == " " * len(C),
           "the editor's list holds the one remaining note only")
    said = decode(d, EY + 3, GX + 4, "Write a new note", GRAY)
    expect(said == "Write a new note",
           f"the new-note entry stands above it, unpicked (read: {said!r})")

done()
