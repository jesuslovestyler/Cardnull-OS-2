# Stone 43 proof, boot 2: the same stick, booted again.
# The card stood on it, so no offer is made; the notes
# were read back from the stick at the rising — 'notes'
# shows both without any keeping being done again —
# and a third note joins them on the stick.


def region_has(rows_, text):
    return any(text in rows_[r] for r in range(13, 23))


found = waitfor(lambda r: r[4][10:29] == "Welcome to Cardnull", 25)
expect(found is not None, "the desktop is up")
expect(not region_has(found, "Type setup to let it remember"),
       "no offer is made: the stick already keeps")

typewrite("notes")
enter()
found = waitfor(
    lambda r: region_has(r, "Your notes, kept on the disk:"), 20)
expect(found is not None, "the page is there after the reboot")
if found:
    expect(region_has(found, "remember the garden"),
           "the first note stayed through the reboot")
    expect(region_has(found, "call billy about the roof"),
           "the second note stayed through the reboot")

typewrite("note pray for quinton")
enter()
found = waitfor(
    lambda r: region_has(r, "Your note is kept on the disk."), 20)
expect(found is not None, "a third note is kept on the stick")

done()
