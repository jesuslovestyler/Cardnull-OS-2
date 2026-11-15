# Stone 3 proof scenario: a face.
# The desktop must be on the emulated screen: the bar with
# the name and a live clock (verified by its color bytes and
# by the clock advancing between two readings), the welcome
# panel with its lines in its color, and the Stone 2 commands
# still working against the faced screen — their answers now
# landing in the answer region.
import re


def region_has(rows_, needle):
    return any(needle in rows_[r] for r in range(13, 23))


found = waitfor(lambda r: r[4][10:29] == "Welcome to Cardnull", 25)
expect(found is not None, "the welcome panel appeared")
if found:
    expect(found[0][1:9] == "Cardnull",
           f"the bar carries the name: {found[0][:12]!r}")
    expect("This computer is public domain: free for everyone, forever." in found[5],
           "the panel says what this is: public domain, free for everyone")
    expect("Unless Yahweh builds the house," in found[7],
           "the panel carries the Scripture line (first half)")
    expect("they labor in vain who build it." in found[8]
           and "Psalm 127:1" in found[8],
           "the panel carries the Scripture line (second half, named)")

colors = attrs()
expect(colors is not None, "the color bytes could be read")
if colors:
    expect(colors[0][0] == 31 and colors[0][40] == 31 and colors[0][79] == 31,
           "the bar is white on blue (31) from end to end")
    expect(colors[4][10] == 112 and colors[5][30] == 112,
           "the panel is black on light gray (112)")

# The clock: shaped like a clock, and alive.
first = waitfor(lambda r: re.match(r"\d\d:\d\d:\d\d", r[0][72:80]), 15)
expect(first is not None, "the bar's right end shows a clock")
if first:
    t1 = first[0][72:80]
    time.sleep(2.2)
    second = rows()
    t2 = second[0][72:80]
    to_seconds = lambda t: int(t[0:2]) * 3600 + int(t[3:5]) * 60 + int(t[6:8])
    expect(to_seconds(t2) > to_seconds(t1),
           f"the clock advanced between readings: {t1} -> {t2}")
    print(f"readback: clock {t1} -> {t2}")

# The commands, against the faced screen.
typewrite("hello")
enter()
found = waitfor(lambda r: region_has(r, "Hello. It is good to see you."), 15)
expect(found is not None, "'hello' is answered in the answer region")

typewrite("time")
enter()
found = waitfor(lambda r: region_has(r, "awake for"), 15)
expect(found is not None, "'time' is answered in the answer region")

typewrite("bogus")
enter()
found = waitfor(lambda r: region_has(r, "I don't know that word yet."), 15)
expect(found is not None, "an unknown word gets the kind answer in the region")

# 'clear' restores the face and empties the answers.
typewrite("clear")
enter()
found = waitfor(
    lambda r: r[4][10:29] == "Welcome to Cardnull"
    and not region_has(r, "Hello. It is good to see you."),
    15,
)
expect(found is not None, "'clear' restores the face and empties the answers")

done()
