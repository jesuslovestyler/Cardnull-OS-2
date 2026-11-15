# Cardnull OS 2

**The operating system of [Cardnull](https://cardnull.com), written in
[Nifla](https://github.com/jesuslovestyler/Nifla) — public domain at every
layer: the language and the system together.**

Cardnull OS 2 is a Christian operating system, built from scratch in Nifla,
Cardnull's own public-domain programming language. Nothing underneath it is
borrowed: no licensed kernel, no licensed language, no runtime carrying
someone else's terms. What is here is given away, free for anyone to read,
learn from, copy, and build on, forever.

It is the successor to the [first Cardnull OS](https://github.com/jesuslovestyler/Cardnull-OS),
which was written in Swift, reached a complete desktop (milestones M1–M38),
and was retired on November 14, 2026 so that this one could be built in
Cardnull's own language instead. The first system's work is not lost — its
lessons are this one's blueprint — and its repository stands as the
permanent public-domain record of it.

Founded November 15, 2026, by Tyler Austin James Kovalevich, in
Washington, North Carolina.

> *Unless Yahweh builds the house, they labor in vain who build it.*
> — Psalm 127:1 (World English Bible)

## Building

The compiler belongs to the language, not to this repository: you need a
checkout of [Nifla](https://github.com/jesuslovestyler/Nifla) beside this
one. By default the build looks for it at `~/workspace/nifla-repo`; set
`NIFLA_REPO` to point somewhere else.

```
./build.sh            # makes build/cardnull.elf (and build/guest.bin, later)
```

The result is a bare-metal program: it boots on its own, with no operating
system underneath. The proofs boot it in QEMU with no display and read the
emulated screen's memory back through the QEMU monitor — the same bench
pattern the Nifla language's own bare-metal proofs use:

```
./prove-stone1.sh     # one script per stone; each prints PASS or FAIL
```

QEMU is the bench's extracted QEMU 10 (`~/qemu10-root`) when present; set
`QEMU` to a plain `qemu-system-x86_64` command line if yours is installed.

## The stones

The system is built stone by stone, in order. Each stone is proven on the
bench before the next begins, and its honest limits are written down here.

### Founding (November 15, 2026)

This repository, the license, the build, and the proof bench. No system
code yet — the first stone is the first boot.

### Stone 1 — First boot

The seed kernel (`src/cardnull.nifla`) boots on its own, greets the
person in plain words — "Cardnull", a welcome, and the machine's memory
reported plainly from the loader's memory map — and then stays alive,
sleeping between timer ticks. Proven by `prove-stone1.sh`: booted
headless with 96 MiB, the screen read back the greeting and the figure
100,137,984 bytes (95 megabytes), the usable sum for that machine.

Honest limits: the greeting is three lines and the machine then simply
waits — it cannot hear the keyboard yet (Stone 2), has no face (Stone 3),
and the clock the tick makes possible is not shown yet. The memory
figure is the loader map's usable sum, which is always a little less
than the machine's whole memory; the firmware's reserved stretches are
not counted, and nothing here manages memory beyond reading the map.

### Stone 2 — Ears

The keyboard is heard. A typing line lives on the screen's last row:
letters echo as they are typed, Backspace un-types, and Enter offers
the word to a small command loop that answers in plain words — `hello`
(a greeting back), `time` (the seconds since the machine woke, from
the timer tick), `memory` (the memory figure), and `clear` (the screen
is wiped). Any other word is answered kindly: "I don't know that word
yet. Try hello, time, memory, or clear." Proven by `prove-stone2.sh`:
it types "hellx", erases the x, finishes "hello", and reads every
answer back off the emulated screen, including that the machine still
answers after a clear.

Honest limits: the machine knows only single lowercase words — no
capital letters (there is no shift state yet), no digits in words, and
no commands with parts. Answers appear where the screen's writing
cursor stands and scroll as they accumulate; after `clear`, the
greeting is gone until the next boot and later answers appear wherever
that cursor had reached. The face (Stone 3) gives answers a proper
home. Keystrokes are gathered in a 48-number buffer; a longer word is
simply not gathered further. (`prove-stone2.sh` describes this
pre-face screen; from Stone 3 on, its command checks live on in the
later proofs, against the faced screen.)

### Stone 3 — A face

The desktop. The system's own screen library (`src/screenlib.nifla`,
joined as a prelude) paints a top bar — "Cardnull" at the left and a
live clock at the right, white on blue — and a welcome panel in the
middle, black on light gray, saying what this is, that it is public
domain and free for everyone, and carrying the founding verse
(Psalm 127:1). Answers now have their own region of the screen and
scroll within it; the typing line still works at the bottom with the
same four words, and `clear` now restores the whole face and empties
the answers. Proven by `prove-stone3.sh`: full-screen readback
verified the bar and panel text, their color bytes (31 and 112), and
the clock advancing between two readings (00:00:00 → 00:00:02), and
the commands answering in their region.

Honest limits: the clock counts from the moment the machine woke —
it is an honest count of uptime, not the world's time; nothing reads
a real-time clock yet, and Stone 4's remembered offset shifts the
shown hour without changing that. The face is drawn in the text
screen's sixteen colors, one panel, no windows, no mouse. The panel
and bar are repainted only when drawn; a guest or a stray writer
could paint over them, and nothing yet defends the arrangement
except the system's own manners.

### Stone 4 — Remembers

The system keeps one setting on the disk: the clock's hour offset.
Two new words set it in plain language — `eastern` (the system's
home time, five hours behind the world's standard) and `utc` (the
world's standard time itself) — and the choice is written to a small
card of the system's own on sector 8 of the disk. At every boot the
card is read back and the bar's clock applies it, without being told
again. When no card has ever been saved, the clock starts on Eastern
time: the first Cardnull OS taught this lesson on real hardware,
where its clock quietly showed the world's standard hour as if it
were local, and this system was designed so as never to repeat it.
Proven by `prove-stone4.sh`: two boots of one scratch disk — a fresh
disk starts at hour 19, the word `utc` moves it to 00 and the machine
says it will remember, and the second boot comes up at 00 on its own
before `eastern` moves it back to 19.

Honest limits, stated exactly: there is still no reading of the
world's clock — the count is the time since the machine woke, and
the offset shifts only the hour the face shows, the way setting a
clock does; nothing here knows the date or the world's present hour.
The choice is kept on the first disk only, in the system's own small
card (the letters C and N and one byte), not in any standard format
another system would read. When there is no disk at all, the words
still work for the session, and the machine says plainly that there
is no disk to remember the choice on. Before asking the drive who it
is, the system selects it with a small piece of floor work — see the
builder note below; without that, the language's own way of asking
would report no disk even when one is fitted.

## Notes for builders

- The visible screen of this system speaks **plain words only** — no codes
  and no jargon on the desktop surface. Diagnostics belong in proofs and
  in this README, not on the screen a person reads.
- On bare metal, Nifla functions must not read or assign the program's
  shared (global) variables: measured on the bench, a function that does
  so receives a broken value, while the same variables work correctly in
  the program's main body. Every helper in this system is therefore
  written in the pure style — values go in as arguments and come back as
  results — and all state is kept in the main body. (A finding about the
  language as it stands at Stone 18; the language is not changed from
  here.)
- The language's `disksectors()` reads the drive's status port before
  selecting the drive, and an unselected drive's status reads as
  nothing there — so on a freshly booted machine it answers 0 even
  with a disk fitted, until some transfer has selected the drive.
  Measured both ways on the bench. This system therefore selects the
  drive first, with a three-instruction floor block (`selectdrive()`),
  after which `disksectors()` answers truthfully with and without a
  disk. A `diskread` or `diskwrite` with no disk fitted still stops
  the machine, exactly as the language's Stone 16 notes say, so the
  system never attempts a transfer until the selection and the
  question have both said a drive is there. (Also a finding, reported
  rather than repaired from here.)
