# Stone 8 proof, boot 4: a second blank disk, never given
# over. The offer stands; ordinary words are answered; the
# gate is asked and answered with 'no' — the disk must be
# left exactly as it was (the proof script compares the
# disk image's bytes after this boot).


def region_has(rows_, text):
    return any(text in rows_[r] for r in range(13, 23))


found = waitfor(lambda r: r[4][10:29] == "Welcome to Cardnull", 25)
expect(found is not None, "the desktop is up")
expect(region_has(found, "A hard disk is here."),
       "the disk is offered in plain words at boot")

typewrite("hello")
enter()
found = waitfor(
    lambda r: region_has(r, "Hello. It is good to see you."), 20)
expect(found is not None, "ordinary words are answered as always")

typewrite("setup")
enter()
found = waitfor(
    lambda r: region_has(r, "This will clear everything on the disk."), 20)
expect(found is not None, "'setup' asks behind the gate")

typewrite("no")
enter()
found = waitfor(
    lambda r: region_has(r, "The disk was left as it was."), 20)
expect(found is not None, "a 'no' at the gate leaves the disk as it was")

done()
