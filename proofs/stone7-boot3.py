# Stone 7 proof, boot 3: the bench clock is pinned to
# Sunday, November 15, 2026, 23:59:50 in the world's
# standard time, and the disc carries the world's own
# choice (UTC). The bar must come up on November 15 at
# 23:59 — and then, as the bench clock ticks over the
# minute, roll forward on its own: Monday, November 16,
# at 00:00. The date turning by itself is the proof.

found = waitfor(
    lambda r: "Sunday, November 15, 2026" in r[0]
    and r[0][72:77] == "23:59", 25)
expect(found is not None,
       "the bar comes up on Sunday, November 15, at 23:59")

found = waitfor(
    lambda r: "Monday, November 16, 2026" in r[0]
    and r[0][72:77] == "00:00", 30)
expect(found is not None,
       "the date rolls forward over midnight on its own")

done()
