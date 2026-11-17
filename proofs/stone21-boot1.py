# Stone 21 proof, boot 1: the editor window, with a
# fitted keeping disk prepared with one known note (the
# CNN3 store laid directly, as prove-stone19.sh lays it:
# the settings card on sector 8, the notes header on
# sector 64, one sector to a note from sector 65).
#
# The word 'editor' opens the window in its picking way;
# its rendered list is DECODED letter by letter against
# the system's own letter shapes (parsed from
# src/font.nifla, the way prove-featherpaint.sh reads).
# A press of the pointer picks the kept note, Enter takes
# it into the writing way with its whole words standing
# as the draft, and Escape closes the window leaving the
# note untouched. A new note is then written with the
# desktop's own typing, kept by Enter, and stands in the
# list; the forty-three-letter measure is typed past and
# the draft stops at it, the window naming the measure
# in plain words; the over-long draft is thrown away by
# Escape and never reaches the page. The kept note is
# then changed in the window — its last word rubbed out
# and another typed — and kept back to the same place.
# The files window, opened between, shows the same notes
# from the same store; Tab brings the editor forward
# among the five windows, and Escape closes it.

import re

BLUE = (0, 0, 170)
WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
DARK = (85, 85, 85)
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


# The editor window's place on this face (1024x768,
# sixty-four cells across): fifty-four wide, centered —
# left at cell 5, top at cell row 32, like the files and
# settings windows. Title at row 32; the picking way's
# heading at 34, the new-note entry at 35 and the kept
# notes at 36 onward (their words at column 9), the
# keeping word at 44; the writing way's heading at 34,
# the draft at 35 (column 7), the measure at 37, the
# keep word at 38, and the keeping word at 40.
GX, GY = 5, 32
OLD = "remember the garden"
NEW = "pray for mother"
CHANGED = "pray for father"

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

typewrite("editor")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2,
                        "Pick a note, then press Enter to write it:", GRAY)
             == "Pick a note, then press Enter to write it:", 25)
expect(d is not None, "the word 'editor' opened the editor window in its picking way")
if d:
    said = decode(d, GY, GX + 1, "Editor", WHITE)
    expect(said == "Editor", f"the window's title reads in plain words (read: {said!r})")
    said = decode(d, GY + 3, GX + 4, "Write a new note", WHITE)
    expect(said == "Write a new note",
           f"the new-note entry stands picked, white on blue (read: {said!r})")
    said = decode(d, GY + 4, GX + 4, OLD, GRAY)
    expect(said == OLD, f"the kept note is listed (read: {said!r})")
    said = decode(d, GY + 12, GX + 2, "Notes are kept on the disk.", GRAY)
    expect(said == "Notes are kept on the disk.",
           f"the window says the notes are kept on the disk (read: {said!r})")

# A press of the pointer on the kept note's row picks
# it: the arrow's point stands at (506, 378); a move of
# (-306, +206) lays it at (200, 584), on the note's row
# (cell row 36).
mousemove(-306, 206)
mousebutton(1)
mousebutton(0)
mousemove(500, -400)
d = waitdump(lambda d: d is not None
             and decode(d, GY + 4, GX + 4, OLD, WHITE) == OLD, 15)
expect(d is not None, "a press on the kept note's row picked it, white on blue")

# Enter takes the pick into the writing way: the note's
# whole words stand as the draft, to be changed.
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, "Change your note:", GRAY)
             == "Change your note:", 15)
expect(d is not None, "Enter opened the writing way over the picked note")
if d:
    said = decode(d, GY + 3, GX + 2, OLD, WHITE)
    expect(said == OLD,
           f"the note's whole words stand as the draft (read: {said!r})")

# Escape closes the window; the note stands untouched,
# as the list below will show again.
sendkey("esc")
d = waitdump(lambda d: d is not None and pixel(d, 400, GY * 16 + 10) == BLACK
             and pixel(d, 600, 600) == BLACK, 15)
expect(d is not None, "Escape closed the editor window back to the desktop")

# A new note, written in the window: the word opens the
# window afresh (the new-note entry picked), Enter takes
# it into the writing way, and the desktop's typing
# writes the draft.
typewrite("editor")
enter()
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, "Write your note:", GRAY)
             == "Write your note:", 15)
