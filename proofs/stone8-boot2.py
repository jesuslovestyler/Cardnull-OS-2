# Stone 8 proof, boot 2: the SAME disk as boot 1, booted
# again, the disc still carrying Eastern. The disk's kept
# choice (the world's time) must overrule the disc: the
# clock comes up at hour 00 with no offer on the desktop.
# Then 'eastern' is chosen and kept in turn — the clock
# moves to 19 and the answer names the disk as its keeper.


def hour_of(rows_):
    return rows_[0][72:74]


def region_has(rows_, text):
    return any(text in rows_[r] for r in range(13, 23))


found = waitfor(lambda r: hour_of(r) == "00", 25)
expect(found is not None,
       "the disk's kept choice overrules the disc at boot (hour 00)")

waitfor(lambda r: False, 3)
rows_now = waitfor(lambda r: r, 5)
expect(rows_now is not None
       and not region_has(rows_now, "A hard disk is here."),
       "no offer: the disk is already the system's")

typewrite("eastern")
enter()
found = waitfor(
    lambda r: region_has(r, "The disk will remember it."), 20)
expect(found is not None, "'eastern' is answered as a choice the disk keeps")
found = waitfor(lambda r: hour_of(r) == "19", 15)
expect(found is not None, "the clock moved to Eastern (hour 19)")

done()
