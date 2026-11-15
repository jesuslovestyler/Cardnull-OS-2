# Stone 9 proof, boot 3: the fallback. This disc is laid
# down with the same kernel built WITHOUT the video asking
# (build/cardnull-text.elf), so no picture screen is
# granted: the desktop must come up on the text screen —
# the system's first face — and say in plain words why it
# is in words. Commands work as they always have.

found = waitfor(lambda r: r[4][10:29] == "Welcome to Cardnull", 40)
expect(found is not None, "the text desktop came up when no picture was granted")
if found:
    said = any("No picture screen was granted, so this face stays in words." in r
               for r in found)
    expect(said, "the fallback is said in plain words on the desktop")

typewrite("hello")
enter()
found = waitfor(
    lambda r: any("Hello. It is good to see you." in r[r0] for r0 in range(25)), 20)
expect(found is not None, "the word 'hello' is answered on the text face")

done()
