# Stone 40 proof, boot 1: names in the files window,
# on a fitted keeping disk prepared with three known
# notes (the CNN3 store laid directly, as
# prove-stone27.sh lays it) and one kept picture (the
# CNP store: its header on sector 80, its bytes on
# sectors 81 to 83).
#
# "Rename" and "Copy" stand at the files window's foot
# beside "Let this note go", and every word is DECODED
# letter by letter against the system's own letter
# shapes. A press on "Rename" opens the naming way;
# Enter on an empty name is refused in plain words in
# the window ("Write the new name first."), and the
# third note's own words typed as the name are refused
# the same way ("That name already stands. Pick
# another name."), with the note whole after both —
# Escape puts the naming away and the list stands as
# it was. The first note is then renamed to "garden
# notes": the list stands repainted with the new name
# picked and the note's words whole at the foot. A
# press on "Copy" and the name "garden copy" lay a
# second keeping on the page, standing picked with
# the first note's words at the foot; the first note
# is let go through Stone 27's asking, and the copy,
# picked afterwards, still stands whole at the foot.
# The kept picture is renamed to "garden picture" the
# same way. prove-stone40.sh reads the disk's own
# bytes after this boot, and boot 2 proves what a
# restart finds.

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
# 5, top row 31. In the files window: heading at GY+2,
# the notes at GY+3 onward (words or names at GX+4),
# the foot's label at GY+11 with "Rename" at GX+24,
# "Copy" at GX+31 and "Let this note go" at GX+36, the
# picked note's words at GY+12, and the picture's row
# at GY+13. In the naming way: the asking at GY+2, the
# name the thing stands under at GY+3, "Its words:" at
# GY+5 with the words at GY+6, the typing word at
# GY+8, the name being typed at GY+9, the measure at
# GY+11, and the naming's own word at GY+12.
GX, GY = 5, 31
A = "remember the garden"
B = "call billy about the roof"
C = "pray for quinton"
N1 = "garden notes"
N2 = "garden copy"
PN = "garden picture"
PIC = "A picture you painted"
ASK = "Give this note a new name:"
PASK = "Give this picture a new name:"
CASK = "Make a copy of this note:"

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

# --- the files window: the naming words stand at its foot ---
typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, "Notes kept on the disk:", GRAY)
             == "Notes kept on the disk:", 25)
expect(d is not None, "the word 'files' opened the files window on the disk's notes")
if d:
    said = decode(d, GY + 3, GX + 4, A, WHITE)
    expect(said == A, f"the first note stands picked under its words (read: {said!r})")
    said = decode(d, GY + 11, GX + 24, "Rename", WHITE)
    expect(said == "Rename",
           f"'Rename' stands at the window's foot (read: {said!r})")
    said = decode(d, GY + 11, GX + 31, "Copy", WHITE)
    expect(said == "Copy",
           f"'Copy' stands at the window's foot (read: {said!r})")
    said = decode(d, GY + 11, GX + 36, "Let this note go", WHITE)
    expect(said == "Let this note go",
           f"'Let this note go' stands beside them, unmoved (read: {said!r})")
    said = decode(d, GY + 13, GX + 4, PIC, GRAY)
    expect(said == PIC,
           f"the kept picture stands listed under its plain words (read: {said!r})")

