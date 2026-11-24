# Stone 43 proof, boot 3: an xHCI controller and a USB
# keyboard, but no stick. The rising offers nothing,
# and the 'usb' word names the keyboard and no stick:
# the road's absence changes nothing.


def region_has(rows_, text):
    return any(text in rows_[r] for r in range(13, 23))


found = waitfor(lambda r: r[4][10:29] == "Welcome to Cardnull", 25)
expect(found is not None, "the desktop is up")
expect(not region_has(found, "Type setup to let it remember"),
       "nothing is offered when no disk stands fitted")

typewrite("usb")
enter()
found = waitfor(
    lambda r: region_has(r, "A USB keyboard is ready on the modern USB road."), 20)
expect(found is not None, "'usb' reports the keyboard as always")
if found:
    expect(not region_has(found, "A USB stick is here."),
           "'usb' names no stick when none stands on the bus")

done()
