# Stone 15 proof, boot 4: no disk, a fresh boot. The
# session note of the boot before is gone — the page is
# empty again, which is what session-only keeping means.


def region_has(rows_, text):
    return any(text in rows_[r] for r in range(13, 23))


found = waitfor(lambda r: r[4][10:29] == "Welcome to Cardnull", 25)
expect(found is not None, "the desktop is up")

typewrite("notes")
enter()
found = waitfor(
    lambda r: region_has(r, "No notes are kept yet."), 20)
expect(found is not None, "nothing stayed: the page is empty on a fresh boot")

done()
