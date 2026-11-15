#!/usr/bin/env python3
# The proof bench's hands: drives one running QEMU through its
# monitor socket — reads the emulated screen (the VGA text
# buffer at 0xB8000) and types on the emulated keyboard with
# `sendkey`. This is the same readback pattern the Nifla
# language's bare-metal proofs use, factored into one place so
# each stone's proof says only what it checks.
#
# Usage: python3 tools/screen.py <scenario.py> <monitor.sock>
#
# The scenario file runs with these helpers in scope:
#   rows()            the screen's 25 rows, as text
#   attrs()           the screen's 2000 color bytes, row by row
#   sendkey(name)     one key by its QEMU name ("a", "ret", ...)
#   typewrite(text)   types letters and spaces, slowly
#   enter()           the Enter key
#   backspace()       the Backspace key
#   waitfor(fn, secs) polls rows() until fn(rows) holds; the
#                     rows it held for, or None on timeout
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

# Connect to the monitor (QEMU may take a moment to open it).
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


def _screen_bytes():
    out = _command("xp /4000bx 0xb8000")
    data = []
    for line in out.splitlines():
        match = re.match(r"^[0-9a-f]+: ((?:0x[0-9a-f]{2} ?)+)$", line.strip())
        if match:
            data += [int(part, 16) for part in match.group(1).split()]
    if len(data) < 4000:
        return None
    return data


def rows():
    """The screen's 25 rows, as text (unprintable bytes as spaces)."""
    data = _screen_bytes()
    if data is None:
        return None
    return [
        "".join(
            chr(data[(r * 80 + c) * 2]) if 32 <= data[(r * 80 + c) * 2] < 127 else " "
            for c in range(80)
        )
        for r in range(25)
    ]


def attrs():
    """The screen's color bytes: 25 rows of 80 attribute bytes."""
    data = _screen_bytes()
    if data is None:
        return None
    return [[data[(r * 80 + c) * 2 + 1] for c in range(80)] for r in range(25)]


def sendkey(name):
    _command(f"sendkey {name}")
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


def backspace():
    sendkey("backspace")


def waitfor(fn, secs=25):
    """Poll the screen until fn(rows) holds; return those rows."""
    end = time.time() + secs
    last = None
    while time.time() < end:
        try:
            last = rows()
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
    "rows": rows,
    "attrs": attrs,
    "sendkey": sendkey,
    "typewrite": typewrite,
    "enter": enter,
    "backspace": backspace,
    "waitfor": waitfor,
    "expect": expect,
    "done": done,
    "time": time,
})
# A scenario that falls off the end without done() has failed
# to finish its checks.
print("FAIL: the scenario ended without a verdict")
sys.exit(1)
