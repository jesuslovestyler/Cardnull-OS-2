# Stone 4 proof, boot 1: a fresh, blank disk.
# Nothing has ever been saved, so the bar's clock must start
# on Eastern time: the count since boot is near zero, so the
# shown hour must be 19 (midnight less five hours). Then the
# word 'utc' moves the choice to the world's standard time —
# the hour must become 00 — and the machine must say it will
# remember.
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
           f"a fresh disk starts on Eastern time (hour {hour_of(found)}, want 19)")

typewrite("utc")
enter()
found = waitfor(lambda r: region_has(r, "standard time"), 15)
expect(found is not None, "'utc' was answered in plain words")
found = waitfor(lambda r: hour_of(r) == "00", 15)
expect(found is not None, "the clock's hour moved to 00 after 'utc'")
found = waitfor(lambda r: region_has(r, "will remember it"), 15)
expect(found is not None, "the machine said it will remember the choice")

done()
