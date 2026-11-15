# Stone 9 proof, boot 1: the shipped disc itself, booted
# from the ISO file — the face of light. The loader is
# asked for 1024x768 and must grant a picture screen; the
# desktop must be DRAWN: the blue bar with its title and
# clock, the light-gray welcome panel with its words, the
# invitation, the typing line's echo, an answer in light,
# the clock's hand moving, and the guest's visit shown as
# light in the guest's own colors. Read back by sampling
# the monitor's screendump (tools/pixels.py).

BLUE = (0, 0, 170)
GRAY = (170, 170, 170)
GREEN = (0, 170, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def band(d, y0, y1, rgb, x0=0, x1=1024):
    w, h, px = d
    n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            o = (y * w + x) * 3
            if (px[o], px[o + 1], px[o + 2]) == rgb:
                n += 1
    return n


d = waitdump(lambda d: d is not None and d[0] == 1024 and count(d, BLUE) > 5000, 40)
expect(d is not None, "a picture screen was granted and the desktop is drawn")
if d:
    expect(d[1] == 768, f"the granted screen is 1024x768 (height {d[1]})")
    expect(pixel(d, 8, 8) == BLUE and pixel(d, 1000, 8) == BLUE,
           "the bar is blue from end to end")
    expect(band(d, 0, 16, WHITE, 16, 130) > 100,
           "the title 'Cardnull' stands in white on the bar")
    expect(pixel(d, 200, 120) == GRAY, "the welcome panel is light gray")
    expect(band(d, 112, 128, BLACK, 128, 1000) > 500,
           "the panel's first line is drawn (dark letters on the gray)")
    expect(band(d, 176, 192, BLACK, 128, 1000) > 500,
           "the panel's verse line is drawn")
    expect(band(d, 336, 352, GRAY) > 30, "the invitation is drawn")

typewrite("time")
d = waitdump(lambda d: d is not None and band(d, 736, 752, GRAY) > 30, 15)
expect(d is not None, "the typing line echoes in light")
enter()
d = waitdump(lambda d: d is not None and band(d, 384, 400, GRAY) > 50, 20)
expect(d is not None, "the word 'time' is answered in light")

d1 = dump()
time.sleep(2.6)
d2 = dump()
diff = sum(1 for x in range(880, 1024) for y in range(0, 16)
           if pixel(d1, x, y) != pixel(d2, x, y))
expect(diff > 20, f"the drawn clock's hand moves ({diff} pixels changed)")

typewrite("guest")
enter()
d = waitdump(lambda d: d is not None and count(d, GREEN) > 10000, 25)
expect(d is not None, "the guest's visit is shown: its green panel as light")
if d:
    expect(band(d, 448, 592, WHITE, 100, 900) > 1000,
           "the guest's own white letters are drawn in its panel")

done()
