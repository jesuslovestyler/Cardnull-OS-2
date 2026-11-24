# Stone 43 proof, boot 4: a blank stick AND a blank
# hard disk in the machine together. The hard disk
# keeps its place, as it always has: it is the disk
# offered at the rising, and the gate's yes cards it —
# the stick is not offered, and (the shell's own check
# after this boot) its bytes stand untouched.


def region_has(rows_, text):
    return any(text in rows_[r] for r in range(13, 23))


found = waitfor(lambda r: r[4][10:29] == "Welcome to Cardnull", 25)
expect(found is not None, "the desktop is up")
found = waitfor(
    lambda r: region_has(r, "A hard disk is here."), 25)
expect(found is not None,
       "the hard disk is offered, as it always has been")
if found:
    expect(not region_has(found, "A USB stick is here. Type setup"),
           "the stick is not offered while a hard disk stands fitted")

typewrite("setup")
enter()
found = waitfor(
    lambda r: region_has(r, "This will clear everything on the disk."), 20)
expect(found is not None, "'setup' asks behind the gate, in plain words")

typewrite("yes")
enter()
found = waitfor(
    lambda r: region_has(r, "The disk will remember your choices now."), 20)
expect(found is not None, "'yes' gives the hard disk its keeping")

done()
