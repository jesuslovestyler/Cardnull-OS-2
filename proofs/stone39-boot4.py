#!/usr/bin/env python3
# Stone 39, boot 4: the chips at large print, from a
# fitted keeping disk whose settings card carries
# the size byte 2 (large) — the desktop rises large,
# as Stone 28 lays it (forty-two cells across,
# thirty-two down, twenty-four-pixel cells; the bar
# at rows 30 and 31). Six windows are opened by
# their words, as in boot 2, and the bar's upper row
# fills before the last chip is laid: the
# terminal's chip goes on at the lower row's middle
# ground, where neither the bar's name at its left
# nor its clock at its right is disturbed — the
# laying's second row, which the usual size's wider
# bar never needs for these eight names.
#
# Bench discipline: this boot makes NO pointer
# press (see Stone 35's boot notes).

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

# ---- the large face's own reading (Stone 33's
# boot 2 discipline): the same letter shapes, drawn
# at three times size.

def cell_bitmap_lg(d, cx, cy, ink):
    rows = []
    for r in range(8):
        v = 0
        for c in range(8):
            if pixel(d, cx + 3 * c + 1, cy + 3 * r + 1) == ink:
                v |= 1 << (7 - c)
        rows.append(v)
    return tuple(rows)


def decode_lg(d, prow, pcol, text, ink):
    out = []
    for i in range(len(text)):
        bm = cell_bitmap_lg(d, (pcol + i) * 24, prow * 24, ink)
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


def safedec_lg(d, prow, pcol, text, ink):
    try:
        return decode_lg(d, prow, pcol, text, ink)
    except Exception:
        return ""


def chip_layout_lg(openwins):
    row, col = 0, 2
    out = {}
    for name, win in CHIPS:
        if win not in openwins:
            continue
        w = len(name)
        lim = 42 if row == 0 else 32
        if col + w > lim:
            row, col = 1, 10
        out[win] = (row, col)
        col += w + 1
    return out


def chip_read_lg(d, openwins, win):
    lay = chip_layout_lg(openwins)
    if win not in lay:
        return None
    row, col = lay[win]
    return safedec_lg(d, 30 + row, col, CHIPNAME[win], WHITE)


def chip_counts_lg(d, openwins, win):
    lay = chip_layout_lg(openwins)
    row, col = lay[win]
    name = CHIPNAME[win]
    blue = gray = 0
    for y in range((30 + row) * 24, (30 + row) * 24 + 24):
        for x in range(col * 24, (col + len(name)) * 24):
            p = pixel(d, x, y)
            if p == BLUE:
                blue += 1
            elif p == LIGHT:
                gray += 1
    return blue, gray


d = waitdump(lambda d: d is not None and d[0] == 1024
             and count_color(d, BLUE) > 5000, 40)
expect2(d is not None, "the desktop is drawn large")

d = waitdump(lambda d: d is not None
             and safedec_lg(d, 31, 2, "Cardnull", WHITE) == "Cardnull", 25)
expect2(d is not None, "the large desktop settles with its bar's name standing")

# Open six windows by their words, as in boot 2,
# waiting for each chip at the large measure.
OPEN = {10}
for word, win in (("files", 3), ("editor", 5), ("paint", 6),
                  ("verse", 7), ("help", 9), ("settings", 4)):
    OPEN = OPEN | {win}
    typewrite(word)
    d = waitdump(lambda d: d is not None
                 and chip_read_lg(d, OPEN, win) == CHIPNAME[win], 30)
    expect2(d is not None
            and chip_read_lg(d, OPEN, win) == CHIPNAME[win],
            f"the word '{word}' lays the {CHIPNAME[win]} chip on the large bar")

ALL2 = {3, 4, 5, 6, 7, 9, 10}
d = dump()
for win in (3, 5, 6, 7, 9, 4):
    expect2(chip_read_lg(d, ALL2, win) == CHIPNAME[win],
            f"the {CHIPNAME[win]} chip stands on the large bar's upper row")
expect2(chip_read_lg(d, ALL2, 10) == "Terminal",
        "the terminal's chip stands on the large bar's lower row — the upper row filled before it")
blue, gray = chip_counts_lg(d, ALL2, 4)
expect2(blue > gray,
        "the settings chip stands blue at the large size — its window stands forward")
blue, gray = chip_counts_lg(d, ALL2, 10)
expect2(gray > blue,
        "the terminal's chip stands gray on the lower row at the large size")
expect2(safedec_lg(d, 31, 2, "Cardnull", WHITE) == "Cardnull",
        "the large bar's name stands whole beside the lower row's chip")
expect2(safedec_lg(d, 31, 34, "19:00:", WHITE) == "19:00:",
        "the large bar's clock stands whole beyond the lower row's chip")

print("FAIL" if FAILS else "PASS", flush=True)
sys.exit(1 if FAILS else 0)
