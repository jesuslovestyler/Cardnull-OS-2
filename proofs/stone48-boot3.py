# Stone 48 proof, boot 3: the kept picture across a
# reboot, and the drag. The disk is boot 1's — the
# picture drawn there stands kept on it, and nothing
# in this boot paints anything: the word 'picture'
# opens the window on the picture the disk's keeping
# alone carried through the reboot, and the same
# cells stand in it (the Red cell's block, the Blue
# cell's block, at the window's own big measure).
# Then the window is dragged by its title bar, three
# cells right and two rows up, on Stone 47's healed
# roads: after the drop the title stands at the new
# place and the picture stands whole there — the
# same blocks at the new origin, nothing of the
# picture left at the old place. A press on the
# close mark at the new place closes it.
#
# The drag is attempted the way Stone 47's proof
# attempts it — the hold taken on the bar, the moves
# stepped a cell at a time, up to three tries. The
# bench's emulated PS/2 mouse has refused held drags
# before, on unmodified trees as readily as on new
# ones; if it refuses here, the drag checks below
# fail on this bench and the stone's record says so
# plainly. The drag is Tyler's to witness in UTM, as
# every drag has been.

import re

BLUE = (0, 0, 170)
RED = (170, 0, 0)
DBLUE = (0, 0, 170)
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


# The picture window's first place: left cell 7, top
# row 30, fifty wide, sixteen high (its painter's
# reckoning). Its drawing stands one cell in from
# its left edge and under its title bar: canvas cell
# (row, col) stands at block column col - 16, block
# row row - 14, each block sixteen wide, thirty-two
# tall.
PX, PY = 7, 30


def pic_block_center(left, top, row, col):
    x = left * 16 + 16 + (col - 16) * 16 + 8
    y = top * 16 + 16 + (row - 14) * 32 + 16
    return (x, y)


def find_picture(d):
    """The picture window's place, found by its title
    — the title's words begin one cell in from the
    window's left, on its top row."""
    if d is None:
        return None
    for top in range(20, 40):
        for left in range(2, 20):
            if decode(d, top, left + 1, "Picture", WHITE) == "Picture":
                return (left, top)
    return None


d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

typewrite("picture")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, PY, PX + 1, "Picture", WHITE) == "Picture", 25)
expect(d is not None, "the word 'picture' opened the picture window")
if d:
    x, y = pic_block_center(PX, PY, 16, 30)
    expect(pixel(d, x, y) == RED,
           "the Red cell stands in the window from the disk's keeping alone")
    x, y = pic_block_center(PX, PY, 15, 20)
    expect(pixel(d, x, y) == DBLUE,
           "the Blue cell stands in the window from the disk's keeping alone")

# ---- The drag: three cells right, two rows up ------
TX, TY = PX + 3, PY - 2
place = (PX, PY)
for _try in range(3):
    d = dump()
    found = find_picture(d)
    if found:
        place = found
    if place == (TX, TY):
        break
    left, top = place
    move_to(left * 16 + 200, top * 16 + 8)
    mousebutton(1)
    time.sleep(0.6)
    steps_x = (TX - left) * 16
    steps_y = (TY - top) * 16
    while steps_x > 0:
        mousemove(16, 0)
        CUR[0] += 16
        steps_x -= 16
        time.sleep(0.5)
    while steps_y < 0:
        mousemove(0, -16)
        CUR[1] -= 16
        steps_y += 16
        time.sleep(0.5)
    mousebutton(0)
    time.sleep(1.5)
    d = dump()
    found = find_picture(d)
    if found:
        place = found

expect(place == (TX, TY),
       f"the picture window was truly dragged to its new place "
       f"(it stands at left {place[0]}, top {place[1]}; want {TX}, {TY})")
park()
time.sleep(0.8)
d = dump()
if d and place == (TX, TY):
    expect(decode(d, TY, TX + 1, "Picture", WHITE) == "Picture",
           "after the drop the title stands at the new top")
    x, y = pic_block_center(TX, TY, 16, 30)
    expect(pixel(d, x, y) == RED,
           "the Red cell followed the drag whole, at the new origin")
    x, y = pic_block_center(TX, TY, 15, 20)
    expect(pixel(d, x, y) == DBLUE,
           "the Blue cell followed the drag whole, at the new origin")
    x, y = pic_block_center(PX, PY, 16, 30)
    expect(pixel(d, x, y) != RED,
           "nothing of the picture is left standing at the old place")

# A press on the close mark at the window's standing
# place closes it.
left, top = place
click((left + 50 - 2) * 16 + 8, top * 16 + 8)
park()
d = waitdump(lambda d: d is not None
             and find_picture(d) is None, 15)
expect(d is not None, "a press on the picture window's close mark closed it")

done()
