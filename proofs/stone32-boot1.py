# Stone 32 proof, boot 1: a USB keyboard stands on the
# modern road (an xHCI controller carries it). The system
# must say at boot, in plain words, that a USB keyboard
# is ready on the modern USB road; words typed while it
# stands there must be answered; and the 'usb' word must
# report that the modern road itself has brought keys —
# the road's own count, which only keys the modern road
# carried can raise. (The bench's keystrokes are offered
# to every keyboard the machine has; the count is what
# proves the modern road carried its share.) Shifted
# letters and Caps Lock are checked on this road too, as
# Stone 12 requires of any road.

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

found = waitfor(lambda r: region_has(r, "A USB keyboard is ready on the modern USB road."), 25)
expect(found is not None,
       "the system says a USB keyboard is ready on the modern USB road")

# The shifted word, by the modern road's modifier byte.
sendkey("shift-h")
typewrite("ello")
found = waitfor(lambda r: r[24].startswith("> Hello"), 15)
expect(found is not None, "the modern road's shift makes the capital")
enter()
found = waitfor(lambda r: region_has(r, "I don't know that word yet."), 20)
expect(found is not None, "the capital word is answered as an unknown word")

# The road's own count: the sentence's letters, its
# Enter, and this word with its Enter were all the
# modern road's to bring (the shift standings are
# grammar, not counted).
typewrite("usb")
enter()
found = waitfor(lambda r: brought_count(r) is not None, 20)
expect(found is not None, "the 'usb' word reports the road's count")
if found:
    n = brought_count(found)
    expect(n is not None and n >= 9,
           f"the modern road itself brought the keys (count {n})")

# Caps Lock by its usage: a whole word in capitals.
sendkey("caps_lock")
typewrite("hello")
found = waitfor(lambda r: r[24].startswith("> HELLO"), 15)
expect(found is not None, "the modern road's Caps Lock makes the line capitals")
enter()
sendkey("caps_lock")

# And small letters again once it is off.
typewrite("hello")
enter()
found = waitfor(lambda r: region_has(r, "Hello. It is good to see you."), 20)
expect(found is not None, "small letters answer again once Caps Lock is off")

done()
