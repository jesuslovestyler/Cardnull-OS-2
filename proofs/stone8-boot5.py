# Stone 8 proof, boot 5: no disk at all. The disc's
# Eastern choice rules (hour 19), no offer stands on the
# desktop, and 'setup' is answered plainly: there is no
# hard disk here to set up.


def hour_of(rows_):
    return rows_[0][72:74]


def region_has(rows_, text):
    return any(text in rows_[r] for r in range(13, 23))


found = waitfor(lambda r: hour_of(r) == "19", 25)
expect(found is not None, "the disc's choice rules with no disk (hour 19)")

waitfor(lambda r: False, 3)
rows_now = waitfor(lambda r: r, 5)
expect(rows_now is not None
       and not region_has(rows_now, "A hard disk is here."),
       "no offer when there is no disk")

typewrite("setup")
enter()
found = waitfor(
    lambda r: region_has(r, "There is no hard disk here to set up."), 20)
expect(found is not None, "'setup' answers plainly with no disk")

done()
