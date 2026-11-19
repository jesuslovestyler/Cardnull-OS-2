# Stone 9 proof, boot 2: a disc carrying a tampered feather,
# booted from its ISO — the face of light must refuse it
# exactly as the text face does: no green anywhere, and the
# refusal drawn as an answer in light.

BLUE = (0, 0, 170)
GRAY = (170, 170, 170)
GREEN = (0, 170, 0)


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
expect(d is not None, "the pixel desktop came up on the tampered-feather disc")

typewrite("feather")
enter()
# Stone 38: the visit brings the feather window
# forward over the terminal's first answer rows, so
# the refusal — printed in the terminal as an answer,
# in the same light gray — stands covered until the
# feather window is closed with Escape, the way a
# person would uncover it.
sendkey("esc")
d = waitdump(lambda d: d is not None and band(d, 528, 560, GRAY) > 50, 25)
expect(d is not None, "the refusal is drawn as an answer in light")
if d:
    expect(count(d, GREEN) < 100,
           f"the refused feather never appears (green pixels: {count(d, GREEN)})")

done()
