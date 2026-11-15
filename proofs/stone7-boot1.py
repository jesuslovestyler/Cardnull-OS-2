# Stone 7 proof, boot 1: the bench clock is pinned to a
# known instant — Sunday, November 15, 2026, 14:32 in the
# world's standard time — and the disc carries the Eastern
# choice. The bar must show the real date in plain words
# and the real time, five hours back: 09:32 on Sunday,
# November 15. The 'time' word must tell the same moment
# in words, with the waking count beneath it.


def region_has(rows_, text):
    return any(text in rows_[r] for r in range(13, 23))


found = waitfor(
    lambda r: "Sunday, November 15, 2026" in r[0]
    and r[0][72:77] == "09:32", 25)
expect(found is not None,
       "the bar shows Sunday, November 15, 2026, at 09:32 (Eastern)")

typewrite("time")
enter()
found = waitfor(
    lambda r: region_has(r, "on Sunday, November 15, 2026."), 20)
expect(found is not None, "'time' tells the date in words")
if found:
    expect(region_has(found, "The time is 09:32:"),
           "'time' tells the hour in words")
    expect(region_has(found, "awake for"),
           "'time' still tells the waking count beneath")

done()
