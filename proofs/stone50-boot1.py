# Stone 50 proof, boot 1: the making of a Cardinal.
# A fitted keeping disk stands ready (its Eastern
# card, two notes — the second named "roof note" —
# and a kept picture, laid by prove-stone50.sh), and
# the shipped stick stands on the bus, the system
# running from the disc. The word 'files' lists the
# keeping; the window — grown by one row for this
# stone, its top at row 29 — carries on its new last
# row "Make this computer a Cardinal" (DECODED). A
# press on the words opens the making's asking: the
# plain question, what will happen said plainly, and
# the two choices with "Not yet" standing picked, so
# Enter alone installs nothing. A press on "Yes,
# make it a Cardinal" runs the making: the window
# first says it is making, and when the copy has
# landed and proved, it answers "This computer is a
# Cardinal now." The disk's own bytes are read by
# prove-stone50.sh between the boots: the record, the
# image at sector 2048, and the keeping untouched.

import re

BLUE = (0, 0, 170)
RED = (170, 0, 0)
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
    while CUR[0] != x or CUR[1] != y:
        dx = max(-61, min(61, x - CUR[0]))
        dy = max(-61, min(61, y - CUR[1]))
        mousemove(dx, dy)
        CUR[0] += dx
        CUR[1] += dy


def click(x, y):
    move_to(x, y)
    mousebutton(1)
    time.sleep(0.4)
    mousebutton(0)
    time.sleep(0.4)


def park():
    move_to(60, 60)


# The files window's place: left cell 5, top row 29
# since this stone grew it by the making's row. Its
# list stands at GY + 3 and after, the picture's
# entry on GY + 13, the exchange's row on GY + 14,
# and the making's row on GY + 15 — its words, and
# its own word after a making, at GX + 2.
GX, GY = 5, 29


def row_has(text, row=None, ink=WHITE):
    if row is None:
        row = GY + 15
    return lambda d: d is not None and \
        decode(d, row, GX + 2, text, ink) == text


def press_door():
    """A press on the making's words, given the
    stone-47 bench discipline: the machine is let
    settle first, and the press is tried up to three
    times, the asking's question read after each."""
    time.sleep(2)
    for _try in range(3):
        click((GX + 7) * 16 + 8, (GY + 15) * 16 + 8)
        park()
        d = waitdump(lambda d: d is not None and decode(
            d, GY + 2, GX + 2, "Make this computer a Cardinal?",
            GRAY) == "Make this computer a Cardinal?", 10)
        if d is not None:
            return d
    return None


def press_yes(final, final_secs):
    """A press on the asking's yes row, with the same
    discipline; the making's own word — that it is
    making, or the final word itself — ends the
    pressing, and the final word is then awaited for
    as long as the copy honestly takes."""
    time.sleep(2)
    for _try in range(3):
        click((GX + 10) * 16 + 8, (GY + 7) * 16 + 8)
        park()
        d = waitdump(lambda d: d is not None and (
            decode(d, GY + 15, GX + 2, "Making this computer a Cardinal...",
                   WHITE) == "Making this computer a Cardinal..."
            or decode(d, GY + 15, GX + 2, final, WHITE) == final), 25)
        if d is not None:
            break
    return waitdump(row_has(final), final_secs)


# The desktop's wait is long on purpose: with a USB
# stick on the bus, SeaBIOS walks the bus before it
# reads the disc, and on this bench that walk can
# take the better part of a minute — once, under
# load, more — before the face of light rises at all.
d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 150)
expect(d is not None, "the desktop is drawn")

# The files window lists the disk's keeping, and the
# making's words stand on its new last row.
typewrite("files")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, GY + 2, GX + 2, "Notes kept on the disk:", GRAY)
             == "Notes kept on the disk:", 25)
expect(d is not None, "the word 'files' opened the files window on the disk's keeping")
if d:
    said = decode(d, GY + 3, GX + 4, "remember the garden", WHITE)
    expect(said == "remember the garden",
           f"the first note stands in the list (read: {said!r})")
    said = decode(d, GY + 4, GX + 4, "roof note", GRAY)
    expect(said == "roof note",
           f"the second note stands under its name (read: {said!r})")
    said = decode(d, GY + 13, GX + 4, "kept picture", GRAY)
    expect(said == "kept picture",
           f"the kept picture stands in the list under its name (read: {said!r})")
    said = decode(d, GY + 15, GX + 2, "Make this computer a Cardinal", WHITE)
    expect(said == "Make this computer a Cardinal",
           f"the making's words stand on the window's last row (read: {said!r})")

# A press on the words opens the asking, with "Not
# yet" standing picked.
d = press_door()
expect(d is not None, "a press on the making's words opened the asking")
if d:
    said = decode(d, GY + 3, GX + 2, "Cardnull will be copied from the stick", GRAY)
    expect(said == "Cardnull will be copied from the stick",
           f"the asking says what will happen, plainly (read: {said!r})")
    said = decode(d, GY + 5, GX + 2, "Your notes and your picture stay as they are.", GRAY)
    expect(said == "Your notes and your picture stay as they are.",
           f"the asking promises the keeping stays (read: {said!r})")
    said = decode(d, GY + 8, GX + 4, "Not yet", WHITE)
    expect(said == "Not yet",
           f"'Not yet' stands picked, white on blue (read: {said!r})")
    said = decode(d, GY + 7, GX + 4, "Yes, make it a Cardinal", GRAY)
    expect(said == "Yes, make it a Cardinal",
           f"the yes stands unpicked beside it (read: {said!r})")

# The yes runs the making. The copy walks the whole
# image sector by sector from the stick; on this
# bench that is minutes, and the window's final word
# is awaited accordingly.
t0 = time.time()
d = press_yes("This computer is a Cardinal now.", 1500)
print(f"note: the making's word came after {time.time() - t0:.0f} seconds of pressing and waiting")
expect(d is not None, "the making finished and the window answered 'This computer is a Cardinal now.'")

done()
