# Stone 18 proof, boot 2: the 'chime' word, read back.
#
# The text face (the kernel built without the video
# asking, as in Stone 9's third boot) — and this boot
# has NO audio device attached at all: the voice's
# waits are bounded, the boot and the typing are
# unheld, and the word is answered in plain words.
# Machines without the speaker path are unaffected;
# this boot is that evidence.

found = waitfor(lambda r: r[4][10:29] == "Welcome to Cardnull", 25)
expect(found is not None, "the desktop is up (no audio device attached)")

typewrite("chime")
enter()
found = waitfor(
    lambda r: any("The welcome chime, once more." in r[i]
                  for i in range(13, 23)), 15)
expect(found is not None, "'chime' is answered in plain words")

typewrite("hello")
enter()
found = waitfor(
    lambda r: any("Hello. It is good to see you." in r[i]
                  for i in range(13, 23)), 15)
expect(found is not None, "typing still works after the chime")

done()
