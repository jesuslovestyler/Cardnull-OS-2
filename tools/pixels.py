#!/usr/bin/env python3
# The proof bench's eyes for the face of light (Stone 9):
# drives one running QEMU through its monitor socket and
# reads the emulated screen as PICTURES — the monitor's
# `screendump` writes a PPM of the granted framebuffer, and
# this harness parses it and answers in pixels. Typing is
# the same `sendkey` road tools/screen.py uses.
#
# Usage: python3 tools/pixels.py <scenario.py> <monitor.sock> <dump.ppm>
#
# The scenario file runs with these helpers in scope:
#   dump()            (width, height, bytes) of the screen now
#   pixel(d, x, y)    the (red, green, blue) at one point
#   count(d, rgb)     how many pixels are exactly that color
#   region(d, x0, y0, x1, y1)  how many distinct colors a
#                     rectangle holds (text shows as many)
#   sendkey(name)     one key by its QEMU name
#   typewrite(text)   types letters and spaces, slowly
#   enter()           the Enter key
#   mousemove(dx, dy) moves the emulated mouse, relatively
#   mousebutton(n)    sets its buttons (1 = first down)
#   waitdump(fn, secs) polls dump() until fn(dump) holds
#   expect(cond, why) records one check, prints ok / NOT OK
#   done()            quits QEMU, prints PASS or FAIL, exits
#
# Exit status is the scenario's verdict: 0 pass, 1 fail.

import re
import socket
import sys
import time

sock_path = sys.argv[2]
scenario_path = sys.argv[1]
dump_path = sys.argv[3]

deadline = time.time() + 15
sock = None
while time.time() < deadline:
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(sock_path)
        break
    except OSError:
        if sock is not None:
            sock.close()
        sock = None
        time.sleep(0.2)
if sock is None:
    print("FAIL: the QEMU monitor never opened")
    sys.exit(1)
sock.settimeout(5)

_buf = b""


def _until_prompt():
    global _buf
    while b"(qemu)" not in _buf:
        chunk = sock.recv(4096)
        if not chunk:
            raise IOError("the monitor closed")
        _buf += chunk
    out, _buf = _buf.decode(errors="replace"), b""
    return out


_until_prompt()  # the greeting


def _command(text):
    sock.sendall(text.encode() + b"\n")
    return _until_prompt()


def _read_ppm(path):
    with open(path, "rb") as f:
        data = f.read()
    # Header: P6, whitespace-separated width, height, maxval,
    # then one whitespace byte, then the pixels.
    parts = []
    i = 0
    while len(parts) < 4:
        while i < len(data) and data[i:i + 1].isspace():
            i += 1
        if data[i:i + 1] == b"#":
            while data[i:i + 1] != b"\n":
                i += 1
            continue
        j = i
        while j < len(data) and not data[j:j + 1].isspace():
            j += 1
        parts.append(data[i:j])
        i = j
    i += 1  # the single whitespace after the max value
    if parts[0] != b"P6":
        return None
    return (int(parts[1]), int(parts[2]), data[i:])


def dump():
    """The screen now: (width, height, pixel bytes), or None."""
    _command(f"screendump {dump_path}")
    time.sleep(0.15)
    try:
        return _read_ppm(dump_path)
    except OSError:
        return None


def pixel(d, x, y):
    w, h, px = d
    o = (y * w + x) * 3
    return (px[o], px[o + 1], px[o + 2])


def count(d, rgb):
    w, h, px = d
    n = 0
    for o in range(0, len(px) - 2, 3):
        if px[o] == rgb[0] and px[o + 1] == rgb[1] and px[o + 2] == rgb[2]:
            n += 1
    return n


def region_colors(d, x0, y0, x1, y1):
    w, h, px = d
    seen = set()
    for y in range(y0, min(y1, h)):
        for x in range(x0, min(x1, w)):
            o = (y * w + x) * 3
            seen.add((px[o], px[o + 1], px[o + 2]))
    return seen


def sendkey(name):
    _command(f"sendkey {name}")
    time.sleep(0.25)


def mousemove(dx, dy):
    """Moves the emulated mouse by (dx, dy), as the
    monitor's own mouse_move speaks it."""
    _command(f"mouse_move {dx} {dy}")
    time.sleep(0.25)


def mousebutton(state):
    """Sets the emulated mouse's buttons: 1 is the first
    button down, 0 is all buttons up."""
    _command(f"mouse_button {state}")
    time.sleep(0.25)


def typewrite(text):
    for ch in text:
        if "a" <= ch <= "z":
            sendkey(ch)
        elif ch == " ":
            sendkey("spc")
        elif "0" <= ch <= "9":
            sendkey(ch)
        else:
            raise ValueError(f"typewrite cannot type {ch!r}")


def enter():
    sendkey("ret")


def waitdump(fn, secs=25):
    """Poll the screen until fn(dump) holds; return that dump."""
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


_failures = []


def expect(cond, why):
    if cond:
        print(f"ok: {why}")
    else:
        print(f"NOT OK: {why}")
        _failures.append(why)
    return cond


def done():
    try:
        _command("quit")
        sock.close()
    except Exception:
        pass
    if _failures:
        print(f"FAIL ({len(_failures)} check(s) failed)")
        sys.exit(1)
    print("PASS")
    sys.exit(0)


scenario = open(scenario_path).read()
exec(compile(scenario, scenario_path, "exec"), {
    "dump": dump,
    "pixel": pixel,
    "count": count,
    "region_colors": region_colors,
    "sendkey": sendkey,
    "typewrite": typewrite,
    "enter": enter,
    "mousemove": mousemove,
    "mousebutton": mousebutton,
    "waitdump": waitdump,
    "expect": expect,
    "done": done,
    "time": time,
})
print("FAIL: the scenario ended without a verdict")
sys.exit(1)
