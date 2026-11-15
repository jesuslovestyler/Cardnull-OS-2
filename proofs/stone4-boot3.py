# Stone 4 proof, boot 3: no modules at all — a bare system,
# as Stones 1-3 booted. The clock must start on the honest
# default, Eastern time (hour 19 against a count near
# zero), and the word 'feather' must be answered plainly:
# this disc holds no feather.
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
           f"with no settings carried, the clock starts on Eastern (hour {hour_of(found)}, want 19)")

typewrite("feather")
enter()
found = waitfor(lambda r: region_has(r, "no feather on this disc"), 15)
expect(found is not None, "'feather' with no modules is answered plainly")

done()
