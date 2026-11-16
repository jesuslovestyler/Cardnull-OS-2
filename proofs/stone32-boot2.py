# Stone 32 proof, boot 2: the modern controller stands
# in the machine but NO keyboard is plugged into it
# (boot 3 runs the same script with no modern controller
# at all). The desktop must come up with no complaint
# and no ready word for the modern road; the PS/2 road
# must carry typing as it always has; and the 'usb' word
# must answer plainly that no USB keyboard is plugged in.


def region_has(rows_, text):
    return any(text in rows_[r] for r in range(13, 23))


found = waitfor(lambda r: r[4][10:29] == "Welcome to Cardnull", 25)
expect(found is not None, "the desktop is up")

waitfor(lambda r: False, 3)
rows_now = waitfor(lambda r: r, 5)
expect(rows_now is not None
       and not region_has(rows_now, "A USB keyboard is ready on the modern USB road."),
       "no modern ready word when no keyboard is plugged into it")

typewrite("hello")
enter()
found = waitfor(lambda r: region_has(r, "Hello. It is good to see you."), 20)
expect(found is not None, "the PS/2 road still answers 'hello'")

typewrite("usb")
enter()
found = waitfor(
    lambda r: region_has(r, "No USB keyboard is plugged in."), 20)
expect(found is not None,
       "the 'usb' word answers plainly: no USB keyboard")

done()
