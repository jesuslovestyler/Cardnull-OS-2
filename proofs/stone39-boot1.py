#!/usr/bin/env python3
# Stone 39, boot 1: the bar's chips at the rising and
# as windows open, and one press that raises. At the
# rising the terminal — the one chip-window standing
# open — carries the bar's only chip, standing
# behind (the welcome window stands forward, and it
# keeps no chip). The word 'files' opens the files
# window forward: its chip stands first on the bar,
# blue, and the terminal's chip moves along, gray.
# The word 'verse' brings the verse window forward:
# the blue moves to its chip. Then the boot's one
# press lands on the files chip, and the files
# window comes forward again — its title bar blue
# where it stood gray, its chip blue where the
# verse window's stood blue a moment before.
#
# Bench discipline: this boot makes at most ONE
# pointer press (see Stone 35's boot notes).

import hashlib
import os
import re
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
SHEEN = (154, 214, 222)

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


PX, PY = 506, 378


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


def typewrite(text):
    for ch in text:
        cmd(f"sendkey {ch}")
        time.sleep(0.12)
    cmd("sendkey ret")
    time.sleep(0.5)


def safedec(d, prow, pcol, text, ink):
    # A screendump caught while the monitor is still
    # writing it is short — read it as "not yet",
    # never as a crash.
    try:
        return decode(d, prow, pcol, text, ink)
    except Exception:
        return ""


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


# ---- the bar's chips, reckoned as the kernel reckons
# them (chipplace in src/cardnull.nifla): the eight
# windows in the icons' order, packed from the bar's
# upper row (row 46) at its second cell, one blank
# cell between chips, going on at the lower row
# (row 47) at its tenth cell when the upper row
# fills, the lower row ending where the clock's
# ground begins (column 24 at this size).

CHIPS = (("Files", 3), ("Editor", 5), ("Paint", 6),
         ("Calculator", 8), ("Verse", 7), ("Help", 9),
         ("Settings", 4), ("Terminal", 10))
CHIPNAME = {win: name for name, win in CHIPS}


def chip_layout(openwins):
    row, col = 0, 2
    out = {}
    for name, win in CHIPS:
        if win not in openwins:
            continue
        w = len(name)
        lim = 64 if row == 0 else 24
        if col + w > lim:
            row, col = 1, 10
        out[win] = (row, col)
        col += w + 1
    return out


def chip_read(d, openwins, win):
    """The chip's name as it stands on the bar, or
    None when the window has no chip in this laying."""
    lay = chip_layout(openwins)
    if win not in lay:
        return None
    row, col = lay[win]
    return safedec(d, 46 + row, col, CHIPNAME[win], WHITE)


def chip_counts(d, openwins, win):
    """(blue, light-gray) pixel counts in the chip's
    plate: the front window's chip stands white on
    blue, a window behind white on light gray — the
    plate's own colors tell which stands forward."""
    lay = chip_layout(openwins)
    row, col = lay[win]
    name = CHIPNAME[win]
    blue = gray = 0
    for y in range((46 + row) * 16, (46 + row) * 16 + 16):
        for x in range(col * 16, (col + len(name)) * 16):
            p = pixel(d, x, y)
            if p == BLUE:
                blue += 1
            elif p == LIGHT:
                gray += 1
    return blue, gray


def chip_front(d, openwins, win):
    blue, gray = chip_counts(d, openwins, win)
    return blue > gray


def chip_behind(d, openwins, win):
    blue, gray = chip_counts(d, openwins, win)
    return gray > blue

# The files window's place at the words' usual size:
# left 5, top 30 (top 31 until Stone 49 grew the
# window by its exchange row) — its title bar's
# blue-or-gray tells at (200, 490) whether it stands
# forward, a point
# the verse window (top row 32) never covers.
d = waitdump(lambda d: d is not None and d[0] == 1024
             and count_color(d, BLUE) > 5000, 40)
expect2(d is not None, "the desktop is drawn")

d = waitdump(lambda d: d is not None
             and safedec(d, 44, 6, ">", LIGHT) == ">", 25)
expect2(d is not None, "the desktop settles with its windows painted")
d = dump()

# At the rising: the terminal's chip alone, behind.
OPEN = {10}
expect2(chip_read(d, OPEN, 10) == "Terminal",
        "at the rising the bar carries the terminal's chip, the one chip-window open")
expect2(chip_behind(d, OPEN, 10),
        "the terminal's chip stands behind at the rising — the welcome window stands forward")

# The word 'files': the files window opens forward,
# its chip first and blue, the terminal's moved
# along behind it.
typewrite("files")
d = waitdump(lambda d: d is not None
             and chip_read(d, {3, 10}, 3) == "Files", 25)
expect2(d is not None and chip_read(d, {3, 10}, 3) == "Files",
        "the word 'files' lays the files chip first on the bar")
expect2(chip_read(d, {3, 10}, 10) == "Terminal",
        "the terminal's chip stands beside it, moved along")
expect2(chip_front(d, {3, 10}, 3),
        "the files chip stands blue — its window stands forward")
expect2(chip_behind(d, {3, 10}, 10),
        "the terminal's chip stands gray — its window stands behind")

# The word 'verse': the verse window comes forward
# and the blue moves to its chip.
typewrite("verse")
d = waitdump(lambda d: d is not None
             and chip_read(d, {3, 7, 10}, 7) == "Verse"
             and chip_front(d, {3, 7, 10}, 7), 25)
expect2(d is not None and chip_read(d, {3, 7, 10}, 7) == "Verse",
        "the word 'verse' lays its chip between the files and terminal chips")
expect2(chip_front(d, {3, 7, 10}, 7),
        "the verse chip stands blue — its window stands forward")
expect2(chip_behind(d, {3, 7, 10}, 3),
        "the files chip stands gray again — its window stands behind")
expect2(pixel(d, 200, 490) == FRAME,
        "the files window's title bar stands gray while it stands behind")

h_title = rect_hash(d, 80, 480, 944, 496)

# The boot's one press: the files chip (the bar's
# upper row, its plate at columns 2 to 6).
click(72, 744)
d = waitdump(lambda d: d is not None
             and pixel(d, 200, 490) == BLUE, 20)
expect2(d is not None and pixel(d, 200, 490) == BLUE,
        "a press on the files chip raises the files window — its title bar stands blue")
expect2(rect_hash(d, 80, 480, 944, 496) != h_title,
        "the files window's title row changed as it came forward")
expect2(chip_front(d, {3, 7, 10}, 3),
        "the files chip stands blue after the press — the front chip moved")
expect2(chip_behind(d, {3, 7, 10}, 7),
        "the verse chip stands gray after the press — its window stands behind again")
expect2(safedec(d, 30, 6, "Files", WHITE) == "Files",
        "the raised files window stands whole, its title reading at its place")

print("FAIL" if FAILS else "PASS", flush=True)
sys.exit(1 if FAILS else 0)
