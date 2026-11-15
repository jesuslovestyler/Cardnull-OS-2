# Stone 8 proof, boot 1: a blank hard disk is attached and
# the disc carries Eastern. The desktop must offer the
# disk plainly; the clock starts on the disc's choice
# (hour 19 against the pinned bench clock); 'setup' must
# ask behind the gate; 'yes' must give the disk its
# keeping; and 'utc' must then be answered as a choice the
# disk will remember, with the clock moving to hour 00.


def hour_of(rows_):
    return rows_[0][72:74]


def region_has(rows_, text):
    return any(text in rows_[r] for r in range(13, 23))


found = waitfor(lambda r: r[4][10:29] == "Welcome to Cardnull", 25)
expect(found is not None, "the desktop is up")
expect(region_has(found, "A hard disk is here."),
       "the disk is offered in plain words at boot")
expect(hour_of(found) == "19",
       f"the disc's Eastern choice rules before setup (hour {hour_of(found)})")

typewrite("setup")
enter()
found = waitfor(
    lambda r: region_has(r, "This will clear everything on the disk."), 20)
expect(found is not None, "'setup' asks behind the gate, in plain words")

typewrite("yes")
enter()
found = waitfor(
    lambda r: region_has(r, "The disk will remember your choices now."), 20)
expect(found is not None, "'yes' gives the disk its keeping")

typewrite("utc")
enter()
found = waitfor(
    lambda r: region_has(r, "The disk will remember it."), 20)
expect(found is not None, "'utc' is answered as a choice the disk keeps")
found = waitfor(lambda r: hour_of(r) == "00", 15)
expect(found is not None, "the clock moved to the world's time (hour 00)")

done()
