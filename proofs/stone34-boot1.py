# Stone 34 proof, boot 1: the region repaint — a drag
# no longer flickers the windows. Self-contained: it
# drives the monitor itself (the way tools/pixels.py
# does).
#
# Restored at Stone 45. As first written, this proof
# also read the runtime's loop-pass counter out of
# the guest through the monitor, from a global cell
# the compiler then laid in the kernel under the name
# __guard_passes, and held the drag's cost under half
# the old road's measured 11,765 passes. The compiler
# no longer lays that cell in the kernel — each loop's
# guard now stands in the loop's own frame, and the
# global cell survives only in the feather runtime's
# data — so the number has nothing honest left to
# read. The property the number stood for is checked
# here directly instead, and more strongly: the
# bystanders' ground is hashed after EVERY step of
# the first drag, not once in its middle, and must
# stand pixel for pixel untouched at every instant —
# a drag that washed and redrew its bystanders, the
# flicker itself, would be caught at the step that
# did it. Stone 45 also adds the dragged window's own
# wholeness after the drop: a census of its body's
# interior (no frame-gray may stand there — the gray
# body of Tyler's witness was the frame's undercoat
# left showing) and a decoding of all five of its
# lines.
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
# whole-desktop repaint — and only then is every
# pixel of the desktop below the welcome window's
# shadow — the bystanders' ground, feather, files,
# verse and all — hashed, so the hash judges the
# drag's own repainting alone. The welcome window is
# dragged by its title bar, six small steps, right
# three cells. After every step — the button still
# held — the bystanders' ground must hash exactly as
# before: the drag's steps never write it, at any
# instant (Stone 45: a step paints only the ground
# the window leaves and the window itself). After
# the window is set down, one region repaint over
# the drag's whole road has made the glass whole:
# the bystanders' ground still hashes as before, the
# welcome window decodes at its new place, its body
# census stands clean, and its five lines decode.
# (The bench's mouse can lose a packet under load
# and a drag fall short; the drag is retried, up to
# three takings, until the window has truly moved —
# the checks judge the road the drag travelled,
# however far the bench carried it. One hardening
# of the harness stands with the restoration, no
# check weakened: a screendump is read only after
# a breath and believed only when its measure is
# whole — the first restored runs read frames a
# step behind the glass under this bench's load,
# took a repaint still in flight for a settled
# desktop, and sent drag steps into it to be lost.)
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
    # The pixels.py discipline, and one guard more:
    # a breath after the screendump command before
    # the file is read (under load the dump can lag
    # a frame behind, or be read half-written), and
    # the picture is believed only when its measure
    # is whole — a torn read is taken again.
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
    # Waits until the desktop above the bar stands
    # still — three successive pictures of it alike,
    # the first taken only after a breath, so a
    # repaint the guest has not yet begun cannot be
    # mistaken for one already done — so the next
    # input is never sent into a guest still busy
    # repainting the last one (this bench loses mouse
    # packets under repaint load; the bar's own clock
    # is below the watched stretch and cannot keep it
    # restless). Returns the settled picture.
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
    # Presses at (x, y) and confirms the taking
    # semantically: the pressed window's title bar
    # turns the front window's blue (a pixel deep in
    # its bar, below the sheen), which only the
    # take-hold's bringing-forward paints. A press
    # the bench's mouse lost changes nothing and is
    # simply tried again by the caller.
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


def welcome_left(d):
    # The welcome window's left cell, found by its
    # title on row 5 — the title's words begin one
    # cell in from the window's left.
    for pl in range(4, 20):
        if decode(d, 5, pl + 1, "Welcome", WHITE) == "Welcome":
            return pl
    return 0


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

pl = welcome_left(dump())
expect(pl == 6, "the welcome window stands at its home place (left cell 6, top row 5)")

