# Stone 47 proof, boot 5: the files window's list is
# paid at the stroke's end — not per packet, mid-
# stroke. Self-contained: it drives the monitor itself
# (the way tools/pixels.py does).
#
# The shipped disc is booted at the BIOS door (the
# face of light) with a keeping disk fitted, prepared
# by prove-stone47.sh: a settings card (sector 8), an
# empty notes page (sector 64, count 0), and a picture
# header standing NOT kept (sector 80, kept byte 0).
# The word 'files' opens the files window (left cell
# 5, top row 31): its heading says no notes are kept,
# and no picture row stands in its list. The word
# 'paint' opens the paint window, which is dragged up
# to top row 6 so the two windows stand apart. A
# stroke is then painted — the button held down in
# the canvas and walked right — and MID-STROKE, the
# button still held and the stroke's presses all
# received, the files window's list must still show
# no picture row: the keeping has saved the picture
# (the desk's standing at 296 has turned), but the
# list's repaint is owed, not yet paid. When the
# button is let go, the owing is paid once: the
# picture's row stands in the list, "A picture you
# painted", at the window's last row (44), its words
# at column 9.
#
# Until this stone every press visit ran the region
# road over the paint window and, when a disk stood,
# over the files window with it — the list repainted
# per packet, mid-stroke (the second diagnosis's S4).
# Now a press visit repaints its own window directly,
# the list's owing is remembered, and the button's
# letting go pays it with one region road over the
# files window alone.
#
# Prints one ok/NOT OK line per check and PASS or FAIL
# as the last line; the exit code carries the verdict.

import hashlib
import os
import socket
import sys
import time

SOCK = sys.argv[1]
DUMP = sys.argv[2]

BLUE = (0, 0, 170)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FRAME = (85, 85, 85)
LIGHT = (170, 170, 170)
GRAY = (170, 170, 170)

