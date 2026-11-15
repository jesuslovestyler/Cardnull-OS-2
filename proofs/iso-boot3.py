# Witness-disc proof, boot 3: a variant disc carrying a
# tampered guest (one byte flipped; the card still
# describes the true guest). Booted from that ISO, the word
# 'guest' must be refused in plain words, the guest must
# never appear, and the desktop must stand unharmed.


def region_has(rows_, needle):
    return any(needle in rows_[r] for r in range(13, 23))


found = waitfor(lambda r: r[4][10:29] == "Welcome to Cardnull", 40)
expect(found is not None, "the desktop came up booting from the tampered ISO")

typewrite("guest")
enter()
found = waitfor(
    lambda r: region_has(r, "not whole, so it was not let in"), 25)
expect(found is not None, "the tampered guest was refused in plain words")

after = rows()
expect(after is not None and "A guest is visiting" not in "".join(after),
       "the refused guest never appeared")
colors = attrs()
expect(colors is not None, "the color bytes could be read")
if colors:
    expect(all(c != 47 for row_ in colors for c in row_),
           "none of the guest's color (47) is anywhere on the screen")
    expect(colors[0][1] == 31 and after[4][10:29] == "Welcome to Cardnull",
           "the desktop stands unharmed after the refusal")

done()
