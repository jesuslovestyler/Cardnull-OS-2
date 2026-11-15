# Stone 15 proof, boot 3: no disk at all. A note is kept
# for the session, and the answers say so in plain words
# — kept until the machine is turned off.


def region_has(rows_, text):
    return any(text in rows_[r] for r in range(13, 23))


found = waitfor(lambda r: r[4][10:29] == "Welcome to Cardnull", 25)
expect(found is not None, "the desktop is up")

typewrite("notes")
enter()
found = waitfor(
    lambda r: region_has(r, "No notes are kept yet."), 20)
expect(found is not None, "the empty page says so plainly")

typewrite("note a passing thought")
enter()
found = waitfor(
    lambda r: region_has(r, "Your note is kept until the machine is turned off."), 20)
expect(found is not None, "the session-only keeping is said in plain words")

typewrite("notes")
enter()
found = waitfor(
    lambda r: region_has(r, "Your notes, kept until the machine is turned off:"), 20)
expect(found is not None, "the page's heading says the notes live only for now")
if found:
    expect(region_has(found, "a passing thought"),
           "the session's note stands on the page")

done()
