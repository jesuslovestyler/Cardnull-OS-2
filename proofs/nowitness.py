# The witness-fix proof scenario: the face, with NO
# hands on the machine at all.
#
# The fifteen standing proofs drive the machine with
# injected keys and read its memory or its screen after
# the interaction — a first-paint fault is invisible to
# that method, which is how the build that Tyler
# witnessed on November 15, 2026 passed every proof and
# still showed him a black screen at the EFI door and a
# fallback face at the BIOS door. This scenario is the
# correction: it boots, sends NO key, moves NO mouse,
# and only watches the screen until the drawn desktop
# stands on it — the bar, the panel, the panel's words,
# the invitation — the very landmarks the Stone 9 proof
# samples, reached here with empty hands.
#
# Run by prove-nowitness.sh through tools/pixels.py, at
# both doors and on both machine shapes the bench has,
# and from the stick.

BLUE = (0, 0, 170)
GRAY = (170, 170, 170)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def band(d, y0, y1, rgb, x0=0, x1=1024):
    w, h, px = d
    n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            o = (y * w + x) * 3
            if (px[o], px[o + 1], px[o + 2]) == rgb:
                n += 1
    return n


d = waitdump(lambda d: d is not None and d[0] == 1024 and count(d, BLUE) > 5000, 45)
expect(d is not None, "with no input at all, a picture screen was granted and the desktop is drawn")
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

done()
