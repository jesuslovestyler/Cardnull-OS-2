#!/usr/bin/env python3
# Stone 38, boot 1: the desktop itself — its icons stand with their names, the terminal window stands open from the rising with the typing line at its foot, and one press on the Files icon opens the files window.
#
# Bench discipline: this boot makes at most ONE
# pointer press (see Stone 35's boot notes).

import hashlib
import os
import re
import socket
import subprocess
import sys
import time

SOCK = sys.argv[1]
DUMP = sys.argv[2]
REPO = os.getcwd()

BLUE = (0, 0, 170)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FRAME = (85, 85, 85)
LIGHT = (170, 170, 170)
RED = (170, 0, 0)
GRAY = (119, 119, 119)

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
    cmd(f"screendump {DUMP}")
    with open(DUMP, "rb") as f:
        data = f.read()
    parts = data.split(b"\n", 3)
    dims = parts[1].split()
    return int(dims[0]), int(dims[1]), parts[3]


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


def xp1(addr):
    out = cmd(f"xp /1gx {addr:#x}")
    toks = [t for t in out.replace(":", " ").split() if t.startswith("0x")]
    return int(toks[-1], 16)


def guard_addr():
    nm = subprocess.run(["nm", "build/cardnull.elf"], cwd=REPO,
                        capture_output=True, text=True).stdout
    for ln in nm.splitlines():
        p = ln.split()
        if len(p) == 3 and p[2] == "__guard_passes":
            return int(p[0], 16)
    raise RuntimeError("no __guard_passes in the built kernel")


PX, PY = 506, 378


def go(x, y):
    global PX, PY
    while PX != x or PY != y:
        dx = max(-200, min(200, x - PX))
        dy = max(-200, min(200, y - PY))
        cmd(f"mouse_move {dx} {dy}")
        PX, PY = PX + dx, PY + dy


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


FAILS = []


def expect2(cond, msg):
    print(("ok: " if cond else "NOT OK: ") + msg, flush=True)
    if not cond:
        FAILS.append(msg)


def click(x, y):
    # One single-jump move from the tracked place, as
    # Stone 26's driver moves: the stepped road loses
    # presses on this bench, the single jump lands.
    global PX, PY
    cmd(f"mouse_move {x - PX} {y - PY}")
    PX, PY = x, y
    time.sleep(0.3)
    cmd("mouse_button 1")
    time.sleep(0.5)
    cmd("mouse_button 0")
    time.sleep(0.4)


def cell_center(row, col):
    """The screen pixel at the center of the feather
    cell (row, col), as the window carries it 1:1."""
    return ((col - 8) * 16 + 8, (row + 24) * 16 + 8)


def cell_pixel(d, row, col):
    x, y = cell_center(row, col)
    return pixel(d, x, y)


def safedec(d, prow, pcol, text, ink):
    # A screendump caught while the monitor is still
    # writing it is short — read it as "not yet",
    # never as a crash.
    try:
        return decode(d, prow, pcol, text, ink)
    except Exception:
        return ""


def safepix(d, row, col):
    try:
        return cell_pixel(d, row, col)
    except Exception:
        return None



FAILS = []


def expect2(cond, msg):
    print(("ok: " if cond else "NOT OK: ") + msg, flush=True)
    if not cond:
        FAILS.append(msg)


def click(x, y):
    global PX, PY
    cmd(f"mouse_move {x - PX} {y - PY}")
    PX, PY = x, y
    time.sleep(0.3)
    cmd("mouse_button 1")
    time.sleep(0.5)
    cmd("mouse_button 0")
    time.sleep(0.4)


def safedec(d, prow, pcol, text, ink):
    try:
        return decode(d, prow, pcol, text, ink)
    except Exception:
        return ""


def enter():
    sendkey("ret")
    time.sleep(0.4)


# The terminal window's place at the words' usual
# size: left 5, top 32, fifty-four wide, fourteen
# high; its answers begin at row 33, two cells in;
# its typing line stands at row 44.
TELEFT = 5
TETOP = 32

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count_color(d, BLUE) > 5000, 40)
expect2(d is not None, "the desktop is drawn — the boot arrives at the desktop itself, with no shell face before it")

# Settle on the terminal's prompt: the desktop's
# ground turns blue before the windows are painted,
# so the standing checks wait for the console's own
# mark at the window's foot.
d = waitdump(lambda d: d is not None
             and safedec(d, 44, TELEFT + 1, ">", LIGHT) == ">", 25)
expect2(d is not None, "the desktop settles with its windows painted")
d = dump()
# The desktop's icons stand down its left edge, with
# their plain names.
# The desktop's icons stand down its left edge, with
# their plain names. The welcome and feather windows
# stand over the middle icons' names at the rising —
# a window stands over the icons it covers, as on
# any desktop — so the names checked here are the
# ones standing in the clear (Files at the top, Help
# below the welcome window), and the Terminal icon
# is known by its picture: its black box stands at
# the edge where the ground would else be blue.
expect2(safedec(d, 2, 4, "Files", WHITE) == "Files",
        "the Files icon stands on the desktop with its name")
expect2(safedec(d, 22, 4, "Help", WHITE) == "Help",
        "the Help icon stands on the desktop with its name")
expect2(pixel(d, 24, 30 * 16 + 8) == BLACK
        and pixel(d, 24, 29 * 16 + 8) == BLACK,
        "the Terminal icon's picture stands on the desktop at the left edge")

# The terminal window stands open from the rising:
# its interior stands black at its place, and the
# typing line's prompt mark stands at its foot.
inner = all(pixel(d, (TELEFT + 3) * 16 + 8, r * 16 + 8) == BLACK
            for r in (34, 38, 42))
expect2(inner, "the terminal window stands open on the desktop, its interior dark at its place")
expect2(safedec(d, 44, TELEFT + 1, ">", LIGHT) == ">",
        "the typing line's prompt stands at the terminal window's foot — the console lives in the window")

# The boot's one press: the Files icon. The files
# window opens, forward, exactly as its word opens it.
click(40, 40)
d = waitdump(lambda d: d is not None
             and safedec(d, 31, 6, "Files", WHITE) == "Files", 20)
expect2(d is not None and safedec(d, 31, 6, "Files", WHITE) == "Files",
        "a press on the Files icon opens the files window, standing forward")

print("FAIL" if FAILS else "PASS", flush=True)
sys.exit(1 if FAILS else 0)
