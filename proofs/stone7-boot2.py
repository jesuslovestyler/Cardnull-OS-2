# Stone 7 proof, boot 2: the bench clock is pinned to
# Monday, November 16, 2026, 02:00 in the world's standard
# time, and the disc carries the Eastern choice. Five
# hours back crosses midnight: the bar must show the
# evening before — Sunday, November 15, at 21:00. The date
# the offset carries the moment to is part of the answer,
# not just the hour.

found = waitfor(
    lambda r: "Sunday, November 15, 2026" in r[0]
    and r[0][72:77] == "21:00", 25)
expect(found is not None,
       "the bar shows Sunday, November 15, 2026, at 21:00 "
       "(the offset carried the date back over midnight)")

done()
