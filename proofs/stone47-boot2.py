# Stone 47 proof, boot 2: the icon labels keep their
# paper — an icon's name is painted on the paper the
# icon itself sets. Self-contained: it drives the
# monitor itself (the way tools/pixels.py does).
#
# The shipped disc is booted at the BIOS door (the
# face of light), no disk fitted. At the rising, the
# name bands of the Files icon (row 2, its name's
# cells, columns 4 to 8) and the Settings icon (row
# 26, columns 4 to 11) are read: the band's pixels are
# counted by color, and the ground's black must be
# the band's dominant color with no blue pixel
# standing in it — the name's paper is the ground the
# icon stands on. Then the word 'hello' is typed and
# the terminal is dragged up two rows and dropped —
# the very sequence the second diagnosis's frame B5
# measured — and the bands are read again: the same
# black, the same absence of blue.
#
# Until this stone oneicon never set the paper its
# name is painted with: pixtext fills each letter's
# cell with the paper standing in the desk, and the
# labels inherited whatever the last painter before
# them had left standing — after the sequence above,
# the front chip's blue — so the labels changed color
# from pass to pass with no icon pressed at all. Now
# the icon sets its own paper (the ground's black)
# before its name, as every other painter in the
# system already set its own.
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


def click(x, y):
    go(x, y)
    cmd("mouse_button 1")
    time.sleep(0.4)
    cmd("mouse_button 0")
    time.sleep(0.4)


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


def band(d, prow, c0, c1):
    """(dominant color, blue count) over a name band's
    cells: the band's row, columns c0 to c1."""
    counts = {}
    blue = 0
    for y in range(prow * 16, prow * 16 + 16):
        for x in range(c0 * 16, (c1 + 1) * 16):
            c = pixel(d, x, y)
            counts[c] = counts.get(c, 0) + 1
            if c == BLUE:
                blue += 1
    dominant = max(counts.items(), key=lambda kv: kv[1])[0]
    return dominant, blue


ANSWER = "Hello. It is good to see you."


def term_top(d):
    for row in range(16, 44):
        if decode(d, row, 6, "Terminal", WHITE) == "Terminal":
            return row
    return 0


d = waitdump(lambda d: d is not None and d[0] == 1024
             and count_color(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")
d = settle()

dom, blue = band(d, 2, 4, 8)
expect(dom == BLACK and blue == 0,
       "at the rising the Files label's band is the ground's black, "
       "with no blue standing in it")
# The Settings label stands under the feather
# window's place at the rising (its title bar covers
# the label's row), so the feather window is closed
# first — a click on its close mark — and the label
# read in the open. The close is itself a repaint
# pass, so the label's paper is still proved against
# a pass's history.
click(920, 424)
d = settle()
dom, blue = band(d, 26, 4, 11)
expect(dom == BLACK and blue == 0,
       "with the feather window closed the Settings label's band is "
       "the ground's black, with no blue standing in it")

typewrite("hello")
d = waitdump(lambda d: d is not None
             and decode(d, 33, 7, ANSWER, GRAY) == ANSWER, 25)
expect(d is not None, "the word 'hello' is answered")

# The diagnosis's sequence: the terminal dragged up
# two rows and dropped.
top = 32
for _try in range(3):
    if not press_takes_hold(400, top * 16 + 8, 500, top * 16 + 10):
        cmd("mouse_button 0")
        settle()
        continue
    for i in range(2):
        cmd("mouse_move 0 -16")
        PY -= 16
        settle()
    cmd("mouse_button 0")
    d = settle()
    top = term_top(d) if d else 0
    if top == 30:
        break
expect(top == 30,
       f"the terminal was truly dragged up two rows (it stands at top row {top})")

d = settle()
dom, blue = band(d, 2, 4, 8)
expect(dom == BLACK and blue == 0,
       "after the drag the Files label's band is still the ground's "
       "black, with no blue standing in it")
dom, blue = band(d, 26, 4, 11)
expect(dom == BLACK and blue == 0,
       "after the drag the Settings label's band is still the ground's "
       "black, with no blue standing in it")

try:
    cmd("quit")
except Exception:
    pass
if _failures:
    print(f"FAIL ({len(_failures)} check(s) failed)")
    sys.exit(1)
print("PASS")
