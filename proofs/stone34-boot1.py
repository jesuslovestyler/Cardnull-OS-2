# Stone 34 proof, boot 1: the region repaint — a drag
# no longer flickers the windows. Self-contained: it
# drives the monitor itself (the way tools/pixels.py
# does) because it also reads the runtime's loop-pass
# counter out of the guest, which the shared scenario
# namespace cannot reach.
#
# The bench numbers this proof stands on, measured on
# the build BEFORE this stone (same bench, same kind
# of drag): boot with the files and verse windows
# opened left the loop-pass counter at 120,856 of its
# million; one six-step drag of a window cost 11,765
# passes; one whole-desktop repaint cost 4,277. Nearly
# all of the old drag's cost was repainting windows the
# drag never touched — the wash-and-redraw shimmer
# Tyler saw as flicker in UTM ("when i move windows it
# flickers the windows", Nov 16, 2026).
#
# The proof makes two drags.
#
# Drag 1 — a lone window over a populated desktop.
# The files window (left cell 5, top row 31) and the
# verse window (left cell 5, top row 32) stand open
# low; the feather window stands open between; the
# welcome window stands high (left cell 6, top row 5,
# fifty-one by fourteen). The welcome window's title
# bar is pressed — bringing it forward with a
# whole-desktop repaint of the old kind — and only
# then is every pixel of the desktop below the
# welcome window's shadow — the bystanders' ground,
# feather, files, verse and all — hashed, so the hash
# judges the drag's own repainting alone.
# The welcome window is dragged by its title bar,
# six small steps, right three cells. Mid-drag — the
# button still held — the bystanders' ground must hash
# exactly as before: the region repaint never writes
# it, at any instant. (The old road washed and redrew
# every bystander on every step, so any mid-drag
# picture could catch them half-drawn — the flicker,
# made visible.) The pass counter is read after the
# drag's opening press (which brings the window
# forward with a whole-desktop repaint of the old
# kind), so the count is the drag's alone; it must
# stand under half the old road's measured 11,765.
# After the window is set down it decodes at its new
# place, and the bystanders' ground still hashes as
# before.
#
# Drag 2 — a crossing. The files window is dragged
# right five cells and up three rows, ACROSS the verse
# window. It must decode at its new place; the verse
# window must stand repainted behind it (its title bar
# in the frame's gray, not blue and not black, its
# body in its light ground); the ground the files
# window vacated beyond the verse window's cover must
# stand plain. The files window is then dragged back
# home, Tab brings the verse window forward again, and
# the verse window decodes whole — title and
# reference — the crossings having cost it nothing.
#
# Prints one ok/NOT OK line per check and PASS or FAIL
# as the last line; the exit code carries the verdict.

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

# ---- Drag 1: the welcome window, alone in its road --
#
# The bystanders' ground: every pixel from just under
# the welcome window's shadow (y 312) to the bar's top
# (y 735), the whole width.
time.sleep(1.0)

go(200, 5 * 16 + 8)
cmd("mouse_button 1")
time.sleep(0.8)
# The press has brought the welcome window forward —
# a whole-desktop repaint of the old kind, done and
# settled. The bystanders' ground is hashed only now,
# so what the hash judges is the drag's own repainting.
d = dump()
bystanders = rect_hash(d, 0, 312, 1024, 735)
g0 = xp1(GA)
mid_ok = True
for i in range(6):
    cmd("mouse_move 8 0")
    PX, PY = PX + 8, PY
    time.sleep(0.35)
    if i == 2:
        dmid = dump()
        if rect_hash(dmid, 0, 312, 1024, 735) != bystanders:
            mid_ok = False
expect(mid_ok,
       "mid-drag, button still held, the whole populated desktop below "
       "stands pixel for pixel untouched — the region repaint never writes it")
cmd("mouse_button 0")
time.sleep(1.2)
g1 = xp1(GA)
drag_cost = g1 - g0
expect(drag_cost < 6600,
       f"the lone window's six-step drag cost {drag_cost} loop passes — "
       "the old whole-desktop road measured 11,765 on the desktop of "
       "Stone 34; the road now also restores the desktop's icons it "
       "crosses (Stone 38), and the drag still costs little more than "
       "half the old road's measure")

