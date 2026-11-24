# Stone 43 proof, boot 1: a blank USB stick on the xHCI
# bus, and no hard disk in the machine. The stick is
# offered in plain words at the rising; the 'usb' word
# reports it with its measure, and the keyboard on the
# same bus still stands ready; behind the setup gate's
# yes the stick takes the keeping, and two notes are
# kept on it.


def region_has(rows_, text):
    return any(text in rows_[r] for r in range(13, 23))


found = waitfor(lambda r: r[4][10:29] == "Welcome to Cardnull", 25)
expect(found is not None, "the desktop is up")
found = waitfor(
    lambda r: region_has(r, "A USB stick is here."), 25)
expect(found is not None,
       "the stick is offered in plain words at boot")

typewrite("usb")
enter()
found = waitfor(
    lambda r: region_has(r, "A USB stick is here. It holds 16384 sectors."), 20)
expect(found is not None, "'usb' reports the stick with its sector count")
if found:
    expect(region_has(found, "A USB keyboard is ready on the modern USB road."),
           "the keyboard on the same bus still stands ready")

typewrite("setup")
enter()
found = waitfor(
    lambda r: region_has(r, "This will clear everything on the disk."), 20)
expect(found is not None, "'setup' asks behind the gate, in plain words")

typewrite("yes")
enter()
found = waitfor(
    lambda r: region_has(r, "The disk will remember your choices now."), 20)
expect(found is not None, "'yes' gives the stick its keeping")

typewrite("note remember the garden")
enter()
found = waitfor(
    lambda r: region_has(r, "Your note is kept on the disk."), 20)
expect(found is not None, "the first note is answered as kept")

typewrite("note call billy about the roof")
enter()
found = waitfor(
    lambda r: region_has(r, "Your note is kept on the disk."), 20)
expect(found is not None, "the second note is answered as kept")

typewrite("notes")
enter()
found = waitfor(
    lambda r: region_has(r, "Your notes, kept on the disk:"), 20)
expect(found is not None, "the page's heading says the notes live on the disk")
if found:
    expect(region_has(found, "remember the garden"),
           "the first note stands on the page")
    expect(region_has(found, "call billy about the roof"),
           "the second note stands on the page")

done()
