# Stone 4 proof, boot 1: a disc whose settings carry the
# world's standard time (offset byte 64, laid by the proof).
# The bar's clock must come up on that choice without being
# told — the count since boot is near zero, so the shown
# hour must be 00. Then the word 'eastern' changes the
# choice for the session: the hour must become 19, and the
# answer must say plainly that it lasts until the machine
# is turned off (a read-only disc remembers nothing more).
import re


def hour_of(rows_):
    m = re.match(r"(\d\d):\d\d:\d\d", rows_[0][72:80])
    return m.group(1) if m else None


def region_has(rows_, needle):
    return any(needle in rows_[r] for r in range(13, 23))


found = waitfor(lambda r: hour_of(r) is not None, 25)
expect(found is not None, "the clock is on the bar")
if found:
    expect(hour_of(found) == "00",
           f"the disc's carried choice was read at boot (hour {hour_of(found)}, want 00)")

typewrite("eastern")
enter()
found = waitfor(lambda r: region_has(r, "Eastern time"), 15)
expect(found is not None, "'eastern' was answered in plain words")
found = waitfor(lambda r: region_has(r, "until the machine is turned off"), 15)
expect(found is not None, "the answer says honestly how long the choice lasts")
found = waitfor(lambda r: hour_of(r) == "19", 15)
expect(found is not None, "the clock's hour moved to 19 after 'eastern'")

done()