_vals = {}
for _m in __import__("re").finditer(r"block\[(\d+)\] = (\d+)",
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


# ---- the monitor client (the pixels.py discipline) --

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
for _ in range(100):
    try:
        sock.connect(SOCK)
        break
    except OSError:
        time.sleep(0.2)
sock.settimeout(10)
_buf = b""


def _until_prompt():
    global _buf
    while b"(qemu)" not in _buf:
        c = sock.recv(4096)
        if not c:
            raise IOError("closed")
        _buf += c
    out, _buf = _buf.decode(errors="replace"), b""
    return out


_until_prompt()


def cmd(t):
    sock.sendall(t.encode() + b"\n")
    return _until_prompt()


def dump():
    for _ in range(3):
        cmd(f"screendump {DUMP}")
        time.sleep(0.15)
        with open(DUMP, "rb") as f:
            data = f.read()
        parts = data.split(b"\n", 3)
        if len(parts) < 4:
            continue
        dims = parts[1].split()
        w, h = int(dims[0]), int(dims[1])
        if len(parts[3]) >= w * h * 3:
            return w, h, parts[3]
        time.sleep(0.2)
    return w, h, parts[3]


def pixel(d, x, y):
    w, h, px = d
    o = (y * w + x) * 3
    return px[o], px[o + 1], px[o + 2]


def count_color(d, rgb):
    w, h, px = d
    n = 0
    for i in range(0, w * h * 3, 3):
        if px[i] == rgb[0] and px[i + 1] == rgb[1] and px[i + 2] == rgb[2]:
            n += 1
    return n


def waitdump(fn, secs=30):
    end = time.time() + secs
    last = None
    while time.time() < end:
        try:
            last = dump()
        except (IOError, OSError):
            last = None
        if last and fn(last):
            return last
        time.sleep(0.4)
    return None


PX, PY = 506, 378


def go(x, y):
    # Paced the pixels.py way — a small step and a
    # pause for each, so the guest's mouse queue is
    # never outrun and the pointer truly stands where
    # this reckoning believes it does.
    global PX, PY
    while PX != x or PY != y:
        dx = max(-64, min(64, x - PX))
        dy = max(-64, min(64, y - PY))
        cmd(f"mouse_move {dx} {dy}")
        PX, PY = PX + dx, PY + dy
        time.sleep(0.25)


def typewrite(text):
    for ch in text:
        cmd(f"sendkey {ch}")
        time.sleep(0.12)
    cmd("sendkey ret")
    time.sleep(0.5)


_failures = []


def expect(cond, why):
    if cond:
        print(f"ok: {why}")
    else:
        print(f"NOT OK: {why}")
        _failures.append(why)
    return cond


def rect_hash(d, x0, y0, x1, y1):
    w, h, px = d
    m = hashlib.sha256()
    for y in range(y0, y1):
        o = (y * w + x0) * 3
        m.update(px[o:o + (x1 - x0) * 3])
    return m.hexdigest()


def settle(secs=12):
    time.sleep(0.5)
    end = time.time() + secs
    prev = None
    same = 0
    last = None
    while time.time() < end:
        try:
            last = dump()
        except (IOError, OSError):
            last = None
        if last is not None:
            h = rect_hash(last, 0, 0, 1024, 736)
            if h == prev:
                same += 1
                if same >= 2:
                    return last
            else:
                same = 0
            prev = h
        time.sleep(0.3)
    return last


def press_takes_hold(x, y, barx, bary):
    go(x, y)
    cmd("mouse_button 1")
    end = time.time() + 8
    while time.time() < end:
        time.sleep(0.4)
        try:
            d = dump()
        except (IOError, OSError):
            d = None
        if d is not None and pixel(d, barx, bary) == BLUE:
            return True
    return False


PIC = "A picture you painted"
HEADING = "No notes are kept on the disk yet."


def picrow(d):
    """The picture's row stands in the files list if
    its words decode at the window's last row — in
    white when the row stands picked (it does here:
    no note stands before it), in light gray when
    not."""
    return (decode(d, 44, 9, PIC, WHITE) == PIC
            or decode(d, 44, 9, PIC, LIGHT) == PIC)


def paint_top(d):
    for row in range(2, 40):
        if decode(d, row, 6, "Paint", WHITE) == "Paint":
            return row
    return 0


d = waitdump(lambda d: d is not None and d[0] == 1024
             and count_color(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

typewrite("files")
d = waitdump(lambda d: d is not None
             and (decode(d, 33, 7, HEADING, GRAY) == HEADING
                  or decode(d, 33, 7, HEADING, WHITE) == HEADING), 25)
expect(d is not None,
       "the files window opens on the empty keeping disk")
expect(d is not None and not picrow(d),
       "no picture row stands in the list yet")

typewrite("paint")
d = waitdump(lambda d: d is not None
             and decode(d, 32, 6, "Paint", WHITE) == "Paint", 25)
expect(d is not None, "the word 'paint' opens the paint window forward")

# The paint window dragged up to top row 6, clear of
# the files window below — in the standing proofs'
# larger steps (small steps can outrun the bench
# mouse's packet under a repaint's load).
top = 32
for _try in range(3):
    if not press_takes_hold(400, top * 16 + 8, 500, top * 16 + 10):
        cmd("mouse_button 0")
        settle()
        continue
    for dy in [-64, -64, -64, -64, -64, -64, -32]:
        cmd(f"mouse_move 0 {dy}")
        PY += dy
        settle()
    cmd("mouse_button 0")
    d = settle()
    top = paint_top(d) if d else 0
    if top == 6:
        break
expect(top == 6,
       f"the paint window was truly dragged up to top row 6 (it stands at {top})")
d = settle()
expect(not picrow(d), "the files list still shows no picture row")

# The stroke: down in the canvas at the center of
# feather cell (16, 20) — window row 14, column 12 —
# and walked right while held. The first painted
# cell makes the keeping save the picture.
go(200, 232)
cmd("mouse_button 1")
time.sleep(0.6)
for x in [264, 328, 392]:
    go(x, 232)
    time.sleep(0.4)
d = dump()
if d is None:
    d = waitdump(lambda dd: dd is not None, 20)
expect(d is not None and not picrow(d),
       "mid-stroke the files list still shows no picture row — "
       "the repaint is owed, not yet paid")
cmd("mouse_button 0")
d = waitdump(lambda d: d is not None and picrow(d), 20)
expect(d is not None,
       "at the stroke's end the picture's row stands in the list — "
       "the owing paid once, where the button was let go")

try:
    cmd("quit")
except Exception:
    pass
if _failures:
    print(f"FAIL ({len(_failures)} check(s) failed)")
    sys.exit(1)
print("PASS")
