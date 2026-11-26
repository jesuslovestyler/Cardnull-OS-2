# Stone 47 proof, boot 4: a press visit writes only
# in its own window — the road wash that was the
# paint and calculator flicker is gone. Self-contained:
# it drives the monitor itself (the way tools/pixels.py
# does).
#
# The shipped disc is booted at the BIOS door (the
# face of light), no disk fitted. The word 'paint'
# opens the paint window (left cell 5, top row 32,
# fifty-four by fourteen — pixel columns 80 to 944,
# rows 512 to 736). A stroke is then painted: the
# button goes down inside the canvas and the pointer
# walks right in five steps, the button held
# throughout. A band around the window — everything
# above it, the ground left of it, the ground right
# of it — is hashed from the frame where the held
# press first stands settled, and after EVERY step a
# fresh frame's band must hash the same: no press
# visit writes outside its window, at any sampled
# instant, and the window's own title must decode in
# every sampled frame — it is never washed away and
# redrawn. After the button is let go, the canvas
# inside the window must differ from before the
# stroke (the stroke landed), and the band must
# still stand as it was.
#
# Then the word 'calculator' opens the calculator at
# the same place, its '7' key is pressed (the key's
# cell center, as proofs/stone30-boot1.py reckons
# it), and the same band must stand unchanged across
# the press, with the '7' standing in the sum's line
# (read the way stone30's proof reads it).
#
# Until this stone every carried press ended its
# visit in the region road over the window's whole
# place: the road washed the place black and
# repainted the window whole — and every bystander
# its closure gathered — many times a second for one
# cell's change; the flicker Tyler saw while painting
# was the wash (the second diagnosis's S4). Now a
# press visit repaints its window directly by its own
# painter when the window stands forward, and no road
# is washed. The band checks here verify the positive
# guarantee on the healed tree — that nothing outside
# the window is written at any sampled instant — and
# the title checks verify the window is never left
# washed mid-stroke; the deferral proof (boot 5) is
# the one that catches the old road red-handed, at
# the files window's list.
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


def band(d):
    """The ground around the low windows' place:
    everything above pixel row 512, the strip left of
    column 80, and the strip right of column 944 down
    to the bar. The mouse arrow stands inside the
    window throughout, so it never enters the band."""
    return (rect_hash(d, 0, 0, 1024, 512),
            rect_hash(d, 0, 512, 80, 736),
            rect_hash(d, 944, 512, 1024, 736))


def sumline(d):
    """The calculator's sum line as it stands, read
    the way proofs/stone30-boot1.py reads it: across
    its whole span at row 35 from column 8, an empty
    cell read as the space it is, the trailing
    emptiness trimmed away."""
    out = []
    for i in range(48):
        bm = cell_bitmap(d, (9 + i) * 16, 35 * 16, BLACK)
        if all(v == 0 for v in bm):
            out.append(" ")
            continue
        best, bestd = None, 999
        for code, g in GLYPHS.items():
            dist = sum(bin(a ^ b).count("1") for a, b in zip(bm, g))
            if dist < bestd:
                bestd, best = dist, code
        out.append(chr(best) if bestd <= 2 else "?")
    return "".join(out).rstrip()


d = waitdump(lambda d: d is not None and d[0] == 1024
             and count_color(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

typewrite("paint")
d = waitdump(lambda d: d is not None
             and decode(d, 32, 6, "Paint", WHITE) == "Paint", 25)
expect(d is not None, "the word 'paint' opens the paint window forward")
d = settle()
inside_before = rect_hash(d, 96, 528, 928, 720)

# The stroke: down inside the canvas at the center
# of feather cell (16, 20), then right in five steps,
# the button held. The held baseline is the first
# frame whose band stands settled with the button
# down — the fresh press's own repaint (the road
# that brings a press in a behind window forward, a
# click path this stone does not touch) has finished
# by then, and from there no step may write outside.
go(200, 648)
cmd("mouse_button 1")
base = None
prev = None
for _ in range(30):
    d = dump()
    if d is None:
        continue
    cur = band(d)
    if cur == prev:
        base = cur
        break
    prev = cur
    time.sleep(0.3)
expect(base is not None, "the held press's band settles")
for step, x in enumerate([264, 328, 392, 456, 520]):
    go(x, 648)
    time.sleep(0.3)
    d = dump()
    if d is None:
        d = waitdump(lambda dd: dd is not None, 20)
    expect(d is not None and band(d) == base,
           f"stroke step {step + 1} writes nothing outside the window")
    expect(d is not None
           and decode(d, 32, 6, "Paint", WHITE) == "Paint",
           f"stroke step {step + 1} leaves the window's title standing "
           "— never washed away and redrawn")
cmd("mouse_button 0")
d = settle()
expect(rect_hash(d, 96, 528, 928, 720) != inside_before,
       "the stroke landed inside the canvas")
expect(band(d) == base,
       "the band stands unchanged after the stroke")

# The calculator at the same place: its '7' key, at
# the center of feather cell (13, 18).
typewrite("calculator")
d = waitdump(lambda d: d is not None
             and decode(d, 32, 6, "Calculator", WHITE) == "Calculator",
             25)
expect(d is not None,
       "the word 'calculator' opens the calculator forward")
d = settle()
base = band(d)
go(168, 600)
cmd("mouse_button 1")
time.sleep(1.0)
d = dump()
if d is None:
    d = waitdump(lambda dd: dd is not None, 20)
expect(d is not None and band(d) == base,
       "the key press writes nothing outside the window")
expect(d is not None
       and decode(d, 32, 6, "Calculator", WHITE) == "Calculator",
       "the key press leaves the window's title standing")
cmd("mouse_button 0")
d = waitdump(lambda d: d is not None and sumline(d) == "7", 15)
expect(d is not None, "the '7' stands in the sum's line")
d = settle()
expect(band(d) == base,
       "the band stands unchanged after the key press")

try:
    cmd("quit")
except Exception:
    pass
if _failures:
    print(f"FAIL ({len(_failures)} check(s) failed)")
    sys.exit(1)
print("PASS")
