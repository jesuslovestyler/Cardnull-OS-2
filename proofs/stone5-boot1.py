# Stone 5 proof, boot 1: the guest as laid on the disk.
# The word 'guest' must bring the welcome guest through the
# door: its own panel, in its own color (white on green,
# 47), inside the desktop — and afterwards the system's own
# line, below the panel, saying the guest has gone home.
# One readback must show all three, in that order down the
# screen: the desktop's welcome panel (row 4), the guest's
# panel (rows 15-19), the system's continuation (row 21).


def all_three(rows_):
    return (
        rows_[4][10:29] == "Welcome to Cardnull"
        and "A guest is visiting" in rows_[16]
        and "The guest visited, and has gone home again." in rows_[21]
    )


found = waitfor(lambda r: r[4][10:29] == "Welcome to Cardnull", 25)
expect(found is not None, "the desktop is up")

typewrite("guest")
enter()
found = waitfor(all_three, 20)
expect(found is not None,
       "desktop, guest panel, and the system's continuation, in order")
if found:
    expect("Hello. I am a small program, here as a guest." in found[17],
           "the guest introduced itself")
    expect("I was checked first, and I am whole." in found[18],
           "the guest said it was checked and whole")

colors = attrs()
expect(colors is not None, "the color bytes could be read")
if colors:
    expect(colors[16][16] == 47 and colors[15][14] == 47,
           "the guest's panel wears the guest's own color (47)")
    expect(colors[0][1] == 31 and colors[4][10] == 112,
           "the desktop's own colors are unharmed around the guest")

done()
