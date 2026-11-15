# Witness-disc proof, boot 1: the shipped disc itself.
# Booted from the ISO file as a CD-ROM — no -kernel, no
# other drive attached. The desktop must come up on the
# disc's carried choice (Eastern: hour 19 against a count
# near zero); the word 'guest' must bring the guest through
# the door (its panel in its color, then the system's
# continuation); and the word 'utc' must move the clock for
# the session (hour 00).
import re


def hour_of(rows_):
    m = re.match(r"(\d\d):\d\d:\d\d", rows_[0][72:80])
    return m.group(1) if m else None


def region_has(rows_, needle):
    return any(needle in rows_[r] for r in range(13, 23))


found = waitfor(lambda r: r[4][10:29] == "Welcome to Cardnull", 40)
expect(found is not None, "the desktop came up booting from the ISO itself")
if found:
    expect(hour_of(found) == "19",
           f"the disc's Eastern choice is on the clock (hour {hour_of(found)}, want 19)")

typewrite("guest")
enter()
found = waitfor(
    lambda r: "A guest is visiting" in r[16]
    and "The guest visited, and has gone home again." in r[21], 25)
expect(found is not None, "the guest visited from the disc and went home")
colors = attrs()
expect(colors is not None, "the color bytes could be read")
if colors:
    expect(colors[16][16] == 47, "the guest's panel wears its color on the disc boot")

typewrite("utc")
enter()
found = waitfor(lambda r: hour_of(r) == "00", 20)
expect(found is not None, "the word 'utc' moved the clock for the session (hour 00)")

done()
