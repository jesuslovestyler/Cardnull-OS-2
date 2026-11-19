# Stone 14 proof, boot 1: the two windows on the face of
# light. The welcome window stands forward at the rising
# (its title bar blue, the feather's quiet gray, the feather's
# body saying no feather has visited yet); Tab brings each
# window forward in turn; a press on the feather's panel
# receives the feather and brings its window forward;
# Escape closes the forward window back to the desktop;
# the word 'feather' opens it again; a press on the welcome
# window's close mark closes it; the word 'welcome' opens
# it again, forward; and the typing line works throughout.
# (Stone 38: the terminal window stands open from the
# rising too, so Tab's turn has three windows in it; and
# the feather's panel lives in its window, so the press
# that receives the feather goes by the start menu's
# Feather choice, as in Stone 13's proof.)

BLUE = (0, 0, 170)
GREEN = (0, 170, 0)
GRAY = (170, 170, 170)
DARK = (85, 85, 85)
BLACK = (0, 0, 0)


def band_count(d, rgb, x0, y0, x1, y1):
    if d is None:
        return 0
    n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pixel(d, x, y) == rgb:
                n += 1
    return n


# The desktop rises: the welcome forward, the feather behind.
d = waitdump(lambda d: d is not None and d[0] == 1024 and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")
if d:
    expect(pixel(d, 400, 90) == BLUE,
           "the welcome window stands forward: its title bar is blue")
    expect(pixel(d, 400, 426) == DARK,
           "the feather window stands behind: its title bar is quiet gray")
    expect(count(d, GREEN) == 0, "no feather panel stands before any visit")
    expect(band_count(d, GRAY, 208, 448, 608, 464) > 20,
           "the feather window's body says no feather has visited yet")

# Tab brings the feather forward; Tab again, the
# terminal (Stone 38: it stands open from the rising,
# third in the turn); Tab a third time, the welcome.
sendkey("tab")
d = waitdump(lambda d: d is not None and pixel(d, 400, 426) == BLUE
             and pixel(d, 400, 90) == DARK, 15)
expect(d is not None, "Tab brought the feather window forward")
sendkey("tab")
# The terminal's title bar is glassy at its left; its
# forward mark is the blue at (600, 520).
d = waitdump(lambda d: d is not None and pixel(d, 600, 520) == BLUE
             and pixel(d, 400, 426) == DARK
             and pixel(d, 400, 90) == DARK, 15)
expect(d is not None, "Tab again brought the terminal window forward")
sendkey("tab")
d = waitdump(lambda d: d is not None and pixel(d, 400, 90) == BLUE
             and pixel(d, 400, 426) == DARK, 15)
expect(d is not None, "Tab a third time brought the welcome window forward")

# A press receiving the feather: the start button,
# then the risen menu's Feather choice — the visit,
# and its window forward. The arrow's square stands
# at (504, 376); a move of (-490, +374) lays its point
# on the button's center (16, 752); a further (+24,
# -136) lays it on the Feather choice at (40, 616).
mousemove(-490, 374)
mousebutton(1)
mousebutton(0)
mousemove(24, -136)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None and count(d, GREEN) > 10000, 25)
expect(d is not None, "the press brought the feather: its green panel stands")
if d:
    expect(pixel(d, 400, 426) == BLUE,
           "the visit brought the feather window forward")

# Escape closes the forward window — the feather's — back
# to the desktop; the welcome stands forward in its place.
sendkey("esc")
# Stone 38: where the feather window's title stood
# (400, 426) is plain desktop ground again — the
# terminal's title bar stands at (600, 520) now, in
# its behind gray, not the old ground's black.
d = waitdump(lambda d: d is not None and count(d, GREEN) == 0
             and pixel(d, 400, 426) == BLACK, 15)
expect(d is not None, "Escape closed the feather window back to the desktop")
if d:
    expect(pixel(d, 400, 90) == BLUE,
           "the welcome window stands forward in its place")

# The word 'feather' opens the window again, and visits.
typewrite("feather")
enter()
d = waitdump(lambda d: d is not None and count(d, GREEN) > 10000, 25)
expect(d is not None, "the word 'feather' opened its window and visited again")

# A press on the welcome window's close mark closes it:
# the mark stands at the title bar's right end, the cell
# at x 880..896, y 80..96; from the arrow's point at
# (40, 616) two moves of (+424, -264) lay its point there.
mousemove(424, -264)
mousemove(424, -264)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None and pixel(d, 200, 120) == BLACK
             and pixel(d, 400, 90) == BLACK, 15)
expect(d is not None, "the close mark closed the welcome window")
if d:
    expect(count(d, GREEN) > 10000,
           "the feather window stands whole while the welcome is closed")

# The word 'welcome' opens it again, forward.
typewrite("welcome")
enter()
d = waitdump(lambda d: d is not None and pixel(d, 200, 120) == GRAY
             and pixel(d, 400, 90) == BLUE, 15)
expect(d is not None, "the word 'welcome' opened its window again, forward")

# The typing line still works, with the windows about.
# The feather window stands over the terminal's first
# answer rows, so a press on the terminal's typing row
# (from the arrow's point at (888, 88): two moves of
# (-244, +312)) raises the terminal first; the answer
# then stands in the clear at its first answer row
# (row 33, y 528..543).
mousemove(-244, 312)
mousemove(-244, 312)
mousebutton(1)
mousebutton(0)
typewrite("hello")
enter()
d = waitdump(lambda d: d is not None and band_count(d, GRAY, 0, 528, 1024, 544) > 50, 20)
expect(d is not None, "'hello' is answered in light, the windows about")

done()