bystanders = None
steps_clean = True
moved_to = 0
for attempt in range(3):
    if not press_takes_hold((pl + 4) * 16, 5 * 16 + 8,
                            (pl + 3) * 16, 5 * 16 + 10):
        cmd("mouse_button 0")
        settle()
        continue
    d = settle()
    if bystanders is None:
        # The press has brought the welcome window
        # forward — a whole-desktop repaint, done and
        # settled. The bystanders' ground is hashed
        # only now, so what the hash judges is the
        # drag's own repainting. (The arrow stands at
        # the press point, above the hashed ground, in
        # this picture and in the drop's alike.)
        bystanders = rect_hash(d, 0, 312, 1024, 735)
    for i in range(6):
        cmd("mouse_move 8 0")
        PX, PY = PX + 8, PY
        dstep = settle()
        if dstep is None or rect_hash(dstep, 0, 312, 1024, 735) != bystanders:
            steps_clean = False
    cmd("mouse_button 0")
    d = settle()
    go((pl + 4) * 16, 5 * 16 + 8)
    d = settle()
    moved_to = welcome_left(d)
    if moved_to > pl:
        break
    pl = moved_to if moved_to else pl

expect(steps_clean,
       "at every step of the drag, button still held, the whole populated "
       "desktop below stands pixel for pixel untouched — no step washes or "
       "redraws a bystander (the flicker, checked at every instant)")
expect(moved_to > 6,
       f"the welcome window was truly dragged from its home place (it stands at left cell {moved_to})")
d = dump()
expect(rect_hash(d, 0, 312, 1024, 735) == bystanders,
       "after the drop the bystanders' ground still stands pixel for pixel as it was")

if moved_to:
    # The body-always-lands census (Stone 45): inside
    # the dragged window's body — below its title bar,
    # inside its frame — the frame's gray undercoat
    # may not stand anywhere; the body is its light
    # ground and its black words, whole.
    gray = 0
    for y in range((5 + 2) * 16, (5 + 13) * 16):
        for x in range((moved_to + 1) * 16, (moved_to + 50) * 16):
            if pixel(d, x, y) == FRAME:
                gray += 1
    expect(gray < 100,
           f"the dragged welcome window's body stands whole — {gray} "
           "frame-gray pixels inside it (a left-behind undercoat band "
           "stands in the tens of thousands)")
    lines = ["Welcome to Cardnull",
             "This computer is public domain:",
             "free for everyone, forever.",
             "\"Unless Yahweh builds the house,",
             "they labor in vain who build it.\" - Psalm 127:1"]
    whole = True
    for off, want in zip([2, 4, 6, 8, 10], lines):
        if decode(d, 5 + off, moved_to + 2, want, BLACK) != want:
            whole = False
    expect(whole,
           "all five of the dragged welcome window's lines decode whole at its new place")
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
held = False
for _try in range(3):
    held = press_takes_hold(400, 31 * 16 + 8, 8 * 16, 31 * 16 + 10)
    if held:
        break
    cmd("mouse_button 0")
    settle()
expect(held, "the files window's title bar takes hold for the crossing drag")
settle()
for i in range(5):
    cmd("mouse_move 16 -10")
    PX, PY = PX + 16, PY - 10
    settle()
cmd("mouse_button 0")
settle()
go(700, 400)
d = settle()
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
held = False
for _try in range(3):
    held = press_takes_hold(400, 28 * 16 + 8, 13 * 16, 28 * 16 + 10)
    if held:
        break
    cmd("mouse_button 0")
    settle()
expect(held, "the files window's title bar takes hold for the drag back home")
settle()
for i in range(5):
    cmd("mouse_move -16 10")
    PX, PY = PX - 16, PY + 10
    settle()
cmd("mouse_button 0")
settle()
go(700, 400)
d = settle()
expect(decode(d, 31, 6, "Files", WHITE) == "Files",
       "the files window decodes back at its home place")

# Tab brings the verse window forward again (it stood
# fully behind the returned files window), and it
# must decode whole — the crossings cost it nothing.
back = None
for _ in range(6):
    cmd("sendkey tab")
    d = settle()
    if d is not None and decode(d, 32, 6, "Verse", WHITE) == "Verse":
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
    d = settle()
    if d is not None and decode(d, 32, 6, "Terminal", WHITE) == "Terminal":
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