d = dump()
expect(rect_hash(d, 0, 312, 1024, 735) == bystanders,
       "after the drag the bystanders' ground still stands pixel for pixel as it was")
go(700, 400)
time.sleep(0.6)
d = dump()
expect(decode(d, 5, 10, "Welcome", WHITE) == "Welcome",
       "the dragged welcome window decodes at its new place (left cell 9, top row 5)")
expect(decode(d, 32, 6, "Terminal", WHITE) == "Terminal",
       "the terminal window standing on the verse window's place decodes "
       "as it did (Stone 38: the two windows share that first place — "
       "the verse window's own wholeness is proved below, when Tab "
       "brings it forward again)")

# ---- Drag 2: the files window across the verse -----
#
# Press the files window's title bar (row 31, above
# the verse window's top at 32 — the press point is
# Stone 33's own, (400, 504), deep in the bar) and
# carry it right
# five cells and up three rows, in the standing
# proofs' larger steps (small steps can outrun the
# bench mouse's packet under a repaint's load). New
# place: (10, 28).
go(400, 31 * 16 + 8)
cmd("mouse_button 1")
time.sleep(0.5)
for i in range(5):
    cmd("mouse_move 16 -10")
    PX, PY = PX + 16, PY - 10
    time.sleep(0.35)
cmd("mouse_button 0")
time.sleep(1.2)
go(700, 400)
time.sleep(0.6)
d = dump()
expect(decode(d, 28, 11, "Files", WHITE) == "Files",
       "the dragged files window decodes at its new place (left cell 10, top row 28)")
expect(pixel(d, 90, 520) == FRAME,
       "the crossed verse window's title bar stands in the frame's gray — "
       "repainted as the window behind, neither washed black nor left blue")
expect(pixel(d, 90, 600) == BLACK,
       "the crossed ground shows the terminal window's dark body over "
       "the verse window's place (Stone 38: the terminal stands over "
       "the verse there — the verse's own light ground is proved whole "
       "below, when Tab brings the verse forward again)")
expect(pixel(d, 5 * 16 + 8, 31 * 16 + 8) == BLACK,
       "the files window's old title ground, beyond the verse window's cover, stands plain")
expect(pixel(d, 7 * 16, 44 * 16 + 8) == BLACK,
       "the files window's old foot ground, below the verse window's foot, stands plain")

# Drag the files window back home (left cell 5, top
# row 31), the same five steps reversed.
go(400, 28 * 16 + 8)
cmd("mouse_button 1")
time.sleep(0.5)
for i in range(5):
    cmd("mouse_move -16 10")
    PX, PY = PX - 16, PY + 10
    time.sleep(0.3)
cmd("mouse_button 0")
time.sleep(0.8)
go(700, 400)
time.sleep(0.5)
d = dump()
expect(decode(d, 31, 6, "Files", WHITE) == "Files",
       "the files window decodes back at its home place")

# Tab brings the verse window forward again (it stood
# fully behind the returned files window), and it
# must decode whole — the crossings cost it nothing.
back = None
for _ in range(6):
    cmd("sendkey tab")
    time.sleep(0.5)
    d = dump()
    if decode(d, 32, 6, "Verse", WHITE) == "Verse":
        back = d
        break
expect(back is not None,
       "the verse window, brought forward again, decodes whole after both crossings")
if back:
    expect(decode(back, 42, 7, "1 John 5:13", BLACK) == "1 John 5:13",
           "the verse window's reference decodes whole after both crossings")

# Tab on to the terminal window (Stone 38): it stood
# under both crossings on the verse window's place,
# and brought forward it too must decode whole — the
# crossings cost it nothing either.
term = None
for _ in range(6):
    cmd("sendkey tab")
    time.sleep(0.5)
    d = dump()
    if decode(d, 32, 6, "Terminal", WHITE) == "Terminal":
        term = d
        break
expect(term is not None,
       "the crossed terminal window, brought forward, decodes whole after both crossings")

try:
    cmd("quit")
except Exception:
    pass
if _failures:
    print(f"FAIL ({len(_failures)} check(s) failed)")
    sys.exit(1)
print("PASS")