# --- a press on "Rename" opens the naming way ---
click((GX + 27) * 16 + 8, (GY + 11) * 16 + 8)
park()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, ASK, GRAY) == ASK, 15)
expect(d is not None, "a press on 'Rename' opened the naming way, in plain words")
if d:
    said = decode(d, GY + 3, GX + 2, A, WHITE)
    expect(said == A, f"the naming shows the name the note stands under (read: {said!r})")
    said = decode(d, GY + 5, GX + 2, "Its words:", GRAY)
    expect(said == "Its words:", f"the naming names the words below (read: {said!r})")
    said = decode(d, GY + 6, GX + 2, A, WHITE)
    expect(said == A, f"the note's words stand whole under the naming (read: {said!r})")
    said = decode(d, GY + 8, GX + 2, "Type the new name, then press Enter:", GRAY)
    expect(said == "Type the new name, then press Enter:",
           f"the naming says how the name is given (read: {said!r})")
    said = decode(d, GY + 11, GX + 2, "A name can hold 19 letters at most.", GRAY)
    expect(said == "A name can hold 19 letters at most.",
           f"the naming says the name's measure plainly (read: {said!r})")
    said = decode(d, GY + 12, GX + 2, "Press Escape to keep the name it has.", GRAY)
    expect(said == "Press Escape to keep the name it has.",
           f"the naming says how it is put away (read: {said!r})")

# --- refusal one: an empty name is refused, in the window ---
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 12, GX + 2, "Write the new name first.", WHITE)
             == "Write the new name first.", 15)
expect(d is not None, "Enter on an empty name was refused in plain words in the window")
if d:
    said = decode(d, GY + 3, GX + 2, A, WHITE)
    expect(said == A, f"the note stands whole after the refusal (read: {said!r})")

# --- refusal two: a name that already stands is refused ---
typewrite(C)
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 12, GX + 2,
                        "That name already stands. Pick another name.", WHITE)
             == "That name already stands. Pick another name.", 15)
expect(d is not None, "a name that already stands was refused in plain words in the window")
if d:
    said = decode(d, GY + 2, GX + 2, ASK, GRAY)
    expect(said == ASK, f"the naming stands open after the refusal (read: {said!r})")
    said = decode(d, GY + 9, GX + 2, C, WHITE)
    expect(said == C, f"the refused name stands as it was typed (read: {said!r})")
    said = decode(d, GY + 3, GX + 2, A, WHITE)
    expect(said == A, f"nothing was renamed by the refusal (read: {said!r})")

# --- Escape puts the naming away; the list stands as it was ---
sendkey("esc")
d = waitdump(lambda d: d is not None
             and decode(d, GY + 3, GX + 4, A, WHITE) == A, 15)
expect(d is not None, "Escape put the naming away, the list repainted whole")
if d:
    said = decode(d, GY + 5, GX + 4, C, GRAY)
    expect(said == C, f"the third note stands whole in the list (read: {said!r})")
    said = decode(d, GY + 12, GX + 2, A, WHITE)
    expect(said == A, f"the first note's words stand at the foot (read: {said!r})")

# --- the rename itself: the list repaints under the new name ---
click((GX + 27) * 16 + 8, (GY + 11) * 16 + 8)
park()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, ASK, GRAY) == ASK, 15)
expect(d is not None, "the naming way opened again")
typewrite(N1)
d = waitdump(lambda d: d is not None
             and decode(d, GY + 9, GX + 2, N1, WHITE) == N1, 15)
expect(d is not None, "the name being typed stands in the window as it is typed")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 3, GX + 4, N1, WHITE) == N1, 15)
expect(d is not None, "the renamed note stands under its new name, the list repainted")
if d:
    said = decode(d, GY + 12, GX + 2, A, WHITE)
    expect(said == A,
           f"the renamed note's words stand whole at the foot — its text survived (read: {said!r})")
    said = decode(d, GY + 4, GX + 4, B, GRAY)
    expect(said == B, f"the second note stands unmoved (read: {said!r})")
    said = decode(d, GY + 5, GX + 4, C, GRAY)
    expect(said == C, f"the third note stands unmoved (read: {said!r})")

