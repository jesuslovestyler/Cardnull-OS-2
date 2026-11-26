# Stone 25 proof, boot 1: a kind shutdown. A fitted
# keeping disk stands ready (its settings card laid by
# prove-stone25.sh); a note is kept by the word 'note'
# and seen standing in the files window; the bar's menu
# is opened and its NINE choices decoded — the eight
# windows (Stone 23's five, the verse window, Stone
# 29, the calculator window, Stone 30, and the help
# window, Stone 31) and, under
# them, Rest (Stone 25: the menu grew by that one
# choice; Stone 29's Verse choice later took the sixth
# row and Rest moved to the seventh, and Stone 30's
# Calculator choice took the seventh row and Rest
# moved to the eighth, and Stone 31's Help choice took
# the eighth row and Rest moved to the ninth, and this
# proof's reckoning moved with it each time —
# Stone 23's own proof still checks the five it
# always checked). A
# press on the Rest choice opens the rest panel at the
# desktop's middle, and its plain words are DECODED
# letter by letter against the system's own letter
# shapes: Rest, Shut down, Restart, Stay. A press on
# Shut down's row then rests the machine: this scenario
# polls the bench afterwards and records which of the
# two honest endings the bench shows — the machine
# actually powered off (the monitor's door closed with
# the QEMU process gone, which prove-stone25.sh also
# checks from outside), or the machine still standing
# with the plain fallback words rendered in its answers
# ("The machine is still on. It is now safe to turn it
# off."), decoded the same way. Either is a pass; the
# script says which one the bench showed.

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


def find_answer(d, text):
    """The answers region (face rows 24 to 45, from the
    second column) is searched for one whole line, in
    the answers' gray — the fallback's home if the
    machine stayed on."""
    for r in range(24, 46):
        if decode(d, r, 2, text, GRAY) == text:
            return True
    return False


# Places on this face (1024x768, sixty-four cells
# across, forty-eight down): the files window at left
# cell 5, top row 30 (Stone 19; row 32 until Stone 33,
# row 31 until Stone 49 grew the window by a row);
# the menu at left 0, top row 37 — it rose from the
# start button at the bar's foot since Stone 33 — its
# choices one to a row (Stone 23, grown at Stone 25,
# again at Stone 29, and again at Stone 30); the rest
# panel centered — sixteen wide, four high, so left
# cell 24, top row 22, its words at its left + 1.
FX, FY = 5, 30
ML, MT = 0, 37
RL, RT = 24, 22
NOTE = "a note before rest"

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

# A note is kept, and seen standing in the files window.
typewrite("note " + NOTE)
enter()
typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, FY + 3, FX + 4, NOTE, WHITE) == NOTE, 25)
expect(d is not None, "the note was kept and stands in the files window")
sendkey("esc")
d = waitdump(lambda d: d is not None
             and pixel(d, 200, FY * 16 + 8) == BLACK, 15)
expect(d is not None, "Escape closed the files window")

# The start button opens the menu, risen from the
# bar at the screen's foot; its nine choices stand
# decoded, Rest the ninth (Stone 29's Verse choice
# stands sixth, Stone 30's Calculator choice seventh,
# Stone 31's Help choice eighth). The pointer's point
# starts at (506, 378); a move of (-490, +374) lays it
# at (16, 752), the button's own center.
mousemove(-490, 374)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, MT + 8, ML + 1, "Rest", WHITE) == "Rest", 25)
expect(d is not None, "a press on the start button opened the menu, with Rest standing in it")
if d:
    for i, word in enumerate(("Welcome", "Feather", "Files",
                              "Settings", "Editor", "Verse",
                              "Calculator", "Help", "Rest")):
        said = decode(d, MT + i, ML + 1, word, WHITE)
        expect(said == word,
               f"the menu's choice {i + 1} reads {word!r} (read: {said!r})")

# A press on the Rest choice opens the rest panel; its
# plain words decode at its reckoned place. The point
# stands at (16, 752); a move of (+24, -24) lays it at
# (40, 728), on the menu's ninth row — the typing
# line's own row, where Rest's words stand.
mousemove(24, -24)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None
             and decode(d, RT + 1, RL + 1, "Shut down", WHITE) == "Shut down", 25)
expect(d is not None, "a press on the menu's Rest choice opened the rest panel")
if d:
    for i, word in enumerate(("Rest", "Shut down", "Restart", "Stay")):
        said = decode(d, RT + i, RL + 1, word, WHITE)
        expect(said == word,
               f"the rest panel's row {i + 1} reads {word!r} (read: {said!r})")

# A press on Shut down's row: the point stands at
# (40, 728) (the Rest choice's row, the menu's ninth);
# a move of (+410, -352) lays it at
# (450, 376), on the panel's second row. The release
# is wrapped: on a bench whose power door answers, the
# machine can be gone before the release is even sent
# — the monitor's door closes under the harness's hand
# (measured on this bench: exactly that happened, the
# broken pipe itself the poweroff's first evidence) —
# and the poll below is the judge either way.
mousemove(410, -352)
mousebutton(1)
try:
    mousebutton(0)
except Exception:
    print("ok: the bench's monitor closed before the press could be "
          "released — the machine was already powering off")

# Which honest ending does the bench show? Poll: a
# dump that raises means the monitor's door closed —
# the machine powered off and QEMU is gone. A dump
# that decodes the fallback line means the machine
# stayed on and said so, in plain words.
off = False
fallback = False
end = time.time() + 30
while time.time() < end and not off and not fallback:
    try:
        d = dump()
    except Exception:
        off = True
        break
    if d is not None and d[0] == 1024:
        if find_answer(d, "The machine is still on. It is now safe to turn it off."):
            fallback = True
    time.sleep(0.4)
expect(off or fallback,
       "choosing Shut down rested the machine: it powered off, or it "
       "stands halted with its plain fallback words rendered")
if off:
    print("ok: BENCH RESULT — the machine actually powered off under QEMU")
if fallback:
    print("ok: BENCH RESULT — the machine stayed on; the fallback words stand rendered")

# The bench result is written where prove-stone25.sh
# reads it back from (STONE25_RESULT1): the script's
# own report of which ending the bench showed comes
# from this, and from nothing else — after done()
# below, the bench's process is gone either way,
# because done() itself asks QEMU to quit.
import os
_rp = os.environ.get("STONE25_RESULT1")
if _rp:
    with open(_rp, "w") as _f:
        _f.write("off" if off else "fallback" if fallback else "neither")

done()
