# Stone 5 proof, boot 1: the feather as laid on the disk.
# The word 'feather' must bring the welcome feather through the
# door: its own panel, in its own color (white on green,
# 47), inside the desktop — and afterwards the system's own
# line, below the panel, saying the feather has gone home.
# One readback must show all three, in that order down the
# screen: the desktop's welcome panel (row 4), the feather's
# panel (rows 15-19), the system's continuation (row 21).


def all_three(rows_):
    return (
        rows_[4][10:29] == "Welcome to Cardnull"
        and "A feather is visiting" in rows_[16]
        and "The feather visited, and has gone home again." in rows_[21]
    )


found = waitfor(lambda r: r[4][10:29] == "Welcome to Cardnull", 25)
expect(found is not None, "the desktop is up")

# The old word is answered with the way to the new one
# (the rename of November 15, 2026), in plain words.
typewrite("guest")
enter()
found = waitfor(
    lambda r: any("Programs are called feathers here" in r[i]
                  for i in range(13, 23)), 15)
expect(found is not None,
       "the old word 'guest' is answered with the feather's name")

typewrite("feather")
enter()
found = waitfor(all_three, 20)
expect(found is not None,
       "desktop, feather panel, and the system's continuation, in order")
if found:
    expect("Hello. I am a small program, here as a feather." in found[17],
           "the feather introduced itself")
    expect("I was checked first, and I am whole." in found[18],
           "the feather said it was checked and whole")

colors = attrs()
expect(colors is not None, "the color bytes could be read")
if colors:
    expect(colors[16][16] == 47 and colors[15][14] == 47,
           "the feather's panel wears the feather's own color (47)")
    expect(colors[0][1] == 31 and colors[4][10] == 112,
           "the desktop's own colors are unharmed around the feather")

done()
