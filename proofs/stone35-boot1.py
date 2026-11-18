#!/usr/bin/env python3
# Stone 35, boot 1: the calculator press. The
# calculator window is opened by its word on the
# quiet desktop, and one press on its 7 key runs the
# visit — the welcome window (open from the face's
# rising, high on the desktop, far from the
# calculator's ground) hashed before and after: the
# region repaint must never have written it. The
# feather window's opening is checked too: its
# visit's receiving already walks the region road.
#
# Bench discipline: this boot makes ONE pointer
# press. On this bench a second press after a
# feather-visit press is not reliable (the emulated
# pointer's button keeping desyncs across a long
# visit), so each press of Stone 35's proof stands
# in its own boot — boots 1 and 2 between them press
# the calculator and the paint canvas.

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


GA = guard_addr()

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count_color(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

typewrite("files")
typewrite("verse")
d = waitdump(lambda d: d is not None
             and decode(d, 32, 6, "Verse", WHITE) == "Verse", 25)
expect(d is not None, "the files and verse windows stand open low on the desktop")


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


# The welcome window's own ground: cols 5..57, rows
# 5..18 — the tall settings window's first place
# begins at row 20, below this ground, and nothing
# else stands above it.
W = (84, 84, 924, 300)

d = waitdump(lambda d: d is not None and d[0] == 1024
             and count_color(d, BLUE) > 5000, 40)
expect2(d is not None, "the desktop is drawn")


GP = guard_addr()


def passes():
    v = xp1(GP)
    return v if v is not None else -1


# Stand the desktop's other windows open first —
# feather, paint, files, verse, settings, editor,
# help — so the press below is measured against a
# full desktop: the old road repainted every one of
# them twice per press, the new road only the
# pressed window's own ground.
typewrite("feather")
d = waitdump(lambda d: d is not None
             and safedec(d, 26, 6, "Feather", WHITE) == "Feather", 25)
expect2(d is not None
        and safedec(d, 26, 6, "Feather", WHITE) == "Feather",
        "the feather window stands open, painted by its visit's region repaint")
typewrite("paint")
d = waitdump(lambda d: d is not None
             and safepix(d, 11, 16) == RED, 25)
expect2(d is not None and safepix(d, 11, 16) == RED,
        "the paint window stands with the feather's swatches painted")
for word in ("files", "verse", "settings", "editor", "help"):
    typewrite(word)
    time.sleep(1.2)

# The calculator last, so it stands forward. Its
# word typed, and typed again if the first typing
# was lost in the openings' settling (a person
# would type it again).
typewrite("calculator")
d = waitdump(lambda d: d is not None
             and safedec(d, 35, 9, "0", BLACK) == "0", 20)
if d is None or safedec(d, 35, 9, "0", BLACK) != "0":
    typewrite("calculator")
    d = waitdump(lambda d: d is not None
                 and safedec(d, 35, 9, "0", BLACK) == "0", 20)
expect2(d is not None and safedec(d, 35, 9, "0", BLACK) == "0",
        "the calculator window stands open on a full desktop, its sum's line at 0")
go(60, 60)
time.sleep(0.5)
d = dump()
h0 = rect_hash(d, *W)

# The boot's one press: the calculator's 7 key, its
# loop passes reckoned around it.
p0 = passes()
time.sleep(0.7)
p0 = passes()
click(*cell_center(13, 18))
go(60, 60)
d = waitdump(lambda d: d is not None
             and safedec(d, 35, 9, "7", BLACK) == "7", 15)
expect2(d is not None and safedec(d, 35, 9, "7", BLACK) == "7",
        "a press on the calculator's 7 key reckons 7")
time.sleep(1.3)
p1 = passes()
if d is None:
    d = dump()
cost = p1 - p0
expect2(0 < cost < 5700,
        f"the calculator press cost {cost} loop passes on a full desktop — "
        "the old road's same press measured 5,961-6,966 on this bench; the "
        "saving is the two whole-desktop repaints of the bystander windows "
        "that no longer happen (the visit itself is most of what remains)")
expect2(rect_hash(d, *W) == h0,
        "after the calculator press the welcome window stands exactly as "
        "it stood — the region repaint keeps it out of the press's road")

print("FAIL" if FAILS else "PASS", flush=True)
sys.exit(1 if FAILS else 0)