expect(d is not None, "Enter on the new-note entry opened the writing way")
if d:
    said = decode(d, GY + 5, GX + 2, "A note can hold 43 letters at most.", GRAY)
    expect(said == "A note can hold 43 letters at most.",
           f"the writing way names the note's measure in plain words (read: {said!r})")
    said = decode(d, GY + 6, GX + 2, "Press Enter to keep the note.", GRAY)
    expect(said == "Press Enter to keep the note.",
           f"the writing way says how the note is kept (read: {said!r})")
    said = decode(d, GY + 8, GX + 2, "Your note will be kept on the disk.", GRAY)
    expect(said == "Your note will be kept on the disk.",
           f"the writing way says the note will be kept on the disk (read: {said!r})")

typewrite(NEW)
d = waitdump(lambda d: d is not None
             and decode(d, GY + 3, GX + 2, NEW, WHITE) == NEW, 15)
expect(d is not None, "the typed words stand as the draft in the window")

# Enter keeps the note: the window returns to its
# picking way, the new note listed and standing picked.
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 5, GX + 4, NEW, WHITE) == NEW, 15)
expect(d is not None, "Enter kept the note: it stands in the list, picked")
if d:
    said = decode(d, GY + 4, GX + 4, OLD, GRAY)
    expect(said == OLD, f"the first note still stands above it (read: {said!r})")

# The measure, honestly: forty-six letters are typed at
# a fresh note and the draft stops at forty-three — the
# window does not let the words run past in silence.
sendkey("up")
sendkey("up")
enter()
typewrite("a" * 46)
d = waitdump(lambda d: d is not None
             and decode(d, GY + 3, GX + 2, "a" * 43, WHITE) == "a" * 43, 25)
expect(d is not None, "the draft stops at the note's measure of forty-three letters")
sendkey("esc")
d = waitdump(lambda d: d is not None and pixel(d, 400, GY * 16 + 10) == BLACK, 15)
expect(d is not None, "Escape threw the over-long draft away with the window")

# The page still holds exactly the two notes: the
# thrown-away draft never reached the store.
typewrite("editor")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 5, GX + 4, NEW, GRAY) == NEW, 15)
expect(d is not None, "the kept note still stands in the list after the discard")
if d:
    said = decode(d, GY + 4, GX + 4, OLD, GRAY)
    expect(said == OLD, f"the first note stands untouched (read: {said!r})")

# Change the kept note in the window: two downs pick it,
# Enter opens the writing way over its whole words, six
# backspaces rub out its last word, and another is typed
# in its place.
sendkey("down")
sendkey("down")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 3, GX + 2, NEW, WHITE) == NEW, 15)
expect(d is not None, "the picked note's words stand as the draft to change")
for _ in range(6):
    sendkey("backspace")
typewrite("father")
d = waitdump(lambda d: d is not None
             and decode(d, GY + 3, GX + 2, CHANGED, WHITE) == CHANGED, 15)
expect(d is not None, "the draft now reads with its last word changed")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 5, GX + 4, CHANGED, WHITE) == CHANGED, 15)
expect(d is not None, "Enter kept the change back to the same place in the list")

# The files window reckons from the same store: opened
# now, it lists the same two notes, the changed words
# standing in it. Its first place stands one row above
# the editor's since Stone 33 (top row 31 to the
# editor's 32 — the taller files window rose to stand
# above the bar at the screen's foot), so its rows are
# read at FY, one less than the editor's GY.
FY = GY - 1
typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, FY + 4, GX + 4, CHANGED, GRAY) == CHANGED, 15)
expect(d is not None, "the files window lists the changed note from the same store")
if d:
    said = decode(d, FY + 3, GX + 4, OLD, WHITE)
    expect(said == OLD,
           f"the files window lists the first note, picked (read: {said!r})")

# Tab cycles through the five windows: from the files
# window it comes to the editor (the settings window
# stands closed), whose title bar stands blue again.
sendkey("tab")
d = waitdump(lambda d: d is not None and pixel(d, 400, GY * 16 + 10) == BLUE
             and decode(d, GY, GX + 1, "Editor", WHITE) == "Editor", 15)
expect(d is not None, "Tab brought the editor window forward among the five")

# Escape closes the editor; the files window, still
# open at the same place on the desktop, stands in its
# place — its own heading reads where the editor's
# stood.
sendkey("esc")
d = waitdump(lambda d: d is not None
             and decode(d, FY + 2, GX + 2, "Notes kept on the disk:", GRAY)
             == "Notes kept on the disk:", 15)
expect(d is not None, "Escape closed the editor: the files window stands in its place")

done()
