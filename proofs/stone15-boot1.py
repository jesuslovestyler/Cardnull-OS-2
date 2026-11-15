# Stone 15 proof, boot 1: a blank hard disk is attached.
# Behind the setup gate's yes, two notes are kept — each
# answered as kept on the disk — and 'notes' shows the
# page: the heading that says where they live, and both
# lines.


def region_has(rows_, text):
    return any(text in rows_[r] for r in range(13, 23))


found = waitfor(lambda r: r[4][10:29] == "Welcome to Cardnull", 25)
expect(found is not None, "the desktop is up")
expect(region_has(found, "A hard disk is here."),
       "the disk is offered in plain words at boot")

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

typewrite("note remember the garden")
enter()
found = waitfor(
    lambda r: region_has(r, "Your note is kept on the disk."), 20)
expect(found is not None, "the first note is answered as kept on the disk")

typewrite("note call billy about the roof")
enter()
found = waitfor(
    lambda r: region_has(r, "Your note is kept on the disk."), 20)
expect(found is not None, "the second note is answered as kept on the disk")

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
