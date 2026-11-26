# Stone 47 proof, boot 1: the terminal-drag census —
# the terminal's painter no longer writes outside its
# window. Self-contained: it drives the monitor itself
# (the way tools/pixels.py does).
#
# The shipped disc is booted at the BIOS door (the
# face of light), no disk fitted. The terminal stands
# open at its first place (left cell 5, top row 32).
# The word 'hello' is typed: its answer stands in the
# console's keeping at the answers' first row (33).
# The terminal is then dragged UP five rows by its
# title bar and dropped: the census after the drop
# reads the answer at the row the window's new top
# names (28), the title at the new top (27), and —
# after one more letter is typed — the typing line's
# prompt at the new typing row (39), with no prompt
# left standing at the old typing row (44) and no
# answer spilled at the rows below the dragged
# window's foot (42). The terminal is then dragged
# back down to its first place and the answer is read
# at row 33 again.
#
# Until this stone a move never laid the console's
# rows (the desk's 128, 132, 136) from the window's
# new place, so the terminal's painter went on laying
# its answers and its typing line at the FIRST place's
# rows — below the dragged window's foot, over ground,
# icons, and other windows, where no wash in the
# system could ever reach them (the second
# diagnosis's S1, frames B1 and B2). Every check here
# reads a row the defect displaced. (The bench's
# mouse can lose a packet under load and a drag fall
# short; each drag is retried, up to three takings,
# until the window has truly arrived — the census
# judges the place the drag reached.)
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


ANSWER = "Hello. It is good to see you."


def term_top(d):
    # The terminal window's top row, found by its
    # title — the title's words begin one cell in from
    # the window's left (cell 5), so at column 6.
    for row in range(16, 44):
        if decode(d, row, 6, "Terminal", WHITE) == "Terminal":
            return row
    return 0


d = waitdump(lambda d: d is not None and d[0] == 1024
             and count_color(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

typewrite("hello")
d = waitdump(lambda d: d is not None
             and decode(d, 33, 7, ANSWER, GRAY) == ANSWER, 25)
expect(d is not None,
       "the word 'hello' is answered at the first place's first row (33)")
d = settle()
expect(term_top(d) == 32,
       "the terminal stands at its first place (top row 32)")

# ---- The drag up five rows -------------------------
top = 32
for _try in range(3):
    if not press_takes_hold(400, top * 16 + 8, 500, top * 16 + 10):
        cmd("mouse_button 0")
        settle()
        continue
    for i in range(5):
        cmd("mouse_move 0 -16")
        PY -= 16
        settle()
    cmd("mouse_button 0")
    d = settle()
    top = term_top(d) if d else 0
    if top == 27:
        break
expect(top == 27,
       f"the terminal was truly dragged up five rows (it stands at top row {top})")

d = settle()
expect(decode(d, 27, 6, "Terminal", WHITE) == "Terminal",
       "after the drop the title stands at the new top (27)")
expect(decode(d, 28, 7, ANSWER, GRAY) == ANSWER,
       "after the drop the answer stands at the new first row (28) — "
       "the console's rows followed their window")
expect(decode(d, 42, 7, ANSWER, GRAY) != ANSWER,
       "no answer is spilled at the rows below the dragged window's foot (42)")

cmd("sendkey y")
time.sleep(0.5)
d = waitdump(lambda d: d is not None
             and decode(d, 39, 6, ">", LIGHT) == ">", 15)
expect(d is not None,
       "the typing prompt stands at the new typing row (39)")
d = settle()
expect(decode(d, 44, 6, ">", LIGHT) != ">",
       "no typing prompt is left standing at the old typing row (44)")

# ---- The drag back down ----------------------------
for _try in range(3):
    if not press_takes_hold(400, top * 16 + 8, 500, top * 16 + 10):
        cmd("mouse_button 0")
        settle()
        continue
    for i in range(5):
        cmd("mouse_move 0 16")
        PY += 16
        settle()
    cmd("mouse_button 0")
    d = settle()
    top = term_top(d) if d else 0
    if top == 32:
        break
expect(top == 32,
       f"the terminal was truly dragged back home (it stands at top row {top})")
d = settle()
expect(decode(d, 33, 7, ANSWER, GRAY) == ANSWER,
       "home again, the answer stands at the first row (33)")

try:
    cmd("quit")
except Exception:
    pass
if _failures:
    print(f"FAIL ({len(_failures)} check(s) failed)")
    sys.exit(1)
print("PASS")
