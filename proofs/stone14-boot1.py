# Stone 14 proof, boot 1: the two windows on the face of
# light. The welcome window stands forward at the rising
# (its title bar blue, the guest's quiet gray, the guest's
# body saying no guest has visited yet); Tab brings each
# window forward in turn; a press on the guest's panel
# receives the guest and brings its window forward;
# Escape closes the forward window back to the desktop;
# the word 'guest' opens it again; a press on the welcome
# window's close mark closes it; the word 'welcome' opens
# it again, forward; and the typing line works throughout.

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


# The desktop rises: the welcome forward, the guest behind.
d = waitdump(lambda d: d is not None and d[0] == 1024 and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")
if d:
    expect(pixel(d, 400, 90) == BLUE,
           "the welcome window stands forward: its title bar is blue")
    expect(pixel(d, 400, 426) == DARK,
           "the guest window stands behind: its title bar is quiet gray")
    expect(count(d, GREEN) == 0, "no guest panel stands before any visit")
    expect(band_count(d, GRAY, 208, 448, 608, 464) > 20,
           "the guest window's body says no guest has visited yet")

# Tab brings the guest forward; Tab again, the welcome.
sendkey("tab")
d = waitdump(lambda d: d is not None and pixel(d, 400, 426) == BLUE
             and pixel(d, 400, 90) == DARK, 15)
expect(d is not None, "Tab brought the guest window forward")
sendkey("tab")
d = waitdump(lambda d: d is not None and pixel(d, 400, 90) == BLUE
             and pixel(d, 400, 426) == DARK, 15)
expect(d is not None, "Tab again brought the welcome window forward")

# A press on the guest's panel: the visit, and its window
# forward. The arrow's square stands at (504, 376); a move
# of (-106, +142) lays its point at (400, 520), well
# inside the panel.
mousemove(-106, 142)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None and count(d, GREEN) > 10000, 25)
expect(d is not None, "the press brought the guest: its green panel stands")
if d:
    expect(pixel(d, 400, 426) == BLUE,
           "the visit brought the guest window forward")

# Escape closes the forward window — the guest's — back
# to the desktop; the welcome stands forward in its place.
sendkey("esc")
d = waitdump(lambda d: d is not None and count(d, GREEN) == 0
             and pixel(d, 600, 520) == BLACK, 15)
expect(d is not None, "Escape closed the guest window back to the desktop")
if d:
    expect(pixel(d, 400, 90) == BLUE,
           "the welcome window stands forward in its place")

# The word 'guest' opens the window again, and visits.
typewrite("guest")
enter()
d = waitdump(lambda d: d is not None and count(d, GREEN) > 10000, 25)
expect(d is not None, "the word 'guest' opened its window and visited again")

# A press on the welcome window's close mark closes it:
# the mark stands at the title bar's right end, the cell
# at x 880..896, y 80..96; from the arrow's square at
# (398, 518) a move of (+488, -432) lays its point there.
mousemove(488, -432)
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None and pixel(d, 200, 120) == BLACK
             and pixel(d, 400, 90) == BLACK, 15)
expect(d is not None, "the close mark closed the welcome window")
if d:
    expect(count(d, GREEN) > 10000,
           "the guest window stands whole while the welcome is closed")

# The word 'welcome' opens it again, forward.
typewrite("welcome")
enter()
d = waitdump(lambda d: d is not None and pixel(d, 200, 120) == GRAY
             and pixel(d, 400, 90) == BLUE, 15)
expect(d is not None, "the word 'welcome' opened its window again, forward")

# The typing line still works, with the windows about.
typewrite("hello")
enter()
d = waitdump(lambda d: d is not None and band_count(d, GRAY, 0, 384, 1024, 400) > 50, 20)
expect(d is not None, "'hello' is answered in light, the windows about")

done()
