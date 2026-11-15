# Stone 8 proof, boot 3: the same disk a third time. Boot
# 2's 'eastern' was written back, so the clock must come
# up at hour 19 — the write-back persisted, in the other
# direction.


def hour_of(rows_):
    return rows_[0][72:74]


found = waitfor(lambda r: hour_of(r) == "19", 25)
expect(found is not None,
       "boot 2's kept choice persisted (hour 19 at boot)")

done()
