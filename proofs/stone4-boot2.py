# Stone 4 proof, boot 2: a disc whose settings carry
# Eastern time (offset byte 59 — the settings the build
# itself lays). The clock must come up at hour 19 against a
# count near zero, and the word 'utc' must move it to 00
# for the session, saying so plainly.
import re


def hour_of(rows_):
    m = re.match(r"(\d\d):\d\d:\d\d", rows_[0][72:80])
    return m.group(1) if m else None


def region_has(rows_, needle):
    return any(needle in rows_[r] for r in range(13, 23))


found = waitfor(lambda r: hour_of(r) is not None, 25)
expect(found is not None, "the clock is on the bar")
if found:
    expect(hour_of(found) == "19",
           f"the disc's Eastern choice was read at boot (hour {hour_of(found)}, want 19)")

typewrite("utc")
enter()
found = waitfor(lambda r: region_has(r, "standard time"), 15)
expect(found is not None, "'utc' was answered in plain words")
found = waitfor(lambda r: hour_of(r) == "00", 15)
expect(found is not None, "the clock's hour moved to 00 after 'utc'")

done()
