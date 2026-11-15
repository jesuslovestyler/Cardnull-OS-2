# Stone 6 proof, boot 1: a USB keyboard stands on the bus
# (a UHCI controller carries it). The system must say at
# boot, in plain words, that a USB keyboard is ready; words
# typed while it stands there must be answered; and the
# 'usb' word must report that the USB road itself has
# brought keys — the road's own count, which only keys the
# USB road carried can raise. (The bench's keystrokes are
# offered to every keyboard the machine has; the count is
# what proves the USB road carried its share.)

import re


def region_has(rows_, text):
    return any(text in rows_[r] for r in range(13, 23))


def brought_count(rows_):
    for r in range(13, 23):
        m = re.search(r"brought (\d+) keys", rows_[r])
        if m:
            return int(m.group(1))
    return None


found = waitfor(lambda r: r[4][10:29] == "Welcome to Cardnull", 25)
expect(found is not None, "the desktop is up")

found = waitfor(lambda r: region_has(r, "A USB keyboard is ready."), 25)
expect(found is not None,
       "the system says a USB keyboard is ready")

typewrite("hello")
enter()
found = waitfor(lambda r: region_has(r, "Hello. It is good to see you."), 20)
expect(found is not None, "'hello' is answered with the keyboard plugged in")

typewrite("usb")
enter()
found = waitfor(lambda r: brought_count(r) is not None, 20)
expect(found is not None, "the 'usb' word reports the road's count")
if found:
    n = brought_count(found)
    expect(n is not None and n >= 6,
           f"the USB road itself brought the keys (count {n})")

done()
