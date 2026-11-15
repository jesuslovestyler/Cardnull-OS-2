# Stone 12 proof, boot 2: real typing on the USB road (a
# UHCI controller carries a USB keyboard). The bench's
# keystrokes are offered to every keyboard the machine
# has; as at Stone 6, the 'usb' word's own count is the
# evidence of which road carried the keys — only keys the
# USB road itself brought can raise it. A shifted word
# stands capital on the typing line, Caps Lock makes a
# whole word capital, and both are the USB road's own
# grammar: its reports' modifier byte and its Caps Lock
# usage, spoken in the shared key numbers.

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
expect(found is not None, "the system says a USB keyboard is ready")

# The shifted word, by the USB road's modifier byte.
sendkey("shift-h")
typewrite("ello")
found = waitfor(lambda r: r[24].startswith("> Hello"), 15)
expect(found is not None, "the USB road's shift makes the capital")
enter()
found = waitfor(lambda r: region_has(r, "I don't know that word yet."), 20)
expect(found is not None, "the capital word is answered as an unknown word")

# The road's own count: the sentence's letters, its Enter,
# and this word with its Enter were all the USB road's to
# bring (the shift standings are grammar, not counted).
typewrite("usb")
enter()
found = waitfor(lambda r: brought_count(r) is not None, 20)
expect(found is not None, "the 'usb' word reports the road's count")
if found:
    n = brought_count(found)
    expect(n is not None and n >= 9,
           f"the USB road itself brought the keys (count {n})")

# Caps Lock by its usage: a whole word in capitals.
sendkey("caps_lock")
typewrite("hello")
found = waitfor(lambda r: r[24].startswith("> HELLO"), 15)
expect(found is not None, "the USB road's Caps Lock makes the line capitals")
enter()
sendkey("caps_lock")

# And small letters again once it is off.
typewrite("hello")
enter()
found = waitfor(lambda r: region_has(r, "Hello. It is good to see you."), 20)
expect(found is not None, "small letters answer again once Caps Lock is off")

done()
