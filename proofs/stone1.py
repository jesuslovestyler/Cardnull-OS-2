# Stone 1 proof scenario: first boot.
# The bench machine is started with -m 96, so the screen must
# greet in plain words and report a memory figure that matches
# what the loader's map calls usable for a 96 MiB machine:
# the machine holds 100663296 bytes; the usable sum is a
# little less (the firmware's reserved stretches are not
# usable) — the band (94 MiB, 96 MiB], measured on this bench
# as 100137984 bytes, 95 whole megabytes.
import re

found = waitfor(lambda r: r[0].startswith("Cardnull"), 25)
expect(found is not None, "the welcome appeared on the screen")
if found:
    expect(found[0].startswith("Cardnull"),
           f"row 1 is the name: {found[0][:20]!r}")
    expect(found[1].startswith("Welcome. This computer is yours"),
           f"row 2 is the greeting: {found[1][:40]!r}")
    m = re.match(r"This machine has (\d+) bytes of memory \((\d+) megabytes\)\.", found[2])
    expect(m is not None, f"row 3 reports the memory plainly: {found[2][:60]!r}")
    if m:
        total, megabytes = int(m.group(1)), int(m.group(2))
        expect(94 * 1048576 < total <= 96 * 1048576,
               f"the byte figure {total} is in the band for a 96 MiB machine")
        expect(megabytes == total // 1048576,
               f"the megabyte figure {megabytes} agrees with the bytes")
        print(f"readback: {total} bytes, {megabytes} megabytes")
done()
