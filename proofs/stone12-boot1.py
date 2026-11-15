# Stone 12 proof, boot 1: real typing on the PS/2 road.
# A shifted sentence is typed and read back off the typing
# line exactly; a two-word line is answered by its first
# word; Caps Lock makes capitals until it is turned off
# again; a figure and its shifted mark type as themselves;
# and a single-word command answers exactly as it always
# has.


def region_has(rows_, text):
    return any(text in rows_[r] for r in range(13, 23))


found = waitfor(lambda r: r[4][10:29] == "Welcome to Cardnull", 25)
expect(found is not None, "the desktop is up")

# The shifted sentence: "Hello Cardnull".
sendkey("shift-h")
typewrite("ello")
sendkey("spc")
sendkey("shift-c")
typewrite("ardnull")
found = waitfor(lambda r: r[24].startswith("> Hello Cardnull"), 15)
expect(found is not None, "the shifted sentence stands on the typing line exactly")
enter()
found = waitfor(lambda r: region_has(r, "I don't know that word yet."), 20)
expect(found is not None,
       "the two-word line is answered by its first word (Hello is no command)")

# The first word is the command word: "hello world" greets.
typewrite("hello world")
enter()
found = waitfor(lambda r: region_has(r, "Hello. It is good to see you."), 20)
expect(found is not None, "'hello world' is answered as 'hello'")

# Caps Lock: capitals until it is turned off again.
sendkey("caps_lock")
typewrite("hello")
found = waitfor(lambda r: r[24].startswith("> HELLO"), 15)
expect(found is not None, "Caps Lock makes the line capitals")
enter()
found = waitfor(lambda r: region_has(r, "I don't know that word yet."), 20)
expect(found is not None, "the capital word is answered as an unknown word")
sendkey("caps_lock")

# A figure and its shifted mark: "a1!".
typewrite("a")
sendkey("1")
sendkey("shift-1")
found = waitfor(lambda r: r[24].startswith("> a1!"), 15)
expect(found is not None, "a figure and its shifted mark type as themselves")
enter()

# A single-word command, byte-identical to before.
typewrite("memory")
enter()
found = waitfor(lambda r: region_has(r, "bytes of memory"), 20)
expect(found is not None, "'memory' answers exactly as it always has")

done()
