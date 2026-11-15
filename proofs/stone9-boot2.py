# Stone 9 proof, boot 2: a disc carrying a tampered guest,
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
expect(d is not None, "the pixel desktop came up on the tampered-guest disc")

typewrite("guest")
enter()
d = waitdump(lambda d: d is not None and band(d, 384, 448, GRAY) > 50, 25)
expect(d is not None, "the refusal is drawn as an answer in light")
if d:
    expect(count(d, GREEN) < 100,
           f"the refused guest never appears (green pixels: {count(d, GREEN)})")

done()