# --- the copy: a second keeping under a new name ---
click((GX + 33) * 16 + 8, (GY + 11) * 16 + 8)
park()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, CASK, GRAY) == CASK, 15)
expect(d is not None, "a press on 'Copy' opened the naming way for a copy")
if d:
    said = decode(d, GY + 3, GX + 2, N1, WHITE)
    expect(said == N1, f"the copy's naming shows the name the note stands under (read: {said!r})")
    said = decode(d, GY + 6, GX + 2, A, WHITE)
    expect(said == A, f"the copy's naming shows the note's words whole (read: {said!r})")
    said = decode(d, GY + 8, GX + 2, "Type the copy's name, then press Enter:", GRAY)
    expect(said == "Type the copy's name, then press Enter:",
           f"the copy's naming says how its name is given (read: {said!r})")
typewrite(N2)
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 6, GX + 4, N2, WHITE) == N2, 15)
expect(d is not None, "the copy stands on the page under its new name, picked, the list repainted")
if d:
    said = decode(d, GY + 3, GX + 4, N1, GRAY)
    expect(said == N1, f"the first note stands above its copy (read: {said!r})")
    said = decode(d, GY + 12, GX + 2, A, WHITE)
    expect(said == A,
           f"the copy's words stand at the foot — the first note's words, whole (read: {said!r})")

# --- let the first note go: the copy stands whole without it ---
click(200, (GY + 3) * 16 + 8)
park()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 3, GX + 4, N1, WHITE) == N1, 15)
expect(d is not None, "a press on the first note's row picked it again")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, "Let this note go for good?", GRAY)
             == "Let this note go for good?", 15)
expect(d is not None, "Enter opened Stone 27's asking for the first note")
sendkey("up")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 3, GX + 4, B, WHITE) == B, 15)
expect(d is not None, "the yes let the first note go: the second stands first now")
if d:
    said = decode(d, GY + 5, GX + 4, N2, GRAY)
    expect(said == N2, f"the copy stands third on the page (read: {said!r})")
click(200, (GY + 5) * 16 + 8)
park()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 5, GX + 4, N2, WHITE) == N2, 15)
expect(d is not None, "a press on the copy's row picked the copy")
if d:
    said = decode(d, GY + 12, GX + 2, A, WHITE)
    expect(said == A,
           f"the copy still opens whole — its words stand at the foot with the first note gone (read: {said!r})")

# --- the picture renamed the same way ---
sendkey("down")
d = waitdump(lambda d: d is not None
             and decode(d, GY + 13, GX + 4, PIC, WHITE) == PIC, 15)
expect(d is not None, "the down arrow picked the kept picture")
if d:
    said = decode(d, GY + 11, GX + 2, "The picture you picked:", GRAY)
    expect(said == "The picture you picked:",
           f"the foot names the picture as picked (read: {said!r})")
    said = decode(d, GY + 11, GX + 36, "Rename", WHITE)
    expect(said == "Rename",
           f"'Rename' stands at the foot for the picture (read: {said!r})")
click((GX + 39) * 16 + 8, (GY + 11) * 16 + 8)
park()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, PASK, GRAY) == PASK, 15)
expect(d is not None, "a press on the picture's 'Rename' opened its naming way")
if d:
    said = decode(d, GY + 3, GX + 2, PIC, WHITE)
    expect(said == PIC, f"the picture's naming shows the name it stands under (read: {said!r})")
    said = decode(d, GY + 5, GX + 2, "The picture itself will not change.", GRAY)
    expect(said == "The picture itself will not change.",
           f"the picture's naming says the picture itself is untouched (read: {said!r})")
    said = decode(d, GY + 11, GX + 2, "A name can hold 43 letters at most.", GRAY)
    expect(said == "A name can hold 43 letters at most.",
           f"the picture's naming says its measure plainly (read: {said!r})")
typewrite(PN)
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 13, GX + 4, PN, WHITE) == PN, 15)
expect(d is not None, "the picture stands under its new name, the list repainted")
if d:
    said = decode(d, GY + 11, GX + 2, "The picture you picked:", GRAY)
    expect(said == "The picture you picked:",
           f"the picture still stands picked at the foot (read: {said!r})")

done()
