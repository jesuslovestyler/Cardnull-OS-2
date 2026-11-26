# Stone 47 proof, boot 3: the ground's invitation is
# whole — the desktop's own lines have a repaint owner
# at last. Self-contained: it drives the monitor
# itself (the way tools/pixels.py does).
#
# The shipped disc is booted at the BIOS door (the
# face of light), no disk fitted. At the rising the
# desktop's invitation stands on the ground at the
# layout's rows 11 and 12 (pixel rows 21 and 23):
# "Type a word, then press Enter:" and the words the
# typing answers to. Both lines are read whole — the
# first from its third cell, the Help icon's disc
# standing over its first letter, as at the rising.
#
# Then the welcome window (left cell 6, top row 5) is
# dragged down six rows — across both lines — and
# back up again, and dropped at its first place: both
# lines must read whole again. Then the word 'paint'
# opens the paint window, a press on the welcome
# window's body brings the welcome forward, and a
# fresh press inside the paint window's cells runs
# the region road over the paint window and the
# window it takes the forward place from — a road
# crossing both lines in the open ground between the
# two windows: after the press is let go, both lines
# must still read whole.
#
# Until this stone the invitation had no repaint
# owner: drawface laid it at the rising and nothing
# ever laid it again, so every wash that crossed it —
# a drag step's leaving ground, a region road's wash —
# rubbed it out in patches for the rest of the sitting
# (the second diagnosis's S2, frame B3). Now the
# ground has an owner, groundline: the whole repaint
# lays the lines after its closed windows' washes and
# before its icons, and the region repaint lays again
# the lines its road touches, with the windows
# standing over a touched line joining its set.
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


LINE0 = "ype a word, then press Enter:"
LINE1 = "hello time memory eastern utc feather welcome usb setup clear"


def lines_whole(d):
    return (decode(d, 21, 3, LINE0, LIGHT) == LINE0
            and decode(d, 23, 2, LINE1, LIGHT) == LINE1)


def welcome_top(d):
    for row in range(2, 24):
        if decode(d, row, 7, "Welcome", WHITE) == "Welcome":
            return row
    return 0


def click(x, y):
    go(x, y)
    cmd("mouse_button 1")
    time.sleep(0.4)
    cmd("mouse_button 0")
    time.sleep(0.4)


d = waitdump(lambda d: d is not None and d[0] == 1024
             and count_color(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")
d = settle()
expect(lines_whole(d),
       "at the rising the invitation's lines stand whole")

# The welcome window dragged down six rows, across
# both lines, and back up again.
top = 5
for _try in range(3):
    if not press_takes_hold(216, top * 16 + 8, 200, top * 16 + 10):
        cmd("mouse_button 0")
        settle()
        continue
    for i in range(6):
        cmd("mouse_move 0 16")
        PY += 16
        settle()
    cmd("mouse_button 0")
    d = settle()
    top = welcome_top(d) if d else 0
    if top == 11:
        break
expect(top == 11,
       f"the welcome window was truly dragged down six rows (it stands at top row {top})")
for _try in range(3):
    if not press_takes_hold(216, top * 16 + 8, 200, top * 16 + 10):
        cmd("mouse_button 0")
        settle()
        continue
    for i in range(6):
        cmd("mouse_move 0 -16")
        PY -= 16
        settle()
    cmd("mouse_button 0")
    d = settle()
    top = welcome_top(d) if d else 0
    if top == 5:
        break
expect(top == 5,
       f"the welcome window was truly dragged back home (it stands at top row {top})")
d = settle()
expect(lines_whole(d),
       "after the crossing drag the invitation's lines stand whole — "
       "the drop's whole repaint laid them again")

# The region road across the lines: the paint window
# opened, the welcome brought forward by a press on
# its body, then a fresh press in the paint window's
# cells.
typewrite("paint")
d = waitdump(lambda d: d is not None
             and decode(d, 32, 6, "Paint", WHITE) == "Paint", 25)
expect(d is not None, "the word 'paint' opens the paint window forward")
click(320, 160)
d = waitdump(lambda d: d is not None
             and decode(d, 5, 7, "Welcome", WHITE) == "Welcome", 15)
expect(d is not None,
       "a press on its body brings the welcome forward")
go(200, 648)
cmd("mouse_button 1")
time.sleep(1.0)
cmd("mouse_button 0")
d = settle()
expect(lines_whole(d),
       "after the crossing region road the invitation's lines stand "
       "whole — the region repaint laid the lines its road touched")

try:
    cmd("quit")
except Exception:
    pass
if _failures:
    print(f"FAIL ({len(_failures)} check(s) failed)")
    sys.exit(1)
print("PASS")
