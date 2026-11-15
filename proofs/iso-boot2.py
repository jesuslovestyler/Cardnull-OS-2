# Witness-disc proof, boot 2: a variant disc whose settings
# carry the world's standard time. Booted from that ISO as
# a CD-ROM, the clock must come up at hour 00 on its own —
# proving the choice truly rides the disc, and is not a
# habit of the kernel.
import re


def hour_of(rows_):
    m = re.match(r"(\d\d):\d\d:\d\d", rows_[0][72:80])
    return m.group(1) if m else None


found = waitfor(lambda r: r[4][10:29] == "Welcome to Cardnull", 40)
expect(found is not None, "the desktop came up booting from the variant ISO")
if found:
    expect(hour_of(found) == "00",
           f"the variant disc's carried choice was read (hour {hour_of(found)}, want 00)")

done()
