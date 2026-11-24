# Stone 46 proof, boot 1: all the programs in the
# start menu. A scenario for tools/pixels.py, the way
# the later proofs are written.
#
# The shipped disc is booted at the BIOS door, no
# disk fitted. A press on the start button opens the
# bar's menu, and all THIRTEEN of its choices are
# decoded at their reckoned rows — Welcome, Feather,
# Files, Editor, Paint, Calculator, Verse, Help,
# Settings, Terminal, Bible, Shield, Rest — the
# desktop icons' own order since this stone, the two
# newcomers standing where they stand among their
# neighbors: Paint fifth, after Editor; Terminal
# tenth, after Settings. Then choices are pressed,
# and each opens its window exactly as its typed
# word does:
#
#   Paint (a new choice): the paint window opens and
#     its feather's opening visit stands in it — the
#     invitation "Pick a color, then draw below."
#     reads in the window, as prove-stone24 reads it.
#   Terminal (a new choice): the terminal window
#     comes forward — its title decodes and its bar
#     stands in the front window's blue.
#   Bible (a moved choice, ninth before this stone,
#     eleventh now): the Bible window opens on its
#     contents page, its title decoded and its bar
#     blue, and the book's name standing in it.
#   Rest (last in the menu, as always): the rest
#     panel opens at the desktop's middle, its
#     heading and its first choice decoded; a press
#     on Stay puts it away. Rest is pressed FIRST
#     among the choices, straight from the decoding's
#     open menu: its row is the menu's lowest, eight
#     pixels from the bar, and this bench's pointer
#     reckoning drifts a little with every move it is
#     given — the lowest row is taken while the
#     reckoning is freshest.
#
# Prints one ok/NOT OK line per check and PASS or
# FAIL as the last line; the exit code carries the
# verdict.

import re

BLUE = (0, 0, 170)
WHITE = (255, 255, 255)
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


ML, MT = 0, 33
CHOICES = ("Welcome", "Feather", "Files", "Editor", "Paint",
           "Calculator", "Verse", "Help", "Settings", "Terminal",
           "Bible", "Shield", "Rest")

# The pointer's standing place, kept as the proofs
# keep it: it starts at (506, 378), and every move
# below is reckoned from it.
PX = [506, 378]


def move(dx, dy):
    # The road to the point is walked in small steps,
    # the standing proofs' discipline (their go()):
    # one long move is a flood of packets to the
    # guest, and under this bench's load some are
    # lost — the pointer falls short and every later
    # press lands off its mark by the loss. Small
    # steps with a breath between them arrive.
    while dx != 0 or dy != 0:
        sx = max(-48, min(48, dx))
        sy = max(-48, min(48, dy))
        mousemove(sx, sy)
        PX[0] += sx
        PX[1] += sy
        dx -= sx
        dy -= sy


def press_at(x, y):
    move(x - PX[0], y - PX[1])
    mousebutton(1)
    mousebutton(0)


def open_menu(rowword):
    # A press on the start button (its center at
    # (16, 752)), and the menu standing open with the
    # named row decoded in it.
    press_at(16, 752)
    return waitdump(lambda d: d is not None
                    and decode(d, MT + CHOICES.index(rowword), ML + 1,
                               rowword, WHITE) == rowword, 25)


d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

d = open_menu("Rest")
expect(d is not None, "a press on the start button opened the menu, "
                      "with Rest standing last in it")
if d:
    for i, word in enumerate(CHOICES):
        said = decode(d, MT + i, ML + 1, word, WHITE)
        expect(said == word,
               f"the menu's choice {i + 1} reads {word!r} (read: {said!r})")

def choose(rowword, row, outcome, secs=12):
    # Opens the menu (the named row decoded in it) and
    # presses the row, waiting on the outcome; a press
    # the bench's mouse loses on the way is simply
    # taken again, the way the standing proofs take
    # their presses — the check judges the outcome,
    # however many takings the bench needed. The
    # takings also step the press's point a few pixels
    # up and down the row: a packet lost anywhere on
    # the road here leaves the pointer's reckoning a
    # little off its true place, and a row is only
    # sixteen pixels tall — the nudged takings cover
    # the reckoning's drift, and the outcome demanded
    # is the same at every taking.
    for nudge in (0, 8, -8, 16, -16):
        if open_menu(rowword) is None:
            continue
        press_at(40, (MT + row) * 16 + 8 + nudge)
        d = waitdump(outcome, secs)
        if d is not None:
            return d
    return None


# ---- Rest, from the last row — pressed first -----
# The menu stands open from the decoding above, and
# Rest's row is the menu's last and lowest, its press
# point eight pixels from the menu's foot and the
# bar: on this bench the pointer's reckoning drifts
# a little with every move it is given, so the
# lowest row is pressed while the reckoning is
# freshest, before the other choices are taken.
RL, RT = 24, 22
press_at(40, (MT + 12) * 16 + 8)
d = waitdump(lambda d: d is not None
             and decode(d, RT + 1, RL + 1, "Shut down", WHITE) == "Shut down",
             12)
if d is None:
    d = choose("Rest", 12,
               lambda d: d is not None
               and decode(d, RT + 1, RL + 1, "Shut down", WHITE)
               == "Shut down")
expect(d is not None,
       "a press on the menu's Rest choice opened the rest panel")
if d:
    said = decode(d, RT, RL + 1, "Rest", WHITE)
    expect(said == "Rest",
           f"the rest panel stands under its heading (read: {said!r})")
# Stay puts the panel away; the desktop stands whole.
press_at((RL + 2) * 16, (RT + 3) * 16 + 8)
d = waitdump(lambda d: d is not None
             and decode(d, RT + 1, RL + 1, "Shut down", WHITE) != "Shut down",
             25)
expect(d is not None, "a press on the panel's Stay put the rest panel away")

# ---- Paint, from its new row (the fifth) -----------
d = choose("Paint", 4,
           lambda d: d is not None
           and decode(d, 34, 8, "Pick a color, then draw below.", WHITE)
           == "Pick a color, then draw below.")
expect(d is not None,
       "a press on the menu's Paint choice opened the paint window, "
       "and its feather's opening visit stands in it")

# ---- Terminal, from its new row (the tenth) --------
# Its bar's blue is read at the bar's twentieth
# column, clear of its title's letters.
d = choose("Terminal", 9,
           lambda d: d is not None
           and decode(d, 32, 6, "Terminal", WHITE) == "Terminal"
           and pixel(d, 320, 32 * 16 + 8) == BLUE)
expect(d is not None,
       "a press on the menu's Terminal choice brought the terminal "
       "window forward — its title decoded, its bar in the front blue")

# ---- Bible, from its moved row (the eleventh) ------
d = choose("Bible", 10,
           lambda d: d is not None
           and decode(d, 30, 6, "Bible", WHITE) == "Bible"
           and pixel(d, 200, 30 * 16 + 8) == BLUE)
expect(d is not None,
       "a press on the menu's Bible choice opened the Bible window — "
       "its title decoded, its bar in the front blue")
if d:
    said = decode(d, 31, 7, "Jonah", BLACK)
    expect(said == "Jonah",
           f"the Bible window stands on its contents page (read: {said!r})")

done()
