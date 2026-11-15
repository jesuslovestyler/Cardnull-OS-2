# Stone 15 proof, boot 5: the face of light, the shipped
# disc booted from the ISO file with the keeping disk
# attached. The notes read back at boot are shown in
# light: 'notes' draws the heading in the answers region,
# and the three kept notes beneath it, letter by letter
# from their bytes — gray letters counted in the rows
# below the heading's own row.

BLUE = (0, 0, 170)
GRAY = (170, 170, 170)


def band_count(d, rgb, x0, y0, x1, y1):
    if d is None:
        return 0
    n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pixel(d, x, y) == rgb:
                n += 1
    return n


d = waitdump(lambda d: d is not None and d[0] == 1024 and count(d, BLUE) > 5000, 40)
expect(d is not None, "the desktop is drawn")

typewrite("notes")
enter()
d = waitdump(lambda d: d is not None
             and band_count(d, GRAY, 32, 400, 760, 448) > 100, 25)
expect(d is not None, "the kept notes are drawn in light on the face of light")

done()
