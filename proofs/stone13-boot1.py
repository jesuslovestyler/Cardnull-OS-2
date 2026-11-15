# Stone 13 proof, boot 1: the pointer on the face of
# light. The arrow stands at the screen's middle when the
# desktop rises; the monitor's own mouse_move carries it
# (its +x is right and its +y is down, as the bench
# speaks); where it left, the desktop stands whole again;
# and a press of the first button with the arrow's point
# on the guest's panel brings the guest — the same visit
# the word 'guest' brings, its green panel and all. No
# green stands anywhere before the press.

BLUE = (0, 0, 170)
GREEN = (0, 170, 0)
GRAY = (170, 170, 170)
WHITE = (255, 255, 255)


def arrow_white(d, x0, y0):
    """The arrow's white edge, counted in its square."""
    if d is None:
        return 0
    n = 0
    for y in range(y0, y0 + 16):
        for x in range(x0, x0 + 16):
            if pixel(d, x, y) == WHITE:
                n += 1
    return n


d = waitdump(lambda d: d is not None and d[0] == 1024 and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")
if d:
    expect(count(d, GREEN) == 0, "no guest panel stands before the press")
    expect(arrow_white(d, 504, 376) > 20,
           "the arrow stands at the screen's middle")

# The arrow follows the mouse: right 200, down 100.
mousemove(200, 100)
d = waitdump(lambda d: d is not None and arrow_white(d, 704, 476) > 20, 15)
expect(d is not None, "the arrow followed the mouse to its new place")
if d:
    expect(arrow_white(d, 504, 376) == 0,
           "where the arrow left, the desktop stands whole")

# Onto the guest's panel, and press: the panel's ground
# on the face is x 176..832, y 448..608; the arrow's
# point is its square's (2, 2), standing at (706, 478)
# now — a move of (-306, +42) lays it at (400, 520),
# well inside.
mousemove(-306, 42)
d = waitdump(lambda d: d is not None and arrow_white(d, 398, 518) > 20, 15)
expect(d is not None, "the arrow stands on the guest's panel")
mousebutton(1)
mousebutton(0)
d = waitdump(lambda d: d is not None and count(d, GREEN) > 10000, 25)
expect(d is not None, "the press brought the guest: its green panel stands")

# The typing line still works, with the pointer about.
typewrite("hello")
enter()
d = waitdump(lambda d: d is not None and sum(
    1 for y in range(384, 400) for x in range(0, 1024)
    if pixel(d, x, y) == GRAY) > 50, 20)
expect(d is not None, "'hello' is answered in light, the pointer about")

done()
