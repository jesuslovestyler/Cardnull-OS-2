# Stone 18 proof, boot 1: the voice, heard in windows.
#
# The bench's speaker capture (the QEMU monitor's
# wavcapture, driven here through a second monitor
# socket named by the SNDSOCK environment variable)
# delivers the speaker's active samples; the proof
# therefore opens a capture window around each event
# and lays the files in SNDWORK for the shell's
# analysis:
#
#   boot.wav    from the scenario's start until two
#               seconds after the drawn desktop first
#               stands — the welcome chime sounds as
#               the desktop rises, inside this window.
#   refuse.wav  opened just before an unknown word is
#               answered — the refusal's low note.
#   idle.wav    four seconds of nothing at all — the
#               silence discipline: no stray noise.
#   chime.wav   opened just before the word 'chime' is
#               typed — the welcome sounded again.
#
# The desktop itself is asserted as Stone 9 asserts it.

import os
import socket
import time as _time

_cap = {"sock": None}


def _hmp(command):
    if _cap["sock"] is None:
        _cap["sock"] = socket.socket(socket.AF_UNIX)
        _cap["sock"].connect(os.environ["SNDSOCK"])
        _cap["sock"].settimeout(3)
    _cap["sock"].sendall((command + "\n").encode())
    _time.sleep(0.3)
    try:
        while True:
            data = _cap["sock"].recv(65536)
            if not data or data.rstrip().endswith(b"(qemu)"):
                break
    except socket.timeout:
        pass


def cap_start(name):
    _hmp("wavcapture %s/%s snd 44100 16 1"
         % (os.environ["SNDWORK"], name))


def cap_stop():
    # The monitor names captures by their place among
    # the captures still open, and this proof never
    # holds more than one open: the open one is 0.
    _hmp("stopcapture 0")


cap_start("boot.wav")
found = waitdump(lambda d: count(d, (0, 0, 170)) > 4000, 30)
expect(found is not None, "the desktop is drawn")
_time.sleep(2)
cap_stop()

cap_start("refuse.wav")
typewrite("zzzz")
enter()
_time.sleep(1.2)
cap_stop()

cap_start("idle.wav")
_time.sleep(4)
cap_stop()

cap_start("chime.wav")
typewrite("chime")
enter()
_time.sleep(1.5)
cap_stop()

done()
