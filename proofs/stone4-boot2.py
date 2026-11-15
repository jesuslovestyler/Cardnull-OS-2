# Stone 4 proof, boot 2: the same disk, a fresh machine.
# Nobody tells this boot anything: the clock must come up on
# the world's standard time (hour 00), because boot 1's
# choice was kept on the disk. Then 'eastern' must move it
# back to 19, proving the word works both ways.
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
           f"the remembered choice came back on its own (hour {hour_of(found)}, want 00)")

typewrite("eastern")
enter()
found = waitfor(lambda r: region_has(r, "Eastern time"), 15)
expect(found is not None, "'eastern' was answered in plain words")
found = waitfor(lambda r: hour_of(r) == "19", 15)
expect(found is not None, "the clock's hour moved back to 19 after 'eastern'")

done()
