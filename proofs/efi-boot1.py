# Boot 1 of the EFI door's proof: the shipped disc
# booted at the UEFI door (the bench's OVMF firmware,
# prove-efi.sh) — never checked since the door was
# built, and owed since Stone 41's hunt set the BIOS
# doorman right and told the two doors apart. The
# desktop must rise at this door; the Files icon's
# name must read; the feather window must stand; the
# word 'feather' must bring the welcome feather
# through the door — its module rides the disc's
# module row at this door too, read into the
# firmware's own buffers — card-checked and painting
# its own panel; the word 'bible' must open the
# Bible window on its contents page; and Escape
# must close it, the visited feather's panel standing
# in the clear again where the window stood.

import re

BLUE = (0, 0, 170)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (170, 170, 170)
GREEN = (0, 170, 0)

_vals = {}
for _m in re.finditer(r"block\[(\d+)\] = (\d+)",
                      open("src/font.nifla").read()):
    _vals[int(_m.group(1))] = int(_m.group(2))
GLYPHS = {}
for _code in range(32, 127):
    GLYPHS[_code] = tuple(_vals.get((_code - 32) * 8 + _r, 0)
                          for _r in range(8))


def cell_bitmap(d, cx, cy, ink):
    rows = []
    for r in range(8):
        v = 0
        for c in range(8):
            if pixel(d, cx + 2 * c + 1, cy + 2 * r + 1) == ink:
                v |= 1 << (7 - c)
        rows.append(v)
    return tuple(rows)


def decode(d, prow, pcol, text, ink):
    if d[0] < (pcol + len(text)) * 16 or d[1] < (prow + 1) * 16:
        return ""
    out = []
    for i in range(len(text)):
        bm = cell_bitmap(d, (pcol + i) * 16, prow * 16, ink)
        if all(v == 0 for v in bm):
            out.append(" ")
            continue
        best, bestd = None, 999
        for code, g in GLYPHS.items():
            dist = sum(bin(a ^ b).count("1") for a, b in zip(bm, g))
            if dist < bestd:
                bestd, best = dist, code
        out.append(chr(best) if bestd <= 2 else "?")
    return "".join(out)


d = waitdump(lambda d: d is not None and d[0] == 1024
             and count(d, BLUE) > 5000, 60)
expect(d is not None, "the desktop is drawn at the EFI door")
if d:
    said = decode(d, 2, 4, "Files", WHITE)
    expect(said == "Files",
           f"the Files icon's name reads at the EFI door (read: {said!r})")
    said = decode(d, 28, 7, "No feather has visited yet.", GRAY)
    expect(said == "No feather has visited yet.",
           f"the feather window stands at the EFI door (read: {said!r})")

typewrite("feather")
enter()
d = waitdump(lambda d: d is not None and count(d, GREEN) > 10000, 30)
expect(d is not None, "the feather visited at the EFI door: its green panel as light")
if d:
    line1 = decode(d, 29, 8, "A feather is visiting", WHITE)
    expect(line1 == "A feather is visiting",
           f"the feather's first line reads at the EFI door (read: {line1!r})")
    line3 = decode(d, 31, 8, "I was checked first, and I am whole.", WHITE)
    expect(line3 == "I was checked first, and I am whole.",
           f"the feather's third line reads at the EFI door (read: {line3!r})")

typewrite("bible")
enter()
d = waitdump(lambda d: d is not None
             and decode(d, 30, 6, "Bible", WHITE) == "Bible"
             and decode(d, 44, 13, "Page 1 of 30", BLACK) == "Page 1 of 30", 30)
expect(d is not None, "the word 'bible' opened the Bible window at the EFI door")

sendkey("esc")
# Closed means: the Bible title no longer stands, and
# what the window covered — the visited feather's
# green panel — stands in the clear again.
d = waitdump(lambda d: d is not None
             and decode(d, 30, 6, "Bible", WHITE) != "Bible"
             and count(d, GREEN) > 10000, 15)
expect(d is not None, "Escape closed the Bible window at the EFI door")

done()
