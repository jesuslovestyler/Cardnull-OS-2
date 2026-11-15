# Stone 2 proof scenario: ears.
# The bench types on the emulated keyboard and reads the
# screen back: the typing line must echo (with a Backspace
# correction along the way), and each word must be answered
# in plain words. 'clear' must wipe the screen — and the
# machine must still answer afterwards.
import re


def anywhere(rows_, needle):
    return any(needle in row for row in rows_)


def anywhere_match(rows_, pattern):
    return any(re.search(pattern, row) for row in rows_)


found = waitfor(lambda r: anywhere(r, "Try: hello, time, memory, clear"), 25)
expect(found is not None, "the boot greeting and the invitation appeared")

# Type "hellx", erase the x, finish "hello": the typing line
# must show the corrected word before Enter is pressed.
typewrite("hellx")
backspace()
typewrite("o")
found = waitfor(lambda r: r[24].startswith("> hello"), 15)
expect(found is not None, "the typing line shows '> hello' after a Backspace fix")

enter()
found = waitfor(lambda r: anywhere(r, "Hello. It is good to see you."), 15)
expect(found is not None, "'hello' was answered with a greeting")

typewrite("time")
enter()
found = waitfor(lambda r: anywhere_match(r, r"awake for (\d+) seconds"), 15)
expect(found is not None, "'time' was answered with the seconds awake")
if found:
    for row in found:
        m = re.search(r"awake for (\d+) seconds", row)
        if m:
            expect(int(m.group(1)) >= 1,
                   f"the seconds awake are real: {m.group(1)}")
            print(f"readback: awake for {m.group(1)} seconds")

typewrite("memory")
enter()
found = waitfor(lambda r: anywhere(r, "bytes of memory (95 megabytes)"), 15)
expect(found is not None, "'memory' was answered with the memory figure")

typewrite("bogus")
enter()
found = waitfor(lambda r: anywhere(r, "I don't know that word yet."), 15)
expect(found is not None, "an unknown word got the kind plain-words answer")

typewrite("clear")
enter()
found = waitfor(
    lambda r: all(row.strip() == "" for row in r[:24]) and r[24].startswith(">"),
    15,
)
expect(found is not None, "'clear' wiped the screen, leaving only the typing line")

typewrite("hello")
enter()
found = waitfor(lambda r: anywhere(r, "Hello. It is good to see you."), 15)
expect(found is not None, "the machine still answers after a clear")

done()
